import unittest

from mcmc_visualizer.layout import (
    ALLOCATION_SECTION_HEADER_STYLE,
    ALLOCATION_SECTION_STYLE,
    create_allocation_sidebar,
    create_allocation_tab,
)


class AllocationLayoutTests(unittest.TestCase):
    def test_allocation_sidebar_uses_section_wrappers(self):
        sidebar = create_allocation_sidebar()

        self.assertEqual(len(sidebar.children), 3)

        for section in sidebar.children:
            section_props = section.to_plotly_json()["props"]
            header = section.children[0]

            self.assertEqual(section_props["style"], ALLOCATION_SECTION_STYLE)
            self.assertEqual(header.to_plotly_json()["props"]["style"], ALLOCATION_SECTION_HEADER_STYLE)

    def test_allocation_tab_right_column_uses_consistent_sections(self):
        tab = create_allocation_tab()
        row = tab.children[1]
        right_column = row.children[1]

        self.assertEqual(len(right_column.children), 3)

        for section in right_column.children:
            section_props = section.to_plotly_json()["props"]
            header = section.children[0]

            self.assertEqual(section_props["style"], ALLOCATION_SECTION_STYLE)
            self.assertEqual(header.to_plotly_json()["props"]["style"], ALLOCATION_SECTION_HEADER_STYLE)


if __name__ == "__main__":
    unittest.main()
