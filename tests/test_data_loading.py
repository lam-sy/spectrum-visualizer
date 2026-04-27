import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mcmc_visualizer.data import load_allocations


class DataLoadingTests(unittest.TestCase):
    def test_missing_required_json_raises_actionable_error(self):
        with TemporaryDirectory() as tmpdir:
            missing_file = Path(tmpdir) / "footnotes_by_service.json"

            with self.assertRaisesRegex(
                FileNotFoundError,
                "Required data file is missing.*footnotes_by_service.json.*data/",
            ):
                load_allocations(missing_file)


if __name__ == "__main__":
    unittest.main()
