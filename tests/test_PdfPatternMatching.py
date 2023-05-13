import os
import sys
import unittest
from io import BytesIO

from hamcrest import assert_that, contains_inanyorder, has_length

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source"))
)

from source import PdfPatternMatching


class TestPdfPatternMatching(unittest.TestCase):
    sample_pdf_filepath = (
        f"{os.path.dirname(os.path.realpath(__file__))}/resources/sample.pdf"
    )

    def test_run_and_get_results(self):
        with open(self.sample_pdf_filepath, "rb") as fh:
            buf = BytesIO(fh.read())

        regex_for_finding_ip_address = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        test_string_but_lowercase = "THIS_IS_A_TEST_STRING".lower()

        regex_collection = [regex_for_finding_ip_address, test_string_but_lowercase]

        result = PdfPatternMatching.PdfPatterMatching.run_and_get_results(
            buf, regex_collection
        )
        assert_that(result, has_length(2))
        assert_that(result.get(0), has_length(2))
        assert_that(
            result.get(0),
            contains_inanyorder(*[test_string_but_lowercase.upper(), "127.0.0.1"]),
        )

        assert_that(result.get(2), has_length(1))
        assert_that(
            result.get(2),
            contains_inanyorder(*[test_string_but_lowercase.lower()]),
        )


if __name__ == "__main__":
    unittest.main()
