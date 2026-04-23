import unittest

import pandas as pd

from mcmc_visualizer.layout import create_spectrum_tab
from mcmc_visualizer.spectrum import (
    SPECTRUM_ROW_HEIGHT_PX,
    SPECTRUM_VIEWPORT_HEIGHT_PX,
    build_spectrum_figure,
)


class SpectrumViewportTests(unittest.TestCase):
    def test_build_spectrum_figure_uses_row_height_for_total_height(self):
        df = pd.DataFrame(
            [
                {
                    "band_start_hz": 1.0,
                    "band_end_hz": 2.0,
                    "band_label": "1 Hz - 2 Hz",
                    "service": "Fixed",
                    "status": "primary",
                },
                {
                    "band_start_hz": 1.0,
                    "band_end_hz": 2.0,
                    "band_label": "1 Hz - 2 Hz",
                    "service": "Mobile",
                    "status": "secondary",
                },
                {
                    "band_start_hz": 3.0,
                    "band_end_hz": 4.0,
                    "band_label": "3 Hz - 4 Hz",
                    "service": "Broadcasting",
                    "status": "primary",
                },
            ]
        )

        fig = build_spectrum_figure(df)

        self.assertEqual(fig.layout.height, 2 * SPECTRUM_ROW_HEIGHT_PX)

    def test_spectrum_tab_uses_fixed_scroll_viewport_height(self):
        spectrum_tab = create_spectrum_tab()

        chart_column = spectrum_tab.children[1]
        chart_section = chart_column.children
        chart_wrapper = chart_section.children[1].children
        graph = chart_wrapper.children
        graph_props = graph.to_plotly_json()["props"]

        self.assertEqual(
            chart_wrapper.style["height"],
            f"{SPECTRUM_VIEWPORT_HEIGHT_PX}px",
        )
        self.assertFalse(graph_props["responsive"])


if __name__ == "__main__":
    unittest.main()
