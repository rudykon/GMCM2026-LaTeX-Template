"""Check compiled template outputs; not a full anonymity/content audit."""
import argparse
from math import isclose
import hashlib
import json
from pathlib import Path
import re
import subprocess

from pypdf import PdfReader


def normalized(text):
    return "".join(text.split())


def check_demo_results(root):
    """Validate the optional optimization demo's saved data and TeX values."""
    data_path = root / "data/optimization_results.json"
    data = json.loads(data_path.read_text())
    assert data["model"]["all_response_coefficients_and_factors_are_assumed"]
    digest = hashlib.sha256(data_path.read_bytes()).hexdigest()
    assert digest in (root / "data/paper_values.tex").read_text(), (
        "Paper values are stale; run python scripts/prepare_paper.py"
    )
    # Check the serialized physical/accounting quantities independently of
    # the optimization implementation; a unit/order error must not reach PDF.
    model = data["model"]
    front = data["main_pareto_front"]
    objectives = []
    for row in front + [data["reference_mix"]]:
        masses = {m: row[m + "_kg_m3"] for m in model["densities_kg_m3"]}
        volume = model["air_volume_m3"] + sum(
            masses[m] / rho for m, rho in model["densities_kg_m3"].items())
        assert isclose(volume, 1.0, abs_tol=1e-12)
        for key, factor in [("carbon_kgCO2e_m3", "carbon_factors_kgCO2e_kg"),
                            ("cost_CNY_m3", "cost_factors_CNY_kg")]:
            assert isclose(row[key], sum(masses[m] * v for m, v in model[factor].items()), abs_tol=1e-9)
        assert row["feasible"] and min(row["constraint_margins"].values()) >= -1e-9
    for row in front:
        objectives.append((row["carbon_kgCO2e_m3"], row["cost_CNY_m3"], -row["strength_MPa"]))
    for i, a in enumerate(objectives):
        assert not any(all(x <= y for x, y in zip(b, a)) and any(x < y for x, y in zip(b, a))
                       for k, b in enumerate(objectives) if k != i), "Stored front contains a dominated row"
    ids = {row["solution_id"] for row in front}
    assert all(row["solution_id"] in ids for row in data["selected_solutions"].values())
    assert len(data["run_summary"]) == 10
    assert all(row["objective_evaluations"] == 8080 for row in data["run_summary"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--demo", action="store_true",
        help="also check the optional synthetic optimization results and generated TeX values",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.demo:
        check_demo_results(root)

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
    if args.demo:
        print("PASS: Optional synthetic optimization results are consistent.")
    print("Pages:", {name: len(r.pages) for name, r in readers.items()})


if __name__ == "__main__":
    main()
