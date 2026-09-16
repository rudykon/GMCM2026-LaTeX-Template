"""Compile isolated fixtures for the official cover and front-matter limits.

Requires XeLaTeX, pypdf and Poppler's pdftotext, like check_build.py.  All
fixture outputs stay in a temporary directory; the example PDFs are untouched.
"""
from pathlib import Path
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
IDENTITIES = ("测试大学", "GMCM-TEST-TEAM", "甲甲甲", "乙乙乙", "丙丙丙")
SHORT_TITLE = "回归测试论文题目"
SHORT_ABSTRACT = r"""
ABSTRACTBEGINMARKER。用于检查摘要与正文之间的分页及页码。
\keywords{版式检查；连续页码}
ABSTRACTENDMARKER
"""


def normalized(text):
    return "".join(text.split())


def document(options="anonymous", title=SHORT_TITLE,
             abstract=SHORT_ABSTRACT, cover_pdf=None, fontset="fandol"):
    cover_setup = (r"\gmcmsetup{cover-pdf={" + str(cover_pdf) + "}}"
                   if cover_pdf else "")
    if fontset:
        options = "fontset=" + fontset + "," + options
    return (
        r"\documentclass[" + options + r"]{gmcm2026}" + "\n"
        r"\gmcmsetup{title={" + title + r"},school={" + IDENTITIES[0]
        + r"},team={" + IDENTITIES[1] + r"},member-a={" + IDENTITIES[2]
        + r"},member-b={" + IDENTITIES[3] + r"},member-c={" + IDENTITIES[4]
        + r"}}" + "\n" + cover_setup + r"""
\begin{document}
\typeout{GMCM-TEXTWIDTH=\the\textwidth}
\typeout{GMCM-TEXTHEIGHT=\the\textheight}
\typeout{GMCM-LEFT=\the\dimexpr1in+\hoffset+\oddsidemargin\relax}
\typeout{GMCM-TOP=\the\dimexpr1in+\voffset+\topmargin+\headheight+\headsep\relax}
\maketitle
\begin{abstract}
""" + abstract + r"""
\end{abstract}
\maketoc
\noindent BODYSTARTMARKER
\section{目录测试章节}
用于检查封面替换、目录和摘要不会改变正文内容与连续页码。
\end{document}
""")


def compile_fixture(parent, name, source, passes=2):
    directory = parent / name
    directory.mkdir()
    (directory / "fixture.tex").write_text(source, encoding="utf-8")
    env = os.environ.copy()
    env["TEXINPUTS"] = str(ROOT) + "//:" + env.get("TEXINPUTS", "")
    for _ in range(passes):
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "fixture.tex"], cwd=directory, env=env,
            check=False, capture_output=True, text=True, encoding="utf-8"
        )
        assert result.returncode == 0, name + ":\n" + result.stdout[-10000:]
    log = (directory / "fixture.log").read_text(encoding="utf-8", errors="replace")
    errors = re.findall(
        r"^.*(?:Overfull \\[hv]box|Missing character:|LaTeX Error|"
        r"Package .+ Error|Class .+ Error|Emergency stop).*$",
        log, re.MULTILINE
    )
    assert not errors, name + ":\n" + "\n".join(errors)
    pdf = directory / "fixture.pdf"
    pages = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"], check=True,
        capture_output=True, text=True, encoding="utf-8"
    ).stdout.split("\f")
    if not pages[-1].strip():
        pages.pop()
    reader = PdfReader(pdf)
    assert len(pages) == len(reader.pages), name + ": PDF/text page count mismatch"
    for page in reader.pages:
        assert abs(float(page.mediabox.width) - 595.28) < 1
        assert abs(float(page.mediabox.height) - 841.89) < 1
    assert not (reader.metadata or {}).get("/Author", ""), name + ": author metadata"
    return pdf, [normalized(page) for page in pages], log, reader


def assert_body_pages(pages):
    for number, page in enumerate(pages, 1):
        assert page.endswith(str(number)), f"Wrong footer on body page {number}"
        for identity in IDENTITIES:
            assert identity not in page, "Identity leaked to body: " + identity


def image_count(resources):
    """Count image objects even when PDF logos are wrapped in form objects."""
    count = 0
    xobjects = resources.get("/XObject")
    if xobjects is None:
        return 0
    for reference in xobjects.get_object().values():
        obj = reference.get_object()
        if obj.get("/Subtype") == "/Image":
            count += 1
        elif obj.get("/Subtype") == "/Form" and "/Resources" in obj:
            count += image_count(obj["/Resources"])
    return count


def assert_warning(log, *terms):
    warnings = re.findall(
        r"Class gmcm2026 Warning:.*?(?=\n\s*\n|\Z)", log,
        re.DOTALL | re.IGNORECASE
    )
    assert any(all(term.lower() in warning.lower() for term in terms)
               for warning in warnings), "Expected class warning: " + ", ".join(terms)


