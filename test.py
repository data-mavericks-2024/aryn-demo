import fitz # PyMuPDF
import os

def extract_images_and_text_to_md(pdf_path, output_folder, markdown_file,
                                   min_width=10, min_height=10, min_size_bytes=1000):
    doc = fitz.open(pdf_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    md_lines = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        page_text = page.get_text().strip()

        md_lines.append(f"## Page {page_index + 1}")
        md_lines.append("")
        if page_text:
            md_lines.append("**Text:**")
            md_lines.append("")
            md_lines.append(page_text)
            md_lines.append("")

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            width = base_image["width"]
            height = base_image["height"]

            if len(image_bytes) < min_size_bytes or width < min_width or height < min_height:
                continue

            image_filename = f"page{page_index + 1}_img{img_index + 1}.{ext}"
            image_path = os.path.join(output_folder, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            md_lines.append(f"**Image {img_index + 1}:**")
            md_lines.append(f"![{image_filename}](images/{image_filename})")
            md_lines.append("")

        md_lines.append("---\n")

    with open(markdown_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"✅ Markdown with text and images saved to: {markdown_file}")


# Example usage
extract_images_and_text_to_md(
    pdf_path="Power-BI-Crash-Course-1644226849.pdf",
    output_folder="images",
    markdown_file="output.md",
    min_width=10,
    min_height=10,
    min_size_bytes=1000
)
