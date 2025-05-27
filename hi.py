# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pypdf",
#     "pillow",
# ]
# ///

from pathlib import Path
from pypdf import PdfReader, PdfWriter

downloads = Path.home() / "Downloads"
pdf_files = list(downloads.glob("*.pdf"))

for pdf_file in pdf_files:
    reader = PdfReader(str(pdf_file))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Compress images by reducing their quality
    for page in writer.pages:
        for img in page.images:
            img.replace(img.image, quality=90)  # Adjust quality as needed (0-95)

    out_file = pdf_file.with_stem(pdf_file.stem + "_compressed")
    with out_file.open("wb") as f:
        writer.write(f)
