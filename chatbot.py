from typing_extensions import TypedDict
from typing import Annotated, List
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END
from langchain_ollama import ChatOllama
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Literal
import os 

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

llm = ChatOllama(
    model="llama3",
    temperature=0,
    # other params...
)

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:State):
    print("we are inside")
    responce = llm.invoke(state.get("messages"))
    return{"messages":[responce]}


def gemini(state: State):

    print("chatbot_gemini Node", state)
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
        
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
  )
    state["llm_output"] = response.choices[0].message.content
    return state


def evalaute_response(state: State) -> Literal["gemini", "endnode"]:
    print("evalaute_response Node", state)
    if False:
        return "endnode"
    
    return "gemini"

def endnode(state: State):
    print("endnode Node", state)
    return state

def sample(state:State):
    print("inside sample node for nowww")
    return {"message":["sample appended "]}


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sample",sample)
graph_builder.add_node("gemini",gemini)
graph_builder.add_node("endnode", endnode)



graph_builder.add_edge(START,"chatbot")

# graph_builder.add_edge("chatbot","sample")
graph_builder.add_conditional_edges("chatbot",evalaute_response)
graph_builder.add_edge("gemini","endnode")


graph = graph_builder.compile()

update=graph.invoke(State({"messages": ["hello im manoj"]}))
#update=graph.invoke(State({"messages": ["manoj"]}))


print("updated",update)

