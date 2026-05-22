from backend.services.pdf_parser import PDFParser


def main():
    parser = PDFParser()

    result = parser.parse_pdf(
        "data/sample_pdfs/AI notes.pdf"
    )

    print("\nPDF PARSING RESULT:\n")

    for page in result[:2]:
        print(page)
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()