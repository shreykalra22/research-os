from backend.services.pdf_parser import PDFParser
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator


def main():
    parser = PDFParser()

    parsed_pages = parser.parse_pdf(
        "data/sample_pdfs/AI notes.pdf"
    )

    chunker = TextChunker()

    chunks = chunker.chunk_documents(parsed_pages)

    embedding_generator = EmbeddingGenerator()

    embedded_chunks = embedding_generator.generate_embeddings(
        chunks[:5]
    )

    print("\nEMBEDDING RESULT:\n")

    for item in embedded_chunks[:2]:
        print("CONTENT:")
        print(item["content"][:200])

        print("\nEMBEDDING VECTOR LENGTH:")
        print(len(item["embedding"]))

        print("\nPAGE:")
        print(item["page_number"])

        print("\nSOURCE:")
        print(item["source"])

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()