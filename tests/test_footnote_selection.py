import unittest

import pandas as pd

from mcmc_visualizer.callbacks import (
    filter_allocations_by_footnote,
    parse_footnote_selection,
    resolve_footnote_selection,
)


class FootnoteSelectionTests(unittest.TestCase):
    def test_parse_footnote_selection_reads_clicked_row(self):
        footnotes_data = [
            {"footnote_number": "5.53", "footnote_text": "First"},
            {"footnote_number": "5.54", "footnote_text": "Second"},
        ]

        self.assertEqual(
            parse_footnote_selection({"row": 1, "column": 0}, footnotes_data),
            "5.54",
        )

    def test_resolve_footnote_selection_toggles_same_footnote_off_and_resets_cell(self):
        footnotes_data = [{"footnote_number": "5.54", "footnote_text": "Second"}]

        self.assertEqual(
            resolve_footnote_selection({"row": 0, "column": 0}, footnotes_data, "5.54"),
            (None, True),
        )

    def test_resolve_footnote_selection_selects_new_footnote_and_resets_cell(self):
        footnotes_data = [{"footnote_number": "5.54", "footnote_text": "Second"}]

        self.assertEqual(
            resolve_footnote_selection({"row": 0, "column": 0}, footnotes_data, None),
            ("5.54", True),
        )

    def test_filter_allocations_by_footnote_keeps_matching_allocations(self):
        df = pd.DataFrame(
            [
                {"service": "Fixed", "footnote_ids": ["5.53", "5.54"]},
                {"service": "Maritime Mobile", "footnote_ids": ["5.55"]},
                {"service": "Mobile", "footnote_ids": []},
            ]
        )

        result = filter_allocations_by_footnote(df, "5.54")

        self.assertEqual(result["service"].tolist(), ["Fixed"])


if __name__ == "__main__":
    unittest.main()
