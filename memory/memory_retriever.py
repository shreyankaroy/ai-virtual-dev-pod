from utils.logger import log


def retrieve_memory(query: str):
    """
    Retrieve relevant past project context.
    (Placeholder before vector DB integration)
    """

    print("MEMORY FUNCTION CALLED")

    log.info(f"Retrieving memory for project idea: {query}")

    # placeholder response until vector DB is implemented
    context = "No previous similar projects found."

    log.info("Memory retrieval complete")

    return context