from __future__ import annotations

from datetime import date, time


def create_meeting_request(
    *,
    customer_name: str,
    email: str,
    company: str,
    meeting_date: date,
    meeting_time: time,
    attendee_count: int,
    discussion_focus: str,
    notes: str = "",
) -> dict[str, str | int]:
    customer_name = customer_name.strip()
    email = email.strip()
    company = company.strip()
    discussion_focus = discussion_focus.strip()
    notes = notes.strip()

    if not customer_name:
        raise ValueError("Customer name is required.")
    if not email:
        raise ValueError("Email is required.")
    if not company:
        raise ValueError("Company is required.")
    if attendee_count < 1:
        raise ValueError("Attendee count must be at least 1.")

    return {
        "customer_name": customer_name,
        "email": email,
        "company": company,
        "meeting_date": meeting_date.isoformat(),
        "meeting_time": meeting_time.strftime("%H:%M"),
        "attendee_count": attendee_count,
        "discussion_focus": discussion_focus or "Commercial Discussion",
        "notes": notes,
    }


def format_confirmation(meeting_request: dict[str, str | int]) -> str:
    return (
        f"Commercial Discussion scheduled for {meeting_request['customer_name']} "
        f"from {meeting_request['company']} on {meeting_request['meeting_date']} "
        f"at {meeting_request['meeting_time']}."
    )
