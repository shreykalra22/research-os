from backend.services.pdf_parser import PDFParser
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.vector_store import VectorStore


def main():

    parser = PDFParser()

    parsed_pages = parser.parse_pdf(
        "data/sample_pdfs/AI notes.pdf"
    )

    chunker = TextChunker()

    chunks = chunker.chunk_documents(parsed_pages)

    embedding_generator = EmbeddingGenerator()

    embedded_chunks = embedding_generator.generate_embeddings(
        chunks[:20]
    )

    vector_store = VectorStore()

    vector_store.add_documents(
        embedded_chunks
    )

    print("\nDOCUMENTS STORED SUCCESSFULLY\n")

    sample_query = "What is artificial intelligence?"

    query_embedding = embedding_generator.model.encode(
        sample_query
    ).tolist()

    results = vector_store.similarity_search(
        query_embedding=query_embedding,
        top_k=3,
    )

    print("\nSEMANTIC SEARCH RESULTS:\n")

    for idx, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][idx]

        print(f"RESULT {idx + 1}")
        print("\nCONTENT:")
        print(document[:300])

        print("\nPAGE:")
        print(metadata["page_number"])

        print("\nSOURCE:")
        print(metadata["source"])

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()