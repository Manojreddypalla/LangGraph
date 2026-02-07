from typeing_extension import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgrapg.graph import StateGraph, START,END

class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:state):
    print("we are inside")
    return{"message":["hello this is chatbot here"]}


def sample(state:state):
    print("inside sample node for nowww")
    return {"message":["sample appended "]}


graph_builder = StateGraph(state)

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sample") 