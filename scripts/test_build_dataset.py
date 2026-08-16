import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("build_dataset.py")
SPEC = importlib.util.spec_from_file_location("build_dataset", SCRIPT)
build_dataset = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(build_dataset)


class ParserTests(unittest.TestCase):
    def test_bold_body_text_is_not_a_field_boundary(self) -> None:
        source = (
            "**Standard Hours per Week** 19\n"
            "**Job Summary**\n**Please read this first.**\nFull summary.\n"
            "**Responsibilities**\n+ First duty"
        )
        fields = build_dataset.parse_fields(source)
        self.assertEqual(fields["Job Summary"], "Please read this first.\nFull summary.")
        self.assertEqual(fields["Responsibilities"], "- First duty")

    def test_hours_range_uses_lower_bound(self) -> None:
        self.assertEqual(build_dataset.parse_hours("0-19"), (0.0, 19.0))
        self.assertEqual(build_dataset.parse_hours("15"), (15.0, 15.0))
        self.assertEqual(build_dataset.parse_hours("Up to 10 hours"), (0.0, 10.0))

    def test_close_date_is_inclusive(self) -> None:
        target = build_dataset.date(2026, 8, 20)
        self.assertTrue(build_dataset.available_on(None, target, target))
        self.assertFalse(build_dataset.available_on(None, build_dataset.date(2026, 8, 19), target))

    def test_food_handler_mojibake_apostrophe_is_detected(self) -> None:
        status, _ = build_dataset.requirement_status("Current Food Handler��s Permit within one month", "food")
        self.assertNotEqual(status, "未发现明确要求")

    def test_shared_additional_information_is_stripped(self) -> None:
        source = (
            "Real special instruction.\n\nAdditional Information\n\n"
            "The University is a participating employer with Utah Retirement Systems (URS). More text."
        )
        self.assertEqual(build_dataset.strip_shared_additional_information(source), "Real special instruction.")

    def test_shared_additional_information_zh_is_stripped(self) -> None:
        source = "真实申请说明。\n\n补充信息\n\n大学是犹他州退休系统（“URS”）的参与雇主。"
        self.assertEqual(build_dataset.strip_shared_additional_information_zh(source), "真实申请说明。")


if __name__ == "__main__":
    unittest.main()
