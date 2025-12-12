"""
section statistics and summaries
preserves original logic for avg wait approximation and busiest section
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class SectionStatus(BaseModel):
    name: str
    current_count: int
    avg_wait_min: float
    peak_occupancy: int


class SectionSummary(BaseModel):
    busiest_section: Optional[str]
    sections: List[SectionStatus]


class SuggestedActions(BaseModel):
    actions: List[str]


class SectionStatistics:
    def __init__(self, state_store) -> None:
        self.state = state_store
        self.SECTION_WAIT_WINDOW_SEC = 5 * 60

        def build_section_summary(self, now: float) -> SectionSummary:
        sections_state = self.state.sections
        section_status_list: List[SectionStatus] = []
        busiest = None
        busiest_count = -1

        for name, s in sections_state.items():
            events = s.get("enter_events", [])
            if not events:
                avg_wait = 0.0
            else:
                avg_wait = self.SECTION_WAIT_WINDOW_SEC / 120.0  # ~2.5 min

            section_status_list.append(SectionStatus(
                name=name,
                current_count=s.get("current_count", 0),
                avg_wait_min=round(avg_wait, 1),
                peak_occupancy=s.get("peak", 0)
            ))

            if s.get("current_count", 0) > busiest_count:
                busiest_count = s["current_count"]
                busiest = name

        return SectionSummary(
            busiest_section=busiest,
            sections=section_status_list
        )

    def build_suggested_actions(self, summary: SectionSummary) -> SuggestedActions:
        actions: List[str] = []
        for s in summary.sections:
            if s.name.startswith("Desk") and s.current_count >= 5:
                actions.append(f"نقترح نقل موظف من قسم آخر لمساندة {s.name} لتقليل وقت الانتظار.")
            if s.name == "Waiting Area" and s.current_count >= 8:
                actions.append("منطقة الانتظار مزدحمة، يُفضّل فتح مسار إضافي أو توجيه الزوار للأقسام الأقل ازدحامًا.")
            if s.name == "Entrance" and s.current_count >= 5:
                actions.append("يوجد ضغط عند المدخل؛ يُفضّل تخصيص موظف للاستقبال السريع وتنظيم حركة الدخول.")
            if s.name == "Exit" and s.current_count >= 5:
                actions.append("حركة الخروج عالية؛ تأكد من انسيابية الممرات وعدم وجود عوائق.")
        if not actions:
            actions.append("الوضع مستقر، لا توجد إجراءات عاجلة حاليًا.")
        return SuggestedActions(actions=actions)

