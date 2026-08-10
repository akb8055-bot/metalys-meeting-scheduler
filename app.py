from __future__ import annotations

from datetime import date, time

import streamlit as st

from meeting_scheduler import create_meeting_request, format_confirmation


st.set_page_config(
    page_title="Metalys Commercial Discussion Scheduler",
    page_icon="📅",
    layout="centered",
)

st.title("Schedule a Commercial Discussion")
st.subheader("Metalys Enclosures Manufacturing")
st.write(
    "Share your preferred meeting details and our team will use them to plan your "
    "commercial discussion."
)

with st.form("commercial_discussion_scheduler"):
    customer_name = st.text_input("Full name")
    email = st.text_input("Business email")
    company = st.text_input("Company")
    meeting_date = st.date_input("Preferred meeting date", min_value=date.today())
    meeting_time = st.time_input("Preferred meeting time", value=time(hour=10, minute=0))
    attendee_count = st.number_input(
        "Number of attendees",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
    )
    discussion_focus = st.selectbox(
        "Discussion focus",
        (
            "New enclosure project",
            "Pricing and lead times",
            "Manufacturing capabilities",
            "Custom fabrication requirements",
            "General Commercial Discussion",
        ),
    )
    notes = st.text_area("Additional notes", placeholder="Share agenda items or project context.")
    submitted = st.form_submit_button("Schedule meeting")

if submitted:
    try:
        meeting_request = create_meeting_request(
            customer_name=customer_name,
            email=email,
            company=company,
            meeting_date=meeting_date,
            meeting_time=meeting_time,
            attendee_count=int(attendee_count),
            discussion_focus=discussion_focus,
            notes=notes,
        )
    except ValueError as exc:
        st.error(str(exc))
    else:
        st.success(format_confirmation(meeting_request))
        st.markdown("### Request details")
        st.write(
            {
                "Customer": meeting_request["customer_name"],
                "Email": meeting_request["email"],
                "Company": meeting_request["company"],
                "Date": meeting_request["meeting_date"],
                "Time": meeting_request["meeting_time"],
                "Attendees": meeting_request["attendee_count"],
                "Focus": meeting_request["discussion_focus"],
                "Notes": meeting_request["notes"] or "No additional notes provided.",
            }
        )
        st.info(
            "If you need to update your requested time, please submit the form again "
            "with the latest details."
        )
