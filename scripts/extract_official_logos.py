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
                {side: int(crop.get(side, "0")) / 100000
                 for side in ("l", "t", "r", "b")} if crop is not None else {},
            ))
    if len(images) != 4:
        raise ValueError("Expected the four official cover logos")
    # Whitespace between inline drawings in Attachment 3, in PDF points.
    gaps = (4.70, 7.90, 4.70, 0.0)
    height = max(item[2] for item in images)
    width = sum(item[1] for item in images) + sum(gaps)
    output = pymupdf.open()
    page = output.new_page(width=width, height=height)
    x = 0
    for (data, w, h, crop), gap in zip(images, gaps):
        # Word permits negative cropping: it adds space around the source.
        # Use a page as the viewport so positive crops also remain exact.
        left, top, right, bottom = (crop.get(side, 0) for side in ("l", "t", "r", "b"))
        if left + right >= 1 or top + bottom >= 1:
            raise ValueError("Invalid logo crop in the source document")
        source_w, source_h = w / (1 - left - right), h / (1 - top - bottom)
        rect = pymupdf.Rect(-left * source_w, -top * source_h,
                            (1 - left) * source_w, (1 - top) * source_h)
        image_pdf = pymupdf.open()
        viewport = image_pdf.new_page(width=w, height=h)
        if data.startswith(b"\xff\xd8"):
            # Keep the original JPEG bitstream without recompression.
            viewport.insert_image(rect, stream=data, keep_proportion=False)
        else:
            # Embed DeviceRGB pixels directly, avoiding convert_to_pdf's ICC
            # wrapper. The second logo has an entirely opaque alpha channel;
            # omit that redundant mask for PDF viewer compatibility.
            pixmap = pymupdf.Pixmap(data)
            if pixmap.alpha and all(alpha == 255 for alpha in pixmap.samples[pixmap.n - 1::pixmap.n]):
                pixmap = pymupdf.Pixmap(pixmap, 0)
            image_xref = viewport.insert_image(rect, pixmap=pixmap, keep_proportion=False)
            # PyMuPDF may attach its default sRGB ICC profile even to a
            # DeviceRGB pixmap. All three source PNGs are sRGB; express their
            # unchanged RGB samples with the simpler PDF color space.
            if pixmap.colorspace.n != 3:
                raise ValueError("Expected an RGB logo in the source document")
            image_pdf.xref_set_key(image_xref, "ColorSpace", "/DeviceRGB")
        page.show_pdf_page(pymupdf.Rect(x, height - h, x + w, height),
                           image_pdf, 0, keep_proportion=False)
        image_pdf.close()
        x += w + gap
    output.set_metadata({"title": "GMCM 2026 official cover logos (Attachment 3)"})
    output.save(args.output, garbage=4, deflate=True)
    print(f"Extracted four original logos: {args.output}")


if __name__ == "__main__":
    main()
