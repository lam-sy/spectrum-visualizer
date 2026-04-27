import unittest

from mcmc_visualizer.callbacks import resolve_allocation_row_selection


class AllocationSelectionTests(unittest.TestCase):
    def test_resolve_allocation_row_selection_selects_row_and_resets_cell(self):
        self.assertEqual(
            resolve_allocation_row_selection({"row": 3, "column": 1}, None),
            (3, True),
        )

    def test_resolve_allocation_row_selection_toggles_same_row_off_and_resets_cell(self):
        self.assertEqual(
            resolve_allocation_row_selection({"row": 3, "column": 1}, 3),
            (None, True),
        )

    def test_resolve_allocation_row_selection_ignores_empty_click(self):
        self.assertEqual(resolve_allocation_row_selection(None, 3), (3, False))


if __name__ == "__main__":
    unittest.main()
