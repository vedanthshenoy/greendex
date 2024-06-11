import sys
import os

# Add the parent directory to the system path for gemini_loader import
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from gemini_loader import explain_image
from pdf_image_extractor import pdf_to_images


def if_pdf_map(pdf_file_path : str)->str:
    """_summary_
        This function kind of like a main function for this particular feature, uses helper function from other files.
        Extract images from the pdf (using the pdf_to_images function), and then get the info from the map in detail from the gemini_loader's explain_image function
    Args:
        pdf_file_path (str): _description_

    Returns:
        str: _description_
    """    


    pdf_to_images(pdf_path=pdf_file_path, output_folder="C:\greendex\images")

    #Prompting the model for explining in detail the map given
    prompt = """ You are expert in Kannada language and a brilliant map analyzer. 
    From the map of a territory given below, figure out what are the labels mentioned in the map.
    Provide details obtaining area numbers and what category that area number belongs to.

    Details : 
    """
    image_explaination = explain_image(image_url=r"C:\greendex\images\page_1.png", prompt=prompt)

    #Optional step mentioned below in case the image is not getting overwritten
    # os.remove(r"C:\greendex\images\page_1.png")
    return image_explaination

if __name__ == "__main__":

    resp = if_pdf_map(pdf_file_path=r"C:\greendex\pdf_ops\sample_pdf.pdf")
    print("Response of the given image map : ",resp)