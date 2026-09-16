"""Check compiled template outputs; not a full anonymity/content audit."""
from pathlib import Path
import re
import subprocess

from pypdf import PdfReader


def normalized(text):
    return "".join(text.split())


def main():
    root = Path(__file__).resolve().parents[1]

    readers = {name: PdfReader(root / (name + ".pdf"))
               for name in ("main", "anonymous")}
    contents = {}
    for name, reader in readers.items():
        assert not reader.is_encrypted, name + ": unexpected encryption"
        assert not (reader.metadata or {}).get("/Author", ""), (
            name + ": author metadata must remain empty"
        )
        # Poppler resolves Adobe CJK character maps used by XeLaTeX fonts.
        text_pages = subprocess.run(
            ["pdftotext", "-layout", str(root / (name + ".pdf")), "-"],
            check=True, capture_output=True, text=True, encoding="utf-8"
        ).stdout.split("\f")
        if not text_pages[-1].strip():
            text_pages.pop()
        assert len(text_pages) == len(reader.pages)
        contents[name] = []
        for number, page in enumerate(reader.pages, 1):
            assert abs(float(page.mediabox.width) - 595.28) < 1
            assert abs(float(page.mediabox.height) - 841.89) < 1
            text = normalized(text_pages[number - 1])
            assert len(text) > 10, f"{name}: empty page {number}"
            assert "??" not in text, f"{name}: unresolved reference"
            contents[name].append(text)
        log = (root / (name + ".log")).read_text(errors="replace")
        assert "Output written on " + name + "." in log, (
            name + ": current log has no successful output"
        )
        errors = re.findall(
            r"^.*(?:undefined references|Citation .+ undefined|"
            r"Reference .+ undefined|Overfull \\[hv]box|"
            r"Missing character:|LaTeX Error|Package .+ Error|"
            r"Class .+ Error|Emergency stop|No pages of output).*$",
            log, re.MULTILINE
        )
        assert not errors, name + ":\n" + "\n".join(errors)
        biblog = (root / (name + ".blg")).read_text(errors="replace")
        assert "Warning--" not in biblog and "error message" not in biblog, (
            name + ": incomplete bibliography; inspect the .blg file"
        )

    assert len(contents["main"]) == len(contents["anonymous"]) + 1
    assert contents["main"][1:] == contents["anonymous"], (
        "Body pages or numbering differ between the two entry points"
    )
    cover = contents["main"][0]
    for marker in ("第二十三届", "学校", "参赛队号", "队员姓名"):
        assert marker in cover, "Missing official cover field: " + marker
    for marker in ("参赛论文", "选择题号"):
        assert marker not in cover, "Obsolete cover field: " + marker
    anon = "".join(contents["anonymous"])
    for marker in ("请填写学校名称", "请填写参赛队号", "请填写队员"):
        assert marker not in anon, "Cover field leaked: " + marker
    assert contents["anonymous"][0].endswith("1"), (
        "Abstract page should start at page 1"
    )
    for number, page in enumerate(contents["anonymous"], 1):
        assert page.endswith(str(number)), f"Wrong footer on page {number}"
    print("PASS: A4 pages, matching body pages, continuous page numbers,")
    print("      empty author metadata, resolved references, no overflow.")
    print("Pages:", {name: len(r.pages) for name, r in readers.items()})


if __name__ == "__main__":
    main()
