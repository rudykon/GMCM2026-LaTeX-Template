<div align="center">

<h1>🏆 GMCM2026 LaTeX Template</h1>

<p><strong>2026「华为杯」第二十三届中国研究生数学建模竞赛</strong></p>
<p>简短、可替换的论文模板，保留封面与常用排版示例。</p>

<p>
  <a href="https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml"><img src="https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml/badge.svg" alt="Compile LaTeX"></a>
  <img src="https://img.shields.io/badge/Engine-XeLaTeX-2563EB" alt="Engine: XeLaTeX">
  <img src="https://img.shields.io/badge/Content-Short_Template-0F766E" alt="Content: Short Template">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
</p>

<p>
  <a href="docs/preview.pdf">📄 模板预览</a> ·
  <a href="https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip">📦 下载源码</a> ·
  <a href="#quick-start">🚀 快速开始</a> ·
  <a href="docs/DEMO.md">🧪 可选演示</a>
</p>

</div>

---

## ✨ 模板一览

| 功能 | 说明 |
| --- | --- |
| 📐 **2026 格式适配** | 依据当届附件 2、附件 3 核对字号、行距与页码 |
| 🏫 **原生封面** | 四个官方 Logo，题目与参赛信息集中填写 |
| 📝 **简短正文** | 摘要、问题、假设、模型、结果与结论，按实际赛题替换 |
| 🧩 **排版示例** | 公式、表格、流程图、文献引用与短代码附录 |
| 🔤 **中文字体适配** | 优先宋体、黑体，提供缺失时的替代方案 |
| ⚙️ **两个编译入口** | 带封面版本与内部审阅稿，支持 GitHub Actions |

**最近一次格式核对：2026-09-16。** 字号、单倍行距、摘要起始页码和参考文献顺序按当届附件设置，具体对应关系见 [格式核对记录](docs/FORMAT-AUDIT.md)。

<a id="quick-start"></a>

## 🚀 快速开始

