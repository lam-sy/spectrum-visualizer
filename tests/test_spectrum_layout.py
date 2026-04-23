import unittest

from mcmc_visualizer.layout import (
    ALLOCATION_SECTION_HEADER_STYLE,
    ALLOCATION_SECTION_STYLE,
    create_spectrum_sidebar,
    create_spectrum_tab,
)


class SpectrumLayoutTests(unittest.TestCase):
    def test_spectrum_sidebar_uses_shared_section_wrappers(self):
        sidebar = create_spectrum_sidebar()

        self.assertEqual(len(sidebar.children), 2)

        for section in sidebar.children:
            section_props = section.to_plotly_json()["props"]
            header = section.children[0]

            self.assertEqual(section_props["style"], ALLOCATION_SECTION_STYLE)
            self.assertEqual(header.to_plotly_json()["props"]["style"], ALLOCATION_SECTION_HEADER_STYLE)

    def test_spectrum_chart_and_legend_use_shared_section_wrappers(self):
        tab = create_spectrum_tab()
        chart_column = tab.children[1]
        legend_column = tab.children[2]

        for column in (chart_column, legend_column):
            section = column.children
            section_props = section.to_plotly_json()["props"]
            header = section.children[0]

            self.assertEqual(section_props["style"], ALLOCATION_SECTION_STYLE)
            self.assertEqual(header.to_plotly_json()["props"]["style"], ALLOCATION_SECTION_HEADER_STYLE)


if __name__ == "__main__":
    unittest.main()
