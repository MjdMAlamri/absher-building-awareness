// Change this when deploying
const API_BASE = "http://localhost:8000";

async function fetchJSON(path) {
  const res = await fetch(`${API_BASE}${path}`);
  return res.json();
}

async function refresh() {
  try {
    const [
      status,
      alerts,
      snapshot,
      sections,
      actions
    ] = await Promise.all([
      fetchJSON("/building-status"),
      fetchJSON("/alerts"),
      fetchJSON("/snapshot"),
      fetchJSON("/sections"),
      fetchJSON("/suggested-actions")
    ]);

    document.getElementById("entries").textContent = status.total_entries;
    document.getElementById("exits").textContent = status.total_exits;
    document.getElementById("inside").textContent = status.current_inside;

    if (snapshot.image_base64) {
      document.getElementById("liveImage").src =
        "data:image/jpeg;base64," + snapshot.image_base64;
    }

    const table = document.getElementById("sectionsTable");
    table.innerHTML = "";
    sections.sections.forEach(s => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${s.name}</td>
        <td>${s.current}</td>
        <td>${s.peak}</td>
      `;
      table.appendChild(row);
    });

    const alertsList = document.getElementById("alertsList");
    alertsList.innerHTML = "";
    alerts.forEach(a => {
      const li = document.createElement("li");
      li.textContent = a.message;
      alertsList.appendChild(li);
    });

    const actionsList = document.getElementById("actionsList");
    actionsList.innerHTML = "";
    actions.forEach(a => {
      const li = document.createElement("li");
      li.textContent = a;
      actionsList.appendChild(li);
    });

  } catch (err) {
    console.error("Refresh failed", err);
  }
}

setInterval(refresh, 1000);
refresh();