"""
Retrieve relevant past project context from ChromaDB vector memory.
Falls back gracefully if no relevant context exists.
"""

from utils.logger import log


def retrieve_memory(query: str) -> str:
    """
    Retrieve relevant past project context using ChromaDB.
    Returns a summary string of matched documents or a fallback message.
    """
    log.info(f"Retrieving memory for project idea: {query}")

    try:
        from memory.vectordb import get_vector_memory
        vm = get_vector_memory()

        if vm.count() == 0:
            log.info("Vector memory is empty — no past context available")
            return "No previous similar projects found."

        results = vm.query(query, n_results=3)

        if not results:
            return "No previous similar projects found."

        # Build a compact context summary from retrieved docs
        context_parts = []
        for r in results:
            context_parts.append(
                f"[{r['id']}]: {r['text'][:500]}"
            )

        context = "\n\n".join(context_parts)
        log.info(f"Memory retrieval complete — {len(results)} documents found")
        return context

    except Exception as e:
        log.warning(f"Memory retrieval failed (non-fatal): {e}")
        return "No previous similar projects found."