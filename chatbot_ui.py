""" Use the command 'mesop chatbot_ui.py' to run the file 
"""
# Imports
import mesop as me
import mesop.labs as mel

# Import the backend chat module (conversation_chain)
from basic_chatbot import conversational_chain


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  #path="/chat",
  title="Mesop Demo Chat",
)
def page():
    """_summary_
        Allows the mesop to use the transform function and bind it with the chat funtionality
    """  
    mel.chat(transform, title="Greendex Chat", bot_user="Mesop Bot")


def transform(input: str,  history: list[mel.ChatMessage]) -> str:
    """_summary_
        This function actually invokes the basic_chatbot (backend) functionality everytime the user needs to query.
        The history feature is currently not used explicitely and handled via backend itself.
    Args:
        input (str): Query provided by the user
        The history parameter is currently not used but since it needs tewaking in the meso chat.py dependency, 
        we've decided to keep it as it is and just not use it in the function.
    Returns:
        str: The response variable is the answer for given query.
    """  
    response = conversational_chain.invoke({"query" : input}, {'configurable': {'user_id': 'vedanth', "conversation_id" : "chat_1"}})
    return response