"""Synthetic data generator for appointments and visits."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from app.config import APPOINTMENTS_CSV, VISITS_CSV, SAMPLE_DATA_DIR


def generate_appointments(n_appointments: int = 5000, n_branches: int = None, days_back: int = 30):
    """
    Generate synthetic appointment data.
    
    Args:
        n_appointments: Number of appointments to generate
        n_branches: Number of branches (if None, uses all Saudi cities)
        days_back: Number of days to go back from today
    
    Returns:
        DataFrame with appointment data
    """
    np.random.seed(42)
    
    # Generate appointment IDs
    appointment_ids = [f"APT-{i:06d}" for i in range(1, n_appointments + 1)]
    
    # Real Saudi cities and regions
    saudi_cities = [
        "Riyadh", "Jeddah", "Mecca", "Medina", "Dammam", "Khobar", "Dhahran",
        "Hail", "Qassim", "Abha", "Tabuk", "Najran", "Jazan", "Al-Baha",
        "Arar", "Sakaka", "Jubail", "Yanbu", "Taif", "Khamis Mushait",
        "Buraydah", "Hofuf", "Al-Kharj", "Al-Mubarraz", "Al-Hufuf"
    ]
    
    # Generate branch IDs with city names
    if n_branches is None:
        branch_ids = [f"{city}-Branch" for city in saudi_cities]
    else:
        branch_ids = [f"{city}-Branch" for city in saudi_cities[:n_branches]]
    
    # Generate national ID hashes (simulated)
    n_unique_ids = int(n_appointments * 0.7)  # Some people have multiple appointments
    national_id_hashes = [f"ID-{hash(str(i)) % 1000000:06d}" for i in range(n_unique_ids)]
    
    # Purposes
    purposes = ["ID Renewal", "Passport", "Traffic", "Civil Status", "Employment", "Other"]
    purpose_weights = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
    
    # Distribute appointments across cities (Riyadh and Jeddah get more)
    if len(branch_ids) <= 5:
        branch_weights = [0.3, 0.25, 0.20, 0.15, 0.10]
    else:
        # More realistic distribution: major cities get more appointments
        branch_weights = [0.25, 0.20, 0.15, 0.10, 0.08] + [0.22 / (len(branch_ids) - 5)] * (len(branch_ids) - 5)
    np.random.shuffle(branch_weights)  # Randomize order
    branch_weights = branch_weights[:len(branch_ids)]
    branch_weights = [w / sum(branch_weights) for w in branch_weights]  # Normalize
    
    # Generate data
    data = {
        "appointment_id": appointment_ids,
        "national_id_hash": np.random.choice(national_id_hashes, n_appointments),
        "branch_id": np.random.choice(branch_ids, n_appointments, p=branch_weights),
        "scheduled_time": [
            (datetime.now() - timedelta(days=int(np.random.randint(0, days_back))) + 
             timedelta(hours=int(np.random.randint(8, 17)), 
                      minutes=int(np.random.choice([0, 15, 30, 45]))))
            for _ in range(n_appointments)
        ],
        "purpose": np.random.choice(purposes, n_appointments, p=purpose_weights),
    }
    
    df = pd.DataFrame(data)
    df["scheduled_time"] = pd.to_datetime(df["scheduled_time"])
    
    return df


def generate_visits(n_visits: int = 20000, appointments_df: pd.DataFrame = None):
    """
    Generate synthetic visit data with some suspicious patterns.
    
    Args:
        n_visits: Number of visits to generate
        appointments_df: DataFrame with appointments (for linking)
    
    Returns:
        DataFrame with visit data
    """
    np.random.seed(42)
    
    if appointments_df is None:
        appointments_df = generate_appointments()
    
    # Generate visit IDs
    visit_ids = [f"VIS-{i:06d}" for i in range(1, n_visits + 1)]
    
    # Link some visits to appointments (70% have appointments)
    n_with_appointment = int(n_visits * 0.7)
    appointment_sample = appointments_df.sample(n=n_with_appointment, replace=True)
    
    appointment_links = list(appointment_sample["appointment_id"]) + [None] * (n_visits - n_with_appointment)
    np.random.shuffle(appointment_links)
    
    # Generate national ID hashes
    n_unique_ids = int(n_visits * 0.6)
    national_id_hashes = [f"ID-{hash(str(i)) % 1000000:06d}" for i in range(n_unique_ids)]
    
    # Generate device IDs (some devices used by multiple identities - suspicious)
    n_devices = int(n_visits * 0.3)
    device_ids = [f"DEV-{i:04d}" for i in range(1, n_devices + 1)]
    
    # Channels and auth methods
    channels = ["main_gate", "side_gate", "vip_gate"]
    auth_methods = ["face+fingerprint", "nafath", "biometric_only"]
    auth_risk_weights = [0.5, 0.3, 0.2]  # nafath has medium risk
    
    # Generate branches and gates with city names
    branches = appointments_df["branch_id"].unique()
    # Extract city names from branch IDs (e.g., "Riyadh-Branch" -> "Riyadh")
    city_names = [branch.split("-")[0] for branch in branches]
    gates = []
    for city in city_names:
        gates.extend([f"{city}-Gate-{i:02d}" for i in range(1, 4)])  # 3 gates per city
    
    # Create base data
    data = {
        "visit_id": visit_ids,
        "appointment_id": appointment_links,
        "national_id_hash": np.random.choice(national_id_hashes, n_visits),
        "branch_id": np.random.choice(branches, n_visits),
        "gate_id": np.random.choice(gates, n_visits),
        "channel": np.random.choice(channels, n_visits, p=[0.6, 0.3, 0.1]),
        "auth_method": np.random.choice(auth_methods, n_visits, p=auth_risk_weights),
        "device_id": np.random.choice(device_ids, n_visits),
    }
    
    df = pd.DataFrame(data)
    
    # Generate visit times (some linked to appointments, some not)
    visit_times = []
    for idx, row in df.iterrows():
        if row["appointment_id"]:
            # Visit time near appointment time (within 2 hours, 80% of time)
            apt_time = appointments_df[appointments_df["appointment_id"] == row["appointment_id"]]["scheduled_time"].iloc[0]
            if np.random.random() < 0.8:
                # Normal visit: within 2 hours
                time_diff = timedelta(hours=np.random.uniform(-1, 2))
            else:
                # Suspicious: way off schedule
                time_diff = timedelta(hours=np.random.uniform(-24, 24))
            visit_time = apt_time + time_diff
        else:
            # No appointment - random time in last 30 days
            visit_time = datetime.now() - timedelta(days=np.random.randint(0, 30), 
                                                     hours=np.random.randint(8, 18))
        visit_times.append(visit_time)
    
    df["visit_time"] = pd.to_datetime(visit_times)
    
    # Generate suspicious patterns
    # 1. Repeated attempts in last 24h
    repeated_attempts = []
    multi_branch_same_day = []
    label_suspicious = []
    
    # Group by national_id_hash and date to calculate features
    df["date"] = df["visit_time"].dt.date
    df_sorted = df.sort_values("visit_time")
    
    for idx, row in df_sorted.iterrows():
        national_id = row["national_id_hash"]
        visit_time = row["visit_time"]
        branch = row["branch_id"]
        
        # Count attempts in last 24h
        time_window = visit_time - timedelta(hours=24)
        attempts_24h = len(df_sorted[
            (df_sorted["national_id_hash"] == national_id) &
            (df_sorted["visit_time"] >= time_window) &
            (df_sorted["visit_time"] < visit_time)
        ])
        repeated_attempts.append(attempts_24h)
        
        # Multi-branch same day
        same_day_visits = df_sorted[
            (df_sorted["national_id_hash"] == national_id) &
            (df_sorted["date"] == row["date"]) &
            (df_sorted["visit_time"] < visit_time)
        ]
        unique_branches = same_day_visits["branch_id"].nunique()
        multi_branch_same_day.append(1 if unique_branches > 0 else 0)
        
        # Label as suspicious if multiple risk factors
        is_suspicious = (
            attempts_24h >= 3 or
            (unique_branches > 0 and len(same_day_visits) > 0) or
            row["auth_method"] == "nafath" or
            attempts_24h >= 2 and row["device_id"] in df_sorted[
                df_sorted["visit_time"] >= time_window
            ]["device_id"].value_counts().head(10).index.tolist()
        )
        label_suspicious.append(1 if is_suspicious else 0)
    
    df["repeated_attempts_last_24h"] = repeated_attempts
    df["multi_branch_same_day"] = multi_branch_same_day
    df["label_suspicious"] = label_suspicious
    
    # Drop temporary date column
    df = df.drop(columns=["date"])
    
    return df


def main():
    """Generate and save synthetic data."""
    print("Generating appointments...")
    appointments_df = generate_appointments()
    appointments_df.to_csv(APPOINTMENTS_CSV, index=False)
    print(f"✓ Generated {len(appointments_df)} appointments → {APPOINTMENTS_CSV}")
    
    print("Generating visits...")
    visits_df = generate_visits(appointments_df=appointments_df)
    visits_df.to_csv(VISITS_CSV, index=False)
    print(f"✓ Generated {len(visits_df)} visits → {VISITS_CSV}")
    
    # Print statistics
    print("\n=== Data Statistics ===")
    print(f"Appointments: {len(appointments_df)}")
    print(f"Visits: {len(visits_df)}")
    print(f"Suspicious visits: {visits_df['label_suspicious'].sum()} ({100 * visits_df['label_suspicious'].mean():.1f}%)")
    print(f"Average repeated attempts: {visits_df['repeated_attempts_last_24h'].mean():.2f}")
    print(f"Multi-branch same day: {visits_df['multi_branch_same_day'].sum()} visits")


if __name__ == "__main__":
    main()

