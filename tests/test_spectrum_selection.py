import unittest

from mcmc_visualizer.callbacks import (
    build_spectrum_selection_notice,
    parse_spectrum_click_selection,
    resolve_spectrum_selection,
)


class SpectrumSelectionTests(unittest.TestCase):
    def test_parse_spectrum_click_selection_reads_customdata(self):
        click_data = {
            "points": [
                {
                    "customdata": [100.0, 200.0, "Fixed"],
                }
            ]
        }

        self.assertEqual(
            parse_spectrum_click_selection(click_data),
            {
                "band_start_hz": 100.0,
                "band_end_hz": 200.0,
                "service": "Fixed",
                "curve_number": None,
                "point_number": None,
            },
        )

    def test_resolve_spectrum_selection_clears_when_same_bar_clicked(self):
        current = {
            "band_start_hz": 100.0,
            "band_end_hz": 200.0,
            "service": "Fixed",
            "curve_number": 7,
            "point_number": 0,
        }
        click_data = {
            "points": [
                {
                    "customdata": [100.0, 200.0, "Fixed"],
                    "curveNumber": 7,
                    "pointNumber": 0,
                }
            ]
        }

        self.assertIsNone(
            resolve_spectrum_selection("spectrum-chart", click_data, 0, current)
        )

    def test_resolve_spectrum_selection_keeps_same_service_on_different_bar(self):
        current = {
            "band_start_hz": 100.0,
            "band_end_hz": 200.0,
            "service": "Fixed",
            "curve_number": 7,
            "point_number": 0,
        }
        click_data = {
            "points": [
                {
                    "customdata": [100.0, 200.0, "Fixed"],
                    "curveNumber": 9,
                    "pointNumber": 0,
                }
            ]
        }

        self.assertEqual(
            resolve_spectrum_selection("spectrum-chart", click_data, 0, current),
            {
                "band_start_hz": 100.0,
                "band_end_hz": 200.0,
                "service": "Fixed",
                "curve_number": 9,
                "point_number": 0,
            },
        )

    def test_resolve_spectrum_selection_clears_from_button(self):
        current = {
            "band_start_hz": 100.0,
            "band_end_hz": 200.0,
            "service": "Fixed",
        }

        self.assertIsNone(
            resolve_spectrum_selection("clear-spectrum-selection-btn", None, 1, current)
        )

    def test_build_spectrum_selection_notice_shows_clear_message(self):
        selection = {
            "band_start_hz": 100.0,
            "band_end_hz": 200.0,
            "service": "Fixed",
        }

        message, style = build_spectrum_selection_notice(selection)

        self.assertIn("Spectrum selection active", message)
        self.assertEqual(style["display"], "flex")

    def test_build_spectrum_selection_notice_hides_when_no_selection(self):
        message, style = build_spectrum_selection_notice(None)

        self.assertEqual(message, "")
        self.assertEqual(style["display"], "none")


if __name__ == "__main__":
    unittest.main()
