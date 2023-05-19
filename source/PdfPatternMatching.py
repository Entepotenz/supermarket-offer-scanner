import re
import string
import typing
import unicodedata

import PyPDF2


class PdfPatterMatching:
    @staticmethod
    def run_and_get_results(data_pdf: typing.BinaryIO, regex_patterns: [re]) -> dict:
        texts_grouped_by_page = PdfPatterMatching.get_text_grouped_by_page(data_pdf)
        texts_grouped_by_page = map(
            PdfPatterMatching.normalize_text, texts_grouped_by_page
        )
        texts_grouped_by_page = list(texts_grouped_by_page)

        # check for regex matches on each page and store results grouped by page
        matches_grouped_by_page = {}
        for i in range(len(texts_grouped_by_page)):
            val = texts_grouped_by_page[i]

            matches_for_current_page = PdfPatterMatching.apply_regex_findall(
                val, regex_patterns
            )

            if matches_for_current_page:
                matches_grouped_by_page[i] = matches_for_current_page

        return matches_grouped_by_page

    @staticmethod
    def apply_regex_findall(text: str, regex_patterns: [re]) -> [str]:
        result = []
        for pattern in regex_patterns:
            matches = re.findall(pattern=pattern, string=text, flags=re.IGNORECASE)

            if matches:
                matches = matches[0]
                result.append(matches)

        return result

    @staticmethod
    def get_text_grouped_by_page(data_pdf: typing.BinaryIO) -> [str]:
        pdf_reader = PyPDF2.PdfReader(data_pdf)
        texts_grouped_by_page = []
        for page in range(len(pdf_reader.pages)):
            texts_grouped_by_page.append(pdf_reader.pages[page].extract_text())

        return texts_grouped_by_page

    @staticmethod
    def normalize_text(text: str) -> str:
        text = PdfPatterMatching.remove_non_printable_characters(text)
        text = PdfPatterMatching.normalize_quotation_marks(text)
        text = PdfPatterMatching.remove_hyphens(text)
        return text

    @staticmethod
    def remove_non_printable_characters(input_string: str) -> str:
        printable_chars = set(string.printable)
        return "".join(filter(lambda x: x in printable_chars, input_string))

    @staticmethod
    def remove_hyphens(input_string: str) -> str:
        return input_string.replace("-", "")

    @staticmethod
    def normalize_quotation_marks(input_string: str) -> str:
        normalized_string = unicodedata.normalize("NFKD", input_string)
        return normalized_string
