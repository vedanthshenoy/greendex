#Imports 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()


def explain_image(image_url : str, model : str = "gemini-1.0-pro-vision-latest") -> str:
    """_summary_
    Sole purpose of this function is to verify whether the Gemini vision model is working without any hiccups.
    This function takes in argument image_url and model to generate a description of the given image.

    Args:
        image_url (str): The path, the image is stored in local
        model (str, optional): Gemini models card name. Defaults to "gemini-1.0-pro-vision-latest".

    Returns:
        str: AIMessage content is finally returned by the model. This will have the description of the image
    """    

    ## call the gemini models, here we are going with the latest version of gemini vision pro as mentioned in their documentation
    llm=ChatGoogleGenerativeAI(model= model,
                            verbose=False,
                            temperature=0,
                            google_api_key=os.getenv("GOOGLE_API_KEY"))

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "What's in this image?",
            },  # You can optionally provide text parts
            {"type": "image_url", "image_url": image_url},
        ]
    )

    response = llm.invoke([message])
    return response.content


if __name__ == "__main__":

    #Random image stored in local
    image_url = r"C:\greendex\randomage.jpg"

    resp = explain_image(image_url=image_url)
    print("AIMessage : ",resp)
