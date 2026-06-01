"""
Tests for README.md structural changes introduced in PR:
- Recent Activity section with <!--START_SECTION:activity--> / <!--END_SECTION:activity--> markers
- Weekly Development Breakdown section with <!--START_SECTION:waka--> / <!--END_SECTION:waka--> markers
- Both sections wrapped in a <div align="center"> element
"""

import os
import re
import unittest

README_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")


def read_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestReadmeActivitySection(unittest.TestCase):
    """Tests for the Recent Activity section added in the PR."""

    def setUp(self):
        self.content = read_readme()

    def test_activity_start_marker_present(self):
        self.assertIn("<!--START_SECTION:activity-->", self.content)

    def test_activity_end_marker_present(self):
        self.assertIn("<!--END_SECTION:activity-->", self.content)

    def test_activity_start_marker_before_end_marker(self):
        start = self.content.index("<!--START_SECTION:activity-->")
        end = self.content.index("<!--END_SECTION:activity-->")
        self.assertLess(start, end)

    def test_activity_section_heading_present(self):
        self.assertIn("## ⚡ Recent Activity", self.content)

    def test_activity_heading_before_start_marker(self):
        heading_pos = self.content.index("## ⚡ Recent Activity")
        start_pos = self.content.index("<!--START_SECTION:activity-->")
        self.assertLess(heading_pos, start_pos)

    def test_activity_markers_exact_format(self):
        # Markers must not have extra whitespace inside the comment tags
        self.assertRegex(self.content, r"<!--START_SECTION:activity-->")
        self.assertRegex(self.content, r"<!--END_SECTION:activity-->")

    def test_activity_start_marker_appears_once(self):
        self.assertEqual(self.content.count("<!--START_SECTION:activity-->"), 1)

    def test_activity_end_marker_appears_once(self):
        self.assertEqual(self.content.count("<!--END_SECTION:activity-->"), 1)


class TestReadmeWakaSection(unittest.TestCase):
    """Tests for the Weekly Development Breakdown (WakaTime) section added in the PR."""

    def setUp(self):
        self.content = read_readme()

    def test_waka_start_marker_present(self):
        self.assertIn("<!--START_SECTION:waka-->", self.content)

    def test_waka_end_marker_present(self):
        self.assertIn("<!--END_SECTION:waka-->", self.content)

    def test_waka_start_marker_before_end_marker(self):
        start = self.content.index("<!--START_SECTION:waka-->")
        end = self.content.index("<!--END_SECTION:waka-->")
        self.assertLess(start, end)

    def test_waka_section_heading_present(self):
        self.assertIn("## 📊 Weekly Development Breakdown", self.content)

    def test_waka_heading_before_start_marker(self):
        heading_pos = self.content.index("## 📊 Weekly Development Breakdown")
        start_pos = self.content.index("<!--START_SECTION:waka-->")
        self.assertLess(heading_pos, start_pos)

    def test_waka_markers_exact_format(self):
        self.assertRegex(self.content, r"<!--START_SECTION:waka-->")
        self.assertRegex(self.content, r"<!--END_SECTION:waka-->")

    def test_waka_start_marker_appears_once(self):
        self.assertEqual(self.content.count("<!--START_SECTION:waka-->"), 1)

    def test_waka_end_marker_appears_once(self):
        self.assertEqual(self.content.count("<!--END_SECTION:waka-->"), 1)


class TestReadmeDivWrapper(unittest.TestCase):
    """Tests for the center-aligned div wrapper enclosing both new sections."""

    def setUp(self):
        self.content = read_readme()

    def test_center_div_present(self):
        self.assertIn('<div align="center">', self.content)

    def test_center_div_closed(self):
        self.assertIn("</div>", self.content)

    def test_div_opens_before_activity_section(self):
        div_pos = self.content.index('<div align="center">')
        activity_pos = self.content.index("<!--START_SECTION:activity-->")
        self.assertLess(div_pos, activity_pos)

    def test_div_opens_before_waka_section(self):
        div_pos = self.content.index('<div align="center">')
        waka_pos = self.content.index("<!--START_SECTION:waka-->")
        self.assertLess(div_pos, waka_pos)

    def test_div_closes_after_activity_section(self):
        activity_end = self.content.index("<!--END_SECTION:activity-->")
        div_close = self.content.rindex("</div>")
        self.assertLess(activity_end, div_close)

    def test_div_closes_after_waka_section(self):
        waka_end = self.content.index("<!--END_SECTION:waka-->")
        div_close = self.content.rindex("</div>")
        self.assertLess(waka_end, div_close)

    def test_activity_section_inside_div(self):
        div_open = self.content.index('<div align="center">')
        div_close = self.content.rindex("</div>")
        activity_start = self.content.index("<!--START_SECTION:activity-->")
        activity_end = self.content.index("<!--END_SECTION:activity-->")
        self.assertGreater(activity_start, div_open)
        self.assertLess(activity_end, div_close)

    def test_waka_section_inside_div(self):
        div_open = self.content.index('<div align="center">')
        div_close = self.content.rindex("</div>")
        waka_start = self.content.index("<!--START_SECTION:waka-->")
        waka_end = self.content.index("<!--END_SECTION:waka-->")
        self.assertGreater(waka_start, div_open)
        self.assertLess(waka_end, div_close)


class TestReadmeSectionOrder(unittest.TestCase):
    """Tests verifying the correct relative ordering of both new sections."""

    def setUp(self):
        self.content = read_readme()

    def test_activity_section_comes_before_waka_section(self):
        activity_heading = self.content.index("## ⚡ Recent Activity")
        waka_heading = self.content.index("## 📊 Weekly Development Breakdown")
        self.assertLess(activity_heading, waka_heading)

    def test_activity_end_marker_before_waka_start_marker(self):
        activity_end = self.content.index("<!--END_SECTION:activity-->")
        waka_start = self.content.index("<!--START_SECTION:waka-->")
        self.assertLess(activity_end, waka_start)

    def test_br_tag_between_sections(self):
        activity_end = self.content.index("<!--END_SECTION:activity-->")
        waka_heading = self.content.index("## 📊 Weekly Development Breakdown")
        between = self.content[activity_end:waka_heading]
        self.assertIn("<br>", between)

    def test_both_sections_present_together(self):
        # Regression: both sections must coexist — neither was accidentally removed
        for marker in [
            "<!--START_SECTION:activity-->",
            "<!--END_SECTION:activity-->",
            "<!--START_SECTION:waka-->",
            "<!--END_SECTION:waka-->",
        ]:
            self.assertIn(marker, self.content, f"Missing marker: {marker}")

    def test_no_stray_section_markers(self):
        # Exactly one pair of markers for each section — no duplicates or mismatches
        self.assertEqual(self.content.count("START_SECTION:activity"), 1)
        self.assertEqual(self.content.count("END_SECTION:activity"), 1)
        self.assertEqual(self.content.count("START_SECTION:waka"), 1)
        self.assertEqual(self.content.count("END_SECTION:waka"), 1)


if __name__ == "__main__":
    unittest.main()
