from datetime import date, time
import unittest

from meeting_scheduler import create_meeting_request, format_confirmation


class MeetingSchedulerTests(unittest.TestCase):
    def test_create_meeting_request_normalizes_values(self) -> None:
        meeting_request = create_meeting_request(
            customer_name="  Alex Morgan  ",
            email=" alex@example.com ",
            company=" Metalys Partner ",
            meeting_date=date(2026, 8, 12),
            meeting_time=time(14, 30),
            attendee_count=3,
            discussion_focus=" Manufacturing capabilities ",
            notes="  Review enclosure options.  ",
        )

        self.assertEqual(meeting_request["customer_name"], "Alex Morgan")
        self.assertEqual(meeting_request["email"], "alex@example.com")
        self.assertEqual(meeting_request["company"], "Metalys Partner")
        self.assertEqual(meeting_request["meeting_date"], "2026-08-12")
        self.assertEqual(meeting_request["meeting_time"], "14:30")
        self.assertEqual(meeting_request["discussion_focus"], "Manufacturing capabilities")
        self.assertEqual(meeting_request["notes"], "Review enclosure options.")

    def test_create_meeting_request_requires_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "Customer name is required."):
            create_meeting_request(
                customer_name=" ",
                email="alex@example.com",
                company="Metalys Partner",
                meeting_date=date(2026, 8, 12),
                meeting_time=time(14, 30),
                attendee_count=1,
                discussion_focus="General Commercial Discussion",
            )

    def test_create_meeting_request_requires_email(self) -> None:
        with self.assertRaisesRegex(ValueError, "Email is required."):
            create_meeting_request(
                customer_name="Alex Morgan",
                email=" ",
                company="Metalys Partner",
                meeting_date=date(2026, 8, 12),
                meeting_time=time(14, 30),
                attendee_count=1,
                discussion_focus="General Commercial Discussion",
            )

    def test_create_meeting_request_requires_company(self) -> None:
        with self.assertRaisesRegex(ValueError, "Company is required."):
            create_meeting_request(
                customer_name="Alex Morgan",
                email="alex@example.com",
                company=" ",
                meeting_date=date(2026, 8, 12),
                meeting_time=time(14, 30),
                attendee_count=1,
                discussion_focus="General Commercial Discussion",
            )

    def test_create_meeting_request_requires_positive_attendee_count(self) -> None:
        with self.assertRaisesRegex(ValueError, "Attendee count must be at least 1."):
            create_meeting_request(
                customer_name="Alex Morgan",
                email="alex@example.com",
                company="Metalys Partner",
                meeting_date=date(2026, 8, 12),
                meeting_time=time(14, 30),
                attendee_count=0,
                discussion_focus="General Commercial Discussion",
            )

    def test_create_meeting_request_preserves_blank_notes(self) -> None:
        meeting_request = create_meeting_request(
            customer_name="Alex Morgan",
            email="alex@example.com",
            company="Metalys Partner",
            meeting_date=date(2026, 8, 12),
            meeting_time=time(14, 30),
            attendee_count=1,
            discussion_focus="General Commercial Discussion",
            notes=" ",
        )

        self.assertEqual(meeting_request["notes"], "")

    def test_create_meeting_request_defaults_blank_discussion_focus(self) -> None:
        meeting_request = create_meeting_request(
            customer_name="Alex Morgan",
            email="alex@example.com",
            company="Metalys Partner",
            meeting_date=date(2026, 8, 12),
            meeting_time=time(14, 30),
            attendee_count=1,
            discussion_focus=" ",
        )

        self.assertEqual(meeting_request["discussion_focus"], "Commercial Discussion")

    def test_format_confirmation_includes_scheduling_details(self) -> None:
        confirmation = format_confirmation(
            {
                "customer_name": "Alex Morgan",
                "company": "Metalys Partner",
                "meeting_date": "2026-08-12",
                "meeting_time": "14:30",
            }
        )

        self.assertIn("Alex Morgan", confirmation)
        self.assertIn("Metalys Partner", confirmation)
        self.assertIn("2026-08-12", confirmation)
        self.assertIn("14:30", confirmation)


if __name__ == "__main__":
    unittest.main()
