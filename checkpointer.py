from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.graph import StateGraph

# -------------------------------------------------------------------
# 1. Compile graph with persistence
# -------------------------------------------------------------------

def compile_graph(checkpointer):
    """
    Compiles the LangGraph with a persistent checkpointer.
    """
    return graph_builder.compile(checkpointer=checkpointer)


# -------------------------------------------------------------------
# 2. Database configuration
# -------------------------------------------------------------------

DB_URI = "mongodb://admin:admin@localhost:27017"


# -------------------------------------------------------------------
# 3. Run graph with streaming + memory
# -------------------------------------------------------------------

def run_graph(user_id: str, user_input: str):
    """
    Runs the graph for a specific user with persistent memory.
    """

    config = {
        "configurable": {
            "thread_id": user_id   # <-- USER ID / MEMORY KEY
        }
    }

    initial_state = State({
        "messages": [user_input]
    })

    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph = compile_graph(checkpointer)

        for state in graph.stream(
            initial_state,
            config=config,
            stream_mode="values"
        ):
            state["messages"][-1].pretty_print()


# -------------------------------------------------------------------
# 4. Entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    run_graph(
        user_id="piyush",
        user_input="what is my name?"
    )
