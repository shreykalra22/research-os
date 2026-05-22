from backend.services.pdf_parser import PDFParser
from backend.rag.chunking import TextChunker


def main():
    parser = PDFParser()

    parsed_pages = parser.parse_pdf(
        "data/sample_pdfs/AI notes.pdf"
    )

    chunker = TextChunker()

    chunks = chunker.chunk_documents(parsed_pages)

    print("\nCHUNKING RESULT:\n")

    for chunk in chunks[:5]:
        print(chunk)
        print("\n" + "=" * 80 + "\n")

    print(f"\nTotal chunks created: {len(chunks)}")


if __name__ == "__main__":
    main()