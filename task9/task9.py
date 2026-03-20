from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import subprocess

class State(TypedDict):
    question: str
    context: str
    query: str
    error: str
    result: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def RAG(state: State):
    # RAG to get context, keep rules and facts that match words in the question
    words_to_match = state["question"].replace("?", "").lower().split()
    with open("familyKB.pl", "r") as f:
        lines = [l.strip() for l in f if ":-" in l or any(s in l.lower() for s in words_to_match)]
    return {"context": "\n".join(lines)}

def judge(state: State):
    # function used to judge relevancy
    prompt = f"Is this context enough to answer '{state['question']}'? Context:\n{state['context']}\nAnswer STRICTLY 'yes' or 'no'."
    res = llm.invoke(prompt).content.lower()
    return {"result": "Proceed" if "yes" in res else "Halt"}

def generate(state: State):
    # generation and self refinement
    if state.get("error"):
        prompt = f"Fix this Prolog syntax error step by step. Failed query: {state['query']}. Error: {state['error']}. Reply ONLY with the corrected raw string."
    else:
        prompt = f"Translate to a single Prolog query (lowercase only). Context:\n{state['context']}\nQuestion: {state['question']}\nReply ONLY with the raw string."

    return {"query": llm.invoke(prompt).content.strip().rstrip('.'), "error": ""}

def execute(state: State):
    #subprocess execution
    goal = f"forall({state['query']}, writeln({state['query']}))"
    try:
        res = subprocess.run(["swipl", "-q", "-s", "familyKB.pl", "-g", goal, "-t", "halt"], capture_output=True, text=True, check=True)
        return {"result": res.stdout.strip() or "Unsure / No Match", "error": ""}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr.strip() or "Syntax Error"}

#routing logic   
def route_judge(state: State): 
    return "generate" if state["result"] == "Proceed" else END

def route_execute(state: State): 
    return "generate" if state.get("error") else END

# build the graph
workflow = StateGraph(State)
workflow.add_node("RAG", RAG)
workflow.add_node("judge", judge)
workflow.add_node("generate", generate)
workflow.add_node("execute", execute)

workflow.set_entry_point("RAG")
workflow.add_edge("RAG", "judge")
workflow.add_conditional_edges("judge", route_judge)
workflow.add_edge("generate", "execute")
workflow.add_conditional_edges("execute", route_execute)

app = workflow.compile()

if __name__ == "__main__":
    output = app.invoke({"question": "Is John the grandfather of David?"})
    print(f"Result: {output['result']}")