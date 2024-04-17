from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def _convert_images_to_pdf(image_paths, pdf_filename,texts):
    # Create a new PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    text_size = 15
    for image_path,text in zip(image_paths,texts):
        # Open the image
        for string,count in zip(text[::-1],range(len(text))):
            c.setFont("Helvetica", text_size)
            x = 10
            y = 10
            text_spacing = 5
            offset = (count)*(text_size+text_spacing)
            c.drawString(x, y+offset, string)
        img = Image.open(image_path)

        # Get the image size
        width, height = img.size

        # Add a new page to the PDF based on the image size
        c.setPageSize((width, height))
        c.showPage()

        # Draw the image on the PDF
        c.drawInlineImage(image_path, 0, 0, width, height)

     # Add title on the first page
    

    # Save th
    c.save()

def generate(image_paths, pdf_filename,texts):
    """Texts argument should be the same size as image paths.
    ex.texts= [['Page1Text1','Page1Text2'],['Page2Text1']]"""
    _convert_images_to_pdf(image_paths, pdf_filename, texts)