from backend.services.pdf_parser import PDFParser
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.vector_store import VectorStore
from backend.rag.retriever import Retriever
from backend.rag.prompt_builder import PromptBuilder
from backend.services.llm_service import LLMService


def main():

    parser = PDFParser()

    parsed_pages = parser.parse_pdf(
        "data/sample_pdfs/AI notes.pdf"
    )

    chunker = TextChunker()

    chunks = chunker.chunk_documents(parsed_pages)

    embedding_generator = EmbeddingGenerator()

    embedded_chunks = embedding_generator.generate_embeddings(
        chunks[:50]
    )

    vector_store = VectorStore()

    vector_store.add_documents(
        embedded_chunks
    )

    retriever = Retriever()

    query = "What is Artificial Intelligence?"

    retrieved_docs = retriever.retrieve(query)

    retrieved_contents = [
        doc["content"]
        for doc in retrieved_docs
    ]

    prompt_builder = PromptBuilder()

    prompt = prompt_builder.build_prompt(
        query=query,
        retrieved_chunks=retrieved_contents,
    )

    llm_service = LLMService()

    response = llm_service.generate_response(
        prompt
    )

    print("\nAI RESPONSE:\n")

    print(response)

    print("\n" + "=" * 80 + "\n")

    print("SOURCES:\n")

    for doc in retrieved_docs:

        print(
            f"Page: {doc['page_number']} | Source: {doc['source']}"
        )


if __name__ == "__main__":
    main()