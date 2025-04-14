import fitz # PyMuPDF
import os

# Input PDF and output folder setup
pdf_path = "Power-BI-Crash-Course-1644226849.pdf"
output_md = "output.md"
images_dir = "images"

# Create images directory
os.makedirs(images_dir, exist_ok=True)

# Open the PDF
doc = fitz.open(pdf_path)

with open(output_md, "w", encoding="utf-8") as md_file:
    for page_num, page in enumerate(doc, start=1):
        # Extract text
        text = page.get_text("text")
        md_file.write(f"\n## Page {page_num}\n\n{text.strip()}\n")

        # Extract images
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_img_name = f"page{page_num}_img{img_index}.png"
            img_path = os.path.join(images_dir, base_img_name)

            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:
                pix.save(img_path)
            else:
                pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(img_path)

            pix = None

            # Write image reference in markdown
            md_file.write(f"\n![Image Page {page_num} - {img_index}]({images_dir}/{base_img_name})\n")