import re
import typing

import PyPDF2


class PdfPatterMatching:
    @staticmethod
    def run_and_get_results(data_pdf: typing.BinaryIO, regex_patterns: [re]) -> list:
        pdf_reader = PyPDF2.PdfReader(data_pdf)

        # extract text from PDF pages and group it by page
        texts_grouped_by_page = []
        for page in range(len(pdf_reader.pages)):
            texts_grouped_by_page.append(pdf_reader.pages[page].extract_text())

        # check for regex matches on each page and store results grouped by page
        matches_grouped_by_page = []
        for val in texts_grouped_by_page:
            matches_for_current_page = []
            for pattern in regex_patterns:
                matches = re.findall(pattern, val, flags=re.IGNORECASE)
                if matches:
                    matches_for_current_page.append(matches)

            matches_grouped_by_page.append(matches_for_current_page)

        return matches_grouped_by_page
