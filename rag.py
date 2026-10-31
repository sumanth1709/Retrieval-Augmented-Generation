from retrieval.retriever import (
    load_vector_database,
    load_embedding_model,
    create_query_embedding,
    search_similar_chunks,
    get_retrieved_context
)

from generation.generator import generate_answer


def main():

    print("=" * 60)
    print("                    RAG SYSTEM")
    print("=" * 60)

    print()
    print("Loading vector database...")

    collection = load_vector_database()

    print(
        "Vectors available:",
        collection.count()
    )

    print()
    print("Loading embedding model...")

    model = load_embedding_model()

    print()
    print("RAG system is ready!")
    print("Ask a question about your documents.")
    print("Type 'exit' to stop.")

    while True:

        print()

        question = input(
            "Question: "
        ).strip()

        if question.lower() == "exit":

            print()
            print("RAG system stopped.")

            break

        if not question:

            print(
                "Please enter a question."
            )

            continue

        print()
        print("Creating query embedding...")

        query_embedding = create_query_embedding(
            model,
            question
        )

        print(
            "Searching documents..."
        )

        results = search_similar_chunks(
            collection,
            query_embedding,
            question,
            top_k=5
        )

        context = get_retrieved_context(
            results
        )

        print()
        print("=" * 60)
        print("RETRIEVED CONTEXT")
        print("=" * 60)

        if context:

            print(context)

        else:

            print(
                "No relevant context found."
            )

            continue

        print()
        print("=" * 60)
        print("GENERATING ANSWER")
        print("=" * 60)

        answer = generate_answer(
            question,
            context
        )

        if answer:

            print()
            print("=" * 60)
            print("FINAL ANSWER")
            print("=" * 60)

            print(answer)

        else:

            print()
            print(
                "Could not generate an answer."
            )


if __name__ == "__main__":
    main()