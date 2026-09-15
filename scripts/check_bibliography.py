"""Exercise the three published GMCM reference formats with synthetic records."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


FIXTURE = r"""
@book{book,
  author={Alpha, Ada and Beta, Ben}, title={Book fixture},
  address={City}, publisher={Press}, pages={10--12}, year={2024}
}
@article{article,
  author={{测试作者}}, title={论文测试}, journal={测试期刊},
  volume={7}, number={2}, pages={21--29}, year={2023}
}
@online{site,
  author={{Example Organization}}, title={Website fixture},
  url={https://example.org/data_set?x=1&y=2#section}, urldate={2026-09-15}
}
"""


def compile_bib(directory, source):
    (directory / "fixture.bib").write_text(source, encoding="utf-8")
    result = subprocess.run(
        ["bibtex", "fixture"], cwd=directory, capture_output=True,
        text=True, encoding="utf-8"
    )
    bbl = (directory / "fixture.bbl").read_text(encoding="utf-8")
    return result, " ".join(bbl.split())


def main():
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="gmcm-bib-") as temp:
        directory = Path(temp)
        shutil.copy2(root / "gmcm-numerical.bst", directory)
        (directory / "fixture.aux").write_text(
            "\\relax\n\\citation{site,book,article}\n"
            "\\bibstyle{gmcm-numerical}\n\\bibdata{fixture}\n"
        )
        result, bbl = compile_bib(directory, FIXTURE)
        assert result.returncode == 0, result.stdout + result.stderr
        assert re.findall(r"\\bibitem\{(.*?)\}", bbl) == [
            "site", "book", "article"
        ], "References must follow citation order, not author or database order"
        assert "City: Press, 10--12, 2024." in bbl
        assert "测试期刊, 7(2): 21--29, 2023." in bbl
        assert (r"\url{https://example.org/data_set?x=1&y=2#section}, "
                "2026-09-15.") in bbl
        assert "Ada Alpha, Ben Beta" in bbl

        # Omitting book pages must be visible to a writer, not silently accepted.
        result, _ = compile_bib(directory, FIXTURE.replace("pages={10--12},", ""))
        assert "Missing pages (the cited range) in book" in result.stdout
    print("PASS: book/article/web formats, citation order, missing-page warning.")


if __name__ == "__main__":
    main()