def main():
    with tempfile.TemporaryDirectory(prefix="gmcm-layout-") as temp:
        directory = Path(temp)
        _, anonymous, base_log, _ = compile_fixture(
            directory, "anonymous", document()
        )
        assert len(anonymous) == 2, "Short abstract and body should occupy two pages"
        assert_body_pages(anonymous)
        assert "Abstract exceeds" not in base_log
        assert "SimSun unavailable" not in base_log, "Explicit Fandol option was ignored"
        assert "SimHei unavailable" not in base_log, "Explicit Fandol option was ignored"
        # TeX points use 72.27 pt/in.  These are physical layout dimensions,
        # independent of font-specific glyph bounding boxes.
        # The 18.5 mm bottom area includes the 8 mm footer allocation.
        for field, expected_mm in (("TEXTWIDTH", 165), ("TEXTHEIGHT", 240.5),
                                   ("LEFT", 22.5), ("TOP", 30)):
            match = re.search(r"GMCM-" + field + r"=([\d.]+)pt", base_log)
            assert match, "Missing fixture dimension: " + field
            actual_mm = float(match.group(1)) * 25.4 / 72.27
            assert abs(actual_mm - expected_mm) < 0.1, (field, actual_mm)

        _, auto_pages, _, _ = compile_fixture(
            directory, "automatic_fonts", document(fontset=None)
        )
        assert auto_pages == anonymous, "Automatic font selection changed fixture text"

        _, covered, _, native_reader = compile_fixture(
            directory, "native_cover", document(options="bwprint")
        )
        assert covered[1:] == anonymous, "Native cover changes following pages"
        assert len(covered) == len(anonymous) + 1
        for identity in IDENTITIES:
            assert identity in covered[0], "Missing identity on native cover: " + identity
        for obsolete in ("参赛论文", "选择题号"):
            assert obsolete not in covered[0], "Obsolete native cover field: " + obsolete
        assert image_count(native_reader.pages[0]["/Resources"]) >= 4, (
            "Native cover must include all four official logos"
        )

        cover_source = r"""
\documentclass[a4paper]{article}
\pagestyle{empty}
\begin{document}
COVERFIRSTMARKER
\newpage
COVERSECONDMARKER
\end{document}
"""
        cover_pdf, _, _, _ = compile_fixture(directory, "cover_source", cover_source)
        _, imported, _, _ = compile_fixture(
            directory, "imported_cover", document(options="bwprint", cover_pdf=cover_pdf)
        )
        assert len(imported) == len(anonymous) + 1, "Imported cover adds blank/extra pages"
        assert "COVERFIRSTMARKER" in imported[0]
        assert "COVERSECONDMARKER" not in "".join(imported), "Imported more than page 1"
        assert imported[1:] == anonymous, "Imported cover changes body or page numbering"

        title = "LONGTITLEBEGIN" + "面向复杂环境的多目标优化与资源配置研究" * 4 + "LONGTITLEEND"
        title_pdf, title_pages, _, _ = compile_fixture(
            directory, "long_title", document(title=title)
        )
        assert title in title_pages[0], "Long title was truncated or reordered"
        bbox = subprocess.run(
            ["pdftotext", "-bbox", str(title_pdf), "-"], check=True,
            capture_output=True, text=True, encoding="utf-8"
        ).stdout
        words = ET.fromstring(bbox).findall(".//{*}page")[0].findall(".//{*}word")
        title_ys = []
        in_title = False
        for word in words:
            text = word.text or ""
            if "LONGTITLEBEGIN" in text:
                in_title = True
            if in_title:
                title_ys.append(round(float(word.attrib["yMin"]), 1))
            if "LONGTITLEEND" in text:
                break
        assert len(set(title_ys)) > 1, "Long title did not wrap onto multiple lines"
        assert_body_pages(title_pages)

        _, two_pages, two_log, _ = compile_fixture(
            directory, "two_page_abstract",
            document(abstract=r"ABSTRACTBEGINMARKER\newpage ABSTRACTENDMARKER")
        )
        assert len(two_pages) == 3, "Two abstract pages must precede one body page"
        assert "ABSTRACTENDMARKER" in two_pages[1]
        assert "BODYSTARTMARKER" in two_pages[2]
        assert "Abstract exceeds" not in two_log, "Two-page abstract warned too early"
        assert_body_pages(two_pages)

        long_abstract = "ABSTRACTBEGINMARKER\\par\n" + (
            "为验证较长摘要的完整性，本段重复给出用于版式测试的文本。"
            "摘要内容应当正常流转到下一页，排版程序应当提示作者压缩内容，"
            "并保留全部文字以供修改。\\par\n"
        ) * 70 + "ABSTRACTENDMARKER\n"
        _, long_pages, long_log, _ = compile_fixture(
            directory, "long_abstract", document(abstract=long_abstract)
        )
        body_index = next(index for index, page in enumerate(long_pages)
                          if "BODYSTARTMARKER" in page)
        assert body_index > 2, "Long fixture must exceed the two-page abstract limit"
        assert "ABSTRACTBEGINMARKER" in long_pages[0]
        assert "ABSTRACTENDMARKER" in long_pages[body_index - 1], "Abstract was truncated"
        assert_warning(long_log, "abstract", "two pages")
        assert_body_pages(long_pages)

        _, toc_pages, toc_log, _ = compile_fixture(
            directory, "withtoc", document(options="anonymous,withtoc"), passes=2
        )
        assert len(toc_pages) == len(anonymous) + 1, "Contents should add one page"
        assert "目录" in toc_pages[1] and "目录测试章节" in toc_pages[1]
        assert_warning(toc_log, "withtoc")
        assert_body_pages(toc_pages)

    print("PASS: official margins/logos, native and imported covers, continuous pages,")
    print("      wrapped long title, complete long abstract with warning, draft contents.")


if __name__ == "__main__":
    main()
