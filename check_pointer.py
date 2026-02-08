import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

# LangGraph Imports
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.mongodb import MongoDBSaver

# LLM Imports
from langchain_ollama import ChatOllama

# Database Imports
from pymongo import MongoClient

# 1. Setup Environment
load_dotenv()

# 2. Setup MongoDB Connection (The Memory)
# Ensure you have a local Mongo running or replace with your Atlas URI
mongo_client = MongoClient("mongodb://localhost:27017")
checkpointer = MongoDBSaver(mongo_client)

# 3. Setup LLM
llm = ChatOllama(
    model="llama3",
    temperature=0
)

# 4. Define State
class State(TypedDict):
    # 'add_messages' ensures we append to history, not overwrite it
    messages: Annotated[list, add_messages]

# 5. Define Nodes
def chatbot(state: State):
    print("--- 🤖 Chatbot Node Executing ---")
    # Invoke the model with the message history
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def endnode(state: State):
    print("--- 🏁 End Node Reached ---")
    return state

# 6. Build the Graph
builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("endnode", endnode)

# Flow: START -> Chatbot -> EndNode -> END
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", "endnode")
builder.add_edge("endnode", END)

# 7. Compile with Checkpointer (CRITICAL STEP)
# This enables the "Memory" feature
graph = builder.compile(checkpointer=checkpointer)

# 8. Run with Thread ID
# This config object tells Mongo: "Save this conversation under the ID 'admin'"
config = {"configurable": {"thread_id": "admin"}}

print("\n--- 🗣️ Turn 1 ---")
output1 = graph.invoke(
    {"messages": [("user", "Hello, my name is Manoj")]}, 
    config=config
)
print(output1["messages"][-1].content)

print("\n--- 🗣️ Turn 2 (Testing Memory) ---")
# Notice we don't send the name again, but it remembers!
output2 = graph.invoke(
    {"messages": [("user", "What is my name?")]}, 
    config=config
)
print(output2["messages"][-1].content)