准备支持中文的 **TeX 环境与 XeLaTeX、latexmk**，安装方法见下方[环境与字体](#environment)。

1. **下载项目**：[下载源码 ZIP](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip) 并解压。
2. **填写内容**：在 [config.tex](config.tex) 设置题目与参赛信息，修改 [sections/](sections/) 中的摘要和正文，在 [reference.bib](reference.bib) 维护文献。
3. **编译论文**：在项目根目录执行：

~~~bash
latexmk main.tex
~~~

输出 **`main.pdf`**，可直接阅读或检查排版。默认正文仅保留简短示例，**无需运行 Python 或优化程序**。

| 使用场景 | 编译命令 | 输出 |
| --- | --- | --- |
| 模板正文，保留信息封面 | `latexmk main.tex` | `main.pdf` |
| 内部审阅，省略信息封面 | `latexmk anonymous.tex` | `anonymous.pdf` |

正式稿使用 `main.tex`。封面不编号，摘要从第 1 页开始，后续页码连续居中；默认不生成目录，摘要下一页直接开始正文。

### ☁️ 在 Overleaf 中使用

上传源码 ZIP，选择 **XeLaTeX** 编译器，并将主文件设为 `main.tex`。内部审阅时可选择 `anonymous.tex`。

模板优先使用已安装的宋体、黑体；缺少时回退到 Fandol。华文新魏、隶书也有替代字体，替代字形与官方 Word 字体不完全相同，提交前应检查生成的 PDF。

## 📝 从示例开始写作

当前示例题目为：

> **基于NSGA-II的过期意大利面-42号混凝土低碳配合比优化**

正文保持简短，保留一个公式、一个流程图、一张“待填”结果表和一幅合成数据插图；该题目由本项目构造，不对应官方赛题。带封面的预览共 5 页，含摘要、参考文献与短代码附录。使用时替换 [config.tex](config.tex) 中的题目，以及 [sections/](sections/) 中的示例文字、图片、参数和结果。

## 🧪 可选：运行 NSGA-II 演示

仓库另保留完整的合成情景优化程序、五次运行对照及图表，供需要数值示例时参考。**默认仅引用随附的 Pareto 图作插图示例，其余结果按需引入。** 模型边界、结果解释和复现步骤见 [演示说明](docs/DEMO.md)。

~~~bash
python -m pip install numpy matplotlib
python code/nsga2_demo.py --check
python scripts/prepare_paper.py
~~~

上述命令更新 `data/` 和 `figures/` 中的演示资源；若需在论文中使用，可自行引用相应表格、数值宏和图片。

## ⚙️ 常用设置

| 想要调整什么 | 修改位置或方法 |
| --- | --- |
| 题目、学校、队号与队员 | [config.tex](config.tex) 中的 `\gmcmsetup{...}` |
| 正文、摘要与附录 | [sections/](sections/) |
| 使用原生信息封面 | 编译 `main.tex`，自动使用附件 3 提取的四个 Logo |
| 导入填写后的 Word 封面 | 按 [封面说明](official/README.md) 设置 `cover-pdf` |
| 省略封面／显示目录 | 内部稿使用 `anonymous`／`withtoc` 类选项 |
| 链接颜色 | 默认 `bwprint`；彩色链接使用 `colorprint` |
| 显式选择中文字体集 | `fontset=fandol`；已安装对应字体时可用 `fontset=windows` |
| 流程图／插入图片 | 修改 [流程图示例](figures/framework.tex)；使用 `\includegraphics` 插入自备图片 |
| 添加文献 | 更新 [reference.bib](reference.bib)，正文使用 `\citep{文献键}` |
| 引用书籍页段 | 填写实际引用范围，例如 `\citep[页码]{文献键}` |
| 排版源程序 | 将代码放入 [code/](code/)，在附录用 `\codefile` 引入 |

参赛信息也可写入 `config.local.tex` 覆盖公开配置，该文件已被 Git 忽略。省略封面不会自动清除正文、图片或代码中手动写入的身份信息。

摘要应包含建模思路、方法、模型、结果与结论、创新点和关键词，**一般不超过两页，无需译成英文**。引用公开资料与程序时应注明来源。若赛题要求上传计算结果和源程序，须按该题规定完成上传，代码附录不能替代这一步。

<a id="environment"></a>

## 🛠️ 环境与字体

可使用 **TeX Live 2025/2026、MacTeX 或配置完整的 MiKTeX**；MiKTeX 的 `latexmk` 还需要 Perl。TeX 宏包与 LaTeX 内核版本应保持匹配。

本次编译环境已安装宋体、黑体、华文新魏、隶书和 Times New Roman。**字体文件未随仓库分发**，其他机器需要自行准备或使用模板的替代字体。安装来源和验证方法见 [字体记录](docs/FONTS.md)。

<details>
<summary>🐧 Ubuntu / Debian：安装编译依赖</summary>

~~~bash
sudo apt-get install latexmk texlive-xetex texlive-lang-chinese \
  texlive-latex-extra texlive-science texlive-bibtex-extra fonts-texgyre
~~~

</details>

<details>
<summary>💻 macOS / Linux / Windows：使用构建脚本</summary>

macOS / Linux：

~~~bash
bash build.sh            # 完整版本
bash build.sh anonymous  # 省略封面
bash build.sh clean      # 清理辅助文件，保留 PDF
~~~

Windows：

~~~bat
build.bat
build.bat anonymous
build.bat clean
~~~

</details>

<details>
<summary>🔧 没有 latexmk：手工完成编译链</summary>

~~~bash
xelatex -no-shell-escape main.tex
bibtex main
xelatex -no-shell-escape main.tex
xelatex -no-shell-escape main.tex
~~~

修改文献后也需要完成 BibTeX 与后续 XeLaTeX 编译步骤。

</details>

## 🗂️ 文件导航

| 文件 / 目录 | 用途 |
| --- | --- |
| [main.tex](main.tex) · [anonymous.tex](anonymous.tex) | 带封面模板与内部审阅稿入口 |
| [config.tex](config.tex) | 论文题目与参赛信息 |
| [gmcm2026.cls](gmcm2026.cls) | 页面、标题、编号、封面及排版命令 |
| [sections/](sections/) | 摘要、建模、结果、评价与附录 |
| [figures/](figures/) | 默认流程图示例与可选演示图表 |
| [reference.bib](reference.bib) · [gmcm-numerical.bst](gmcm-numerical.bst) | 文献数据与书籍、期刊、网页三类著录样式 |
| [code/](code/) | 可选 NSGA-II 优化程序及通用代码示例 |
| [data/](data/) | 可选演示的 JSON、CSV、数值宏和表格 |
| [.latexmkrc](.latexmkrc) · [build.sh](build.sh) · [build.bat](build.bat) | 编译配置与跨平台脚本 |
| [scripts/](scripts/) | 生成图表、检查输出与重新提取 Logo |
| [docs/](docs/) | 论文预览、格式依据、字体记录及复现说明 |
| [official/](official/) | 原始 Logo 与可选 Word 封面说明 |
| [.github/workflows/latex.yml](.github/workflows/latex.yml) | GitHub Actions 编译流程 |

## ✅ 自动编译与检查

GitHub Actions 会编译两个入口并检查结果。运行成功后，可在 [Actions 页面](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions) 下载 **`GMCM2026-PDF`** 构建产物。

<details>
<summary>🧩 在本地运行输出检查</summary>

安装 Python 的 `pypdf` 与 Poppler 的 `pdftotext`。Ubuntu / Debian 可执行：

~~~bash
python -m pip install pypdf
sudo apt-get install poppler-utils
~~~

编译两个入口后，运行：

~~~bash
python scripts/check_build.py
python scripts/check_bibliography.py
python scripts/check_layout.py
~~~

检查涵盖页面尺寸与页码、正文一致性、引用解析，以及封面、长标题、长摘要等版式场景。

</details>

普通编译使用 LaTeX 示例与 `official/logos.pdf`，无需 LibreOffice 或 Python。只有重新提取 Logo 时才需 LibreOffice 和 PyMuPDF，步骤见 [资源说明](official/README.md)。

## 📐 格式依据与文档

模板依据随项目提供的两份 2026 年附件：

- [附件 2：“华为杯”第二十三届中国研究生数学建模竞赛论文格式规范](docs/附件2：“华为杯”第二十三届中国研究生数学建模竞赛论文格式规范.docx)
- [附件 3：“华为杯”第二十三届中国研究生数学建模竞赛论文模板](docs/附件3：“华为杯”第二十三届中国研究生数学建模竞赛论文模板.doc)

附件 2 落款为 **2026 年 9 月 16 日**。明确的文字要求用于正文排版，封面与摘要结构参照附件 3；模板示例在正式写作时应按实际题目、数据和来源替换。

| 文档 | 可以查到什么 |
| --- | --- |
| [📋 FORMAT-AUDIT.md](docs/FORMAT-AUDIT.md) | 当届格式逐项核对与编译验证 |
| [📏 FORMAT.md](docs/FORMAT.md) | 版式参数、引用写法与样式支持范围 |
| [🔤 FONTS.md](docs/FONTS.md) | 字体安装来源与检查方法 |
| [🧪 DEMO.md](docs/DEMO.md) | 合成模型、结果解释与完整复现步骤 |
| [🔎 UPSTREAM.md](docs/UPSTREAM.md) | 参考项目、实现来源与许可说明 |

## 🤝 致谢与许可

参考 [latexstudio/GMCMthesis](https://github.com/latexstudio/GMCMthesis) 与 [andy123t/GMCMthesis](https://github.com/andy123t/GMCMthesis) 的论文结构和排版经验，采用独立编写的类文件与文献样式。

本仓库代码采用 [MIT License](LICENSE)。官方附件、Logo、字体及其他第三方资源遵循各自的权利与许可。

<p align="center">
  <a href="#quick-start">🚀 开始写作</a> ·
  <a href="docs/preview.pdf">📄 查看模板</a> ·
  <a href="docs/DEMO.md">🧪 可选演示</a>
</p>
