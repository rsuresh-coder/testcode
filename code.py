from typing import Dict, TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from PIL import Image
import io
 
class GraphState(TypedDict):
    question: Optional[str] 
    search_results: Optional[str] 
    response: Optional[str]

rag_graph = StateGraph(GraphState)
  
def handle_search_node(state):
    question = state.get('question', '').strip()
    #Perform search here 
    return {"search_results": ["Result 1 " + question, "Result 2 " + question] }

def handle_generation_node(state):
    search_results = state.get('search_results')
    generated = ','.join(search_results)
    return {"response": generated}

#Add Nodes
rag_graph.add_node("search", handle_search_node)
rag_graph.add_node("generate", handle_generation_node)

#Add Edges
rag_graph.add_edge('search', "generate")
rag_graph.add_edge('generate', END)

#Set Entry point
rag_graph.set_entry_point("search")

app = rag_graph.compile()

try:
    image_bytes = app.get_graph().draw_mermaid_png()
    image = Image.open(io.BytesIO(image_bytes))
    image.save("graph.png", "PNG")
except Exception as e:
    print(e)
    pass
  
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in app.stream( {"question" : user_input}):
        # print(event.keys(), event.values())
        for val in event.values():
            if 'response' in val.keys():
                print(val['response'])
         
# inputs = {"question": "Hello, good morning"}
# result = app.invoke(inputs)
# print(result)
