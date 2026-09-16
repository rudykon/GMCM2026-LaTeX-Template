"""Extract Attachment 3's logo row without redrawing or resampling its images.

Convert the original .doc to .docx with LibreOffice first, then run:
  python scripts/extract_official_logos.py converted.docx official/logos.pdf
Requires PyMuPDF for asset regeneration only, not for LaTeX compilation.
"""
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pymupdf


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    with ZipFile(args.docx) as source:
        relationships = {
            rel.get("Id"): rel.get("Target")
            for rel in ET.fromstring(source.read("word/_rels/document.xml.rels"))
        }
        root = ET.fromstring(source.read("word/document.xml"))
        first = root.find("w:body/w:p", ns)
        images = []
        for drawing in first.findall(".//wp:inline", ns):
            extent = drawing.find("wp:extent", ns)
            blip = drawing.find(".//a:blip", ns)
            crop = drawing.find(".//a:srcRect", ns)
            images.append((
                source.read("word/" + relationships[blip.get("{" + ns["r"] + "}embed")]),
                float(extent.get("cx")) / 12700,
                float(extent.get("cy")) / 12700,
                {side: max(0, int(crop.get(side, "0"))) / 100000
                 for side in ("l", "t", "r", "b")} if crop is not None else {},
            ))
    if len(images) != 4:
        raise ValueError("Expected the four official cover logos")
    # Whitespace between inline drawings in Attachment 3, in PDF points.
    gaps = (4.75, 8.0, 4.75, 0.0)
    height = max(item[2] for item in images)
    width = sum(item[1] for item in images) + sum(gaps)
    output = pymupdf.open()
    page = output.new_page(width=width, height=height)
    x = 0
    for (data, w, h, crop), gap in zip(images, gaps):
        image_doc = pymupdf.open(stream=data)
        image_pdf = pymupdf.open(stream=image_doc.convert_to_pdf(), filetype="pdf")
        box = image_pdf[0].rect
        clip = pymupdf.Rect(box.width * crop.get("l", 0),
                            box.height * crop.get("t", 0),
                            box.width * (1 - crop.get("r", 0)),
                            box.height * (1 - crop.get("b", 0)))
        page.show_pdf_page(pymupdf.Rect(x, height - h, x + w, height),
                           image_pdf, 0, clip=clip, keep_proportion=False)
        image_pdf.close()
        image_doc.close()
        x += w + gap
    output.set_metadata({"title": "GMCM 2026 official cover logos (Attachment 3)"})
    output.save(args.output, garbage=4, deflate=True)
    print(f"Extracted four original logos: {args.output}")


if __name__ == "__main__":
    main()
