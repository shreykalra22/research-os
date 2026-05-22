import fitz
from pathlib import Path
from typing import List, Dict

from backend.utils.logger import app_logger


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Parse PDF and extract text page by page.
        """

        app_logger.info(f"Starting PDF parsing: {pdf_path}")

        parsed_pages = []

        try:
            pdf_document = fitz.open(pdf_path)

            total_pages = len(pdf_document)

            app_logger.info(f"PDF loaded successfully with {total_pages} pages")

            for page_number in range(total_pages):
                page = pdf_document.load_page(page_number)

                text = page.get_text("text")

                cleaned_text = self.clean_text(text)

                parsed_pages.append(
                    {
                        "page_number": page_number + 1,
                        "text": cleaned_text,
                        "source": Path(pdf_path).name,
                    }
                )

            pdf_document.close()

            app_logger.info("PDF parsing completed successfully")

            return parsed_pages

        except Exception as e:
            app_logger.error(f"PDF parsing failed: {str(e)}")
            raise Exception(f"Failed to parse PDF: {str(e)}")

    def clean_text(self, text: str) -> str:
        """
        Clean extracted text.
        """

        cleaned = text.replace("\\n", " ").strip()

        cleaned = " ".join(cleaned.split())

        return cleaned