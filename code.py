from vertexai.preview import reasoning_engines
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import END, MessageGraph
from langchain_core.tools import tool   
from langgraph.prebuilt import ToolNode
from typing import Literal, List    

PROJECT_ID = "gen-lang-client-0259041665"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}
# STAGING_BUCKET = "gs://gen_ai_bucket_hyd"  # @param {type:"string"}
 
# vertexai.init(project=PROJECT_ID, location=LOCATION) 
#, staging_bucket=STAGING_BUCKET)
 

def get_product_details(product_name: str):
    """Gathers basic details about a product."""
    print("Returning details for ", product_name)
    details = {
        "smartphone": "A cutting-edge smartphone with advanced camera features and lightning-fast processing.",
        "coffee": "A rich, aromatic blend of ethically sourced coffee beans.",
        "shoes": "High-performance running shoes designed for comfort, support, and speed.",
        "headphones": "Wireless headphones with advanced noise cancellation technology for immersive audio.",
        "speaker": "A voice-controlled smart speaker that plays music, sets alarms, and controls smart home devices.",
    }
    return details.get(product_name, "Product details not found.")

@tool
def lookup_policy(query: str) -> str:
    """Provides information about banking related, card related questions."""
    # print("Received LP: ", query)
    # docs = retriever.query(query, k=2)
    # return "\n\n".join([doc["page_content"] for doc in docs])
    return query



def router(state: List[BaseMessage]) -> Literal["get_product_details", "__end__"]:
    """Initiates product details retrieval if the user asks for a product."""
    # Get the tool_calls from the last message in the conversation history.
    tool_calls = state[-1].tool_calls
    # If there are any tool_calls
    if len(tool_calls):
        # print(tool_calls)
        # Return the name of the tool to be called
        return "get_product_details"
    else:
        # End the conversation flow.
        return "__end__"

class SimpleLangGraphApp:
    def __init__(self, project: str, location: str) -> None:
        self.project_id = project
        self.location = location

    # The set_up method is used to define application initialization logic
    def set_up(self) -> None:
        model = ChatVertexAI(model="gemini-1.5-pro")

        builder = MessageGraph()

        model_with_tools = model.bind_tools([  get_product_details])
        builder.add_node("tools", model_with_tools)

        tool_node = ToolNode([get_product_details])
        builder.add_node("get_product_details", tool_node)
        builder.add_edge("get_product_details", END)

        # tool2_node = ToolNode([lookup_policy])
        # builder.add_node("lookup_policy", tool2_node)
        # builder.add_edge("lookup_policy", END)
 
        builder.set_entry_point("tools")
        builder.add_conditional_edges("tools", router)

        self.runnable = builder.compile()

    # The query method will be used to send inputs to the agent
    def query(self, message: str):
        """Query the application.

        Args:
            message: The user message.

        Returns:
            str: The LLM response.
        """
        chat_history = self.runnable.invoke(HumanMessage(message))
        # print(chat_history)

        return chat_history[-1].content

agent = SimpleLangGraphApp(project=PROJECT_ID, location=LOCATION)
agent.set_up()

print(agent.query(message="tell me about product shoes"))
# print(agent.query(message="When will i receive my first billing statement?"))


# print(agent.query(message="tell me about the weather"))
