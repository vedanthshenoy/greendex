import fitz  # PyMuPDF
from PIL import Image

def pdf_to_images(pdf_path : str, output_folder : str = r"C:\greendex\images"):
    """_summary_
        Purpose of this function is to convert the pdf to images as the pdf reader might not be a best choice in analyzing a 
        map like structure, as it contains more of a spatial information than linearly coded text information. 
        Although, do feel free to use PDFReader or some other modules including modules from langchain pdf readers to obtain 
        information from the pdf.
    Args:
        pdf_path (str): The pdf path after downloading from the landrecords revenue maps website
        output_folder (str): Output folder path where the images need to be stored
    """    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)
        
        # Get the page dimensions and create a blank image
        pix = page.get_pixmap()
        
        # Convert to PIL image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save the image
        img_path = f"{output_folder}/page_{page_number + 1}.png"
        img.save(img_path, "PNG")
        print(f"Saved {img_path}")

# Example usage

if __name__ == "__main__":

    pdf_path = r"C:\greendex\pdf_ops\sample_pdf.pdf"
    output_folder = r"C:\greendex\images"
    pdf_to_images(pdf_path, output_folder)
