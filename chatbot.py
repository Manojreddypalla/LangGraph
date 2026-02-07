from typing_extensions import TypedDict
from typing import Annotated, List
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3",
    temperature=0,
    # other params...
)



class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:State):
    print("we are inside")
    responce = llm.invoke(state.get("messages"))
    return{"messages":[responce]}


def sample(state:State):
    print("inside sample node for nowww")
    return {"message":["sample appended "]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sample",sample)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sample")


graph = graph_builder.compile()

update=graph.invoke(State({"messages": ["hello im manoj"]}))
#update=graph.invoke(State({"messages": ["manoj"]}))


print("updated",update)

