#Imports
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.string import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.utils import ConfigurableFieldSpec
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from operator import itemgetter
from dotenv import load_dotenv
import os

load_dotenv()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

model = ChatGoogleGenerativeAI(model="gemini-pro",
                                temperature=0,
                                google_api_key=os.getenv("GOOGLE_API_KEY"),
                                convert_system_message_to_human=True
                                )

prompt = ChatPromptTemplate.from_messages(
        [
        ("system", "You are an intelligent chatbot assistant for geographical content"),
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human", "{query}"),
    ]

)

# The dictionary which stores all chat history. Kindly don't use in production.
store = {}

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """_summary_
    This class is used as an alternative to ChatMessageHistory class used in the get_session_history function.
    Essentially used to append the messages and clear it if needed.
    Args:
        BaseChatMessageHistory (_type_): Message with history chunks returned by the get_session_history function.
        BaseModel (_type_): Currently not used.
    """    

    messages : List[BaseMessage] = Field(default_factory=list)

    def add_message(self, message: BaseMessage) -> None:
       self.messages.append(message)

    def clear(self) -> None:
        self.messages = []
    

def get_session_history(user_id: str, conversation_id : str) -> BaseChatMessageHistory:
    """_summary_
    Gets the user id and conversation id and loads the memory of the overall chat. 
    Checks if user id and conversation id exists in store, if not, adds it to "store" dictionary
    Args:
        user_id (str): _description_
        conversation_id (str): _description_

    Returns:
        BaseChatMessageHistory: The overall memory chunk from store dictionary 
    """    
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]

chain = RunnablePassthrough.assign(query = itemgetter("query")) | prompt | model | StrOutputParser()

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="chat_history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id = "user_id",
            annotation=str,
            name = "User Id",
            description = "Unique Identifier for User Id",
            default = "",
            is_shared = True
        ),
        ConfigurableFieldSpec(
            id = "conversation_id",
            annotation=str,
            name = "Conversation Id",
            description = "Unique Identifier for Conversation Id",
            default = "",
            is_shared = True
        )

    ]
)


if __name__ == "__main__":

    # Use Ctrl + C to break out of the loop.
    while True:

        resp = conversational_chain.invoke({"query" : input("Ask your question : ")}, {'configurable': {'user_id': 'vedanth', "conversation_id" : "chat_1"}})

        print(resp)

    # Uncomment the below to see the history as well or include it inside the loop.
    # print(store)