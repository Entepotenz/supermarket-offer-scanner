import logging
import os
import sys
import unittest
from io import BytesIO

from hamcrest import assert_that, contains_inanyorder, has_length

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source"))
)

from source import PdfPatternMatching  # noqa: disable=E402

logger = logging.getLogger(__name__)


class TestPdfPatternMatching(unittest.TestCase):
    sample_pdf_filepath = (
        f"{os.path.dirname(os.path.realpath(__file__))}/resources/sample.pdf"
    )

    def test_run_and_get_results(self):
        with open(self.sample_pdf_filepath, "rb") as fh:
            buf = BytesIO(fh.read())

        regex_for_finding_ip_address = "\d{1,3} \d{1,3} \d{1,3} \d{1,3}"
        test_string_but_lowercase = "THIS IS A TEST STRING".lower()

        regex_collection = [regex_for_finding_ip_address, test_string_but_lowercase]

        result = PdfPatternMatching.PdfPatterMatching.run_and_get_results(
            buf, regex_collection
        )
        assert_that(result, has_length(2))
        assert_that(result.get(0), has_length(2))
        assert_that(
            result.get(0),
            contains_inanyorder(*[test_string_but_lowercase.upper(), "127 0 0 1"]),
        )

        assert_that(result.get(2), has_length(1))
        assert_that(
            result.get(2),
            contains_inanyorder(*[test_string_but_lowercase.lower()]),
        )

    def test_run_and_get_results_string_normalization(self):
        with open(self.sample_pdf_filepath, "rb") as fh:
            buf = BytesIO(fh.read())

        regex_for_string_with_spaces = "THIS\s+IS\s+A\s+TEST\s+STRING\s+WITH\s+SPACES"

        regex_for_string_with_hyphens = "THIS-IS-A-TEST-STRING-WITH-HYPHENS".replace(
            "-", ""
        )

        regex_for_string_with_line_breaks = "THIS IS A TESTWITH LINE BREAKS"

        regex_collection = [
            regex_for_string_with_spaces,
            regex_for_string_with_hyphens,
            regex_for_string_with_line_breaks,
        ]

        result = PdfPatternMatching.PdfPatterMatching.run_and_get_results(
            buf, regex_collection
        )
        assert_that(result, has_length(1))
        assert_that(result.get(0), has_length(3))
        assert_that(
            result.get(0),
            contains_inanyorder(
                *[
                    regex_for_string_with_spaces.replace("\s+", " "),
                    regex_for_string_with_hyphens,
                    regex_for_string_with_line_breaks,
                ]
            ),
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s %(levelname)s %(message)s"
    )
    unittest.main()
