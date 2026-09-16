# GMCM2026 LaTeX Template

2026「华为杯」第二十三届中国研究生数学建模竞赛 LaTeX 写作模板。

[![Compile LaTeX](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml/badge.svg)](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

参考 [latexstudio/GMCMthesis](https://github.com/latexstudio/GMCMthesis) 与 [andy123t/GMCMthesis](https://github.com/andy123t/GMCMthesis) 的论文结构和排版经验，补齐独立封面、匿名版本、文献引用及代码附录。开箱即可编译，无需准备示例图片。

当前正文已扩展为《基于NSGA-II的过期意大利面-42号混凝土低碳配合比优化》学术演示，包含模型、算法、数值图表、重复运行对照和局限讨论。全部响应系数、碳排放因子、成本参数与计算数据均为**合成情景**；“42号”是案例编号，不是强度等级。详见 [学术演示与复现说明](docs/DEMO.md)。

[查看示例 PDF](docs/preview.pdf) · [下载源码 ZIP](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip)

**格式核对（2026-09-16）：**本次依据 `docs/` 中提供的 2026 年附件 2《论文格式规范》和附件 3《论文模板》修改。字号、单倍行距、摘要起始页码和参考文献顺序按当届规范设置。版式对应关系与字体替代说明见 [逐项核对记录](docs/FORMAT-AUDIT.md)。

## 快速开始

1. [下载源码 ZIP](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip) 并解压。
2. 修改 `config.tex` 的论文题目、学校、参赛队号和队员姓名。
3. 修改 `sections/` 中的正文与摘要，维护 `reference.bib`。
4. 在模板根目录执行：

~~~bash
latexmk
~~~

生成 `main.pdf`。省略参赛信息封面的版本：

~~~bash
latexmk anonymous.tex
~~~

生成 `anonymous.pdf`，仅供内部审阅。正式稿使用 `main.tex`，保留附件 3 的封面结构。封面不编号，摘要从第 1 页开始，之后在页脚中部连续编号。默认不生成目录，摘要下一页直接开始正文。

**Overleaf：**上传源码 ZIP，选择 XeLaTeX 编译器。主文件设为 `main.tex`；内部审阅可选择 `anonymous.tex`。模板优先使用系统中安装的宋体、黑体，缺少时回退到发行版自带的 Fandol 字体；华文新魏、隶书也有替代字体。替代字体与官方 Word 字体不完全相同。

## 学术演示与数值复现

演示以每立方米模型拌合物为功能单位，通过绝对体积法生成配料，以碳排放、成本和负强度响应为三个最小化目标，使用受约束 NSGA-II 求取近似 Pareto 解集。碳排和成本边界包括材料生产及假想添加物预处理，不包含拌合能耗、运输、施工、服役、拆除或避免处置信用。

当前合成情景的折中解中，干意大利面添加物用量仅约 `0.027 kg/m³`。这一接近零的结果反映了假设响应与目标之间的取舍，不能解释为实际材料的有效掺量或工程建议。文中没有真实材料试验，也未验证这种假想非结构添加物的适用性。

普通 LaTeX 编译直接读取随附的数据、表格和图片，**无需运行 Python**。需要重新计算时，在项目根目录运行：

~~~bash
python -m pip install numpy matplotlib
python code/nsga2_demo.py --check
python scripts/prepare_paper.py
latexmk main.tex
latexmk anonymous.tex
~~~

优化脚本使用 NumPy，图表生成脚本另需 Matplotlib。第一步计算五个随机种子的 NSGA-II 结果及相同评价次数的均匀随机对照，并验证约束、非支配性、体积闭合及主运行的重复性；第二步生成正文数值宏、LaTeX 表格以及三组 PDF/PNG 图。结果文件、算法参数、敏感性边界和读取方法见 [DEMO.md](docs/DEMO.md)。

## 本地环境

当前工作环境已安装模板使用的宋体、黑体、华文新魏、隶书和 Times New Roman，安装位置、来源和验证方法见 [字体记录](docs/FONTS.md)。字体文件安装在本机用户目录，其他机器仍需自行准备。

推荐完整安装 TeX Live 2025/2026 或 MacTeX。MiKTeX 用户需装齐宏包，并为 `latexmk` 配置 Perl。精简的 Ubuntu/Debian 安装可补充：

~~~bash
sudo apt-get install latexmk texlive-xetex texlive-lang-chinese \
  texlive-latex-extra texlive-science texlive-bibtex-extra fonts-texgyre
~~~

不要把最新单个宏包直接混入很旧的 TeX Live；宏包和 LaTeX 内核版本需要匹配。

也可使用脚本：

~~~bash
bash build.sh            # macOS / Linux：完整版本
bash build.sh anonymous  # 省略封面
bash build.sh clean      # 清理辅助文件，保留 PDF
~~~

Windows 对应 `build.bat`、`build.bat anonymous`、`build.bat clean`。

没有 `latexmk` 时，按顺序运行：

~~~bash
xelatex -no-shell-escape main.tex
bibtex main
xelatex -no-shell-escape main.tex
xelatex -no-shell-escape main.tex
~~~

## 常用设置

| 需求 | 修改方式 |
| --- | --- |
| 修改题目、参赛信息 | 编辑 `config.tex` 中的 `\gmcmsetup{...}` |
| 保留信息封面 | 编译 `main.tex`，自动使用从附件 3 提取的四个 Logo |
| 导入填写后的 Word 封面 | 按 [说明](official/README.md) 设置 `cover-pdf` |
| 省略信息封面（内部稿） | 编译 `anonymous.tex`，或添加 `anonymous` 类选项 |
| 显示目录（内部稿） | 在 `main.tex` 的类选项中加入 `withtoc` |
| 黑白打印 | 默认 `bwprint`，链接无彩色边框 |
| 彩色链接 | 将 `bwprint` 改为 `colorprint` |
| 跨平台中文字体 | 缺少系统宋体、黑体时自动使用 Fandol；也可显式添加 `fontset=fandol` |
| 指定 Windows 字体集 | 本机安装相应字体后添加 `fontset=windows` |
| 图片与图表更新 | 修改 `scripts/prepare_paper.py` 后重新生成；自备图片在正文中用 `\includegraphics` 引入 |
| 引用文献 | 更新 `reference.bib`；引用书籍时填实际页段，正文可用 `\citep[页码]{文献键}` |
| 排版代码 | 修改 `code/`；附录使用 `\codefile` 引入 |

参赛信息也可写入 `config.local.tex`，覆盖公开配置；该文件已被 Git 忽略。省略封面不会自动删除正文、图片或代码中手动写入的身份信息。

摘要应包含建模思路、主要方法、模型、结果与结论、创新点和关键词，**一般不超过两页，无需译成英文**。引用公开资料时须同时在正文和参考文献中注明，引用程序也须注明来源。若赛题要求上传计算结果和源程序，应在该题规定的时间内上传竞赛系统；论文中的代码附录不能替代这项上传。

## 文件结构

| 文件 / 目录 | 用途 |
| --- | --- |
| `main.tex`、`anonymous.tex` | 两个编译入口 |
| `gmcm2026.cls` | 页面、标题、编号、封面和排版命令 |
| `config.tex` | 论文与参赛信息 |
| `sections/` | 摘要、建模、结果、评价与附录 |
| `figures/` | Pareto、迭代历史和敏感性图，附 PDF 与 PNG |
| `reference.bib`、`gmcm-numerical.bst` | 真实文献示例；按竞赛规范编排书籍、期刊和网页三类文献 |
| `code/` | 合成情景 NSGA-II 程序；旧通用示例供另行参考 |
| `data/` | 优化结果 JSON、CSV，以及正文使用的数值宏和表格 |
| `.latexmkrc`、`build.sh`、`build.bat` | 编译配置与脚本 |
| `scripts/` | 生成论文图表；检查 PDF、封面、长摘要、引用和数值；提供 Logo 再生脚本 |
| `docs/` | 排版依据、字体记录、学术演示复现和参考项目说明 |
| `official/` | 从附件 3 提取的原始 Logo；可选填写后的封面 PDF |

GitHub Actions 会编译两个入口并检查结果，成功后可从 [Actions](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions) 下载 `GMCM2026-PDF`。本地运行自动检查还需 `pypdf`（`python -m pip install pypdf`）和 Poppler 的 `pdftotext`（Ubuntu/Debian：`sudo apt-get install poppler-utils`）：

~~~bash
python scripts/check_build.py
python scripts/check_bibliography.py
python scripts/check_layout.py
~~~

普通编译直接使用随附图表和 `official/logos.pdf`，无需 LibreOffice 或 Python。只有重新提取 Logo 时才需 LibreOffice 和 PyMuPDF，步骤见 [资源说明](official/README.md)。数值重新计算与绘图的 Python 依赖见上文。

## 格式依据

本次依据随项目提供的 [附件 2：2026 论文格式规范](docs/附件2：“华为杯”第二十三届中国研究生数学建模竞赛论文格式规范.docx) 和 [附件 3：2026 论文模板](docs/附件3：“华为杯”第二十三届中国研究生数学建模竞赛论文模板.doc)。附件 2 落款为 2026 年 9 月 16 日。明确的文字要求优先用于正文排版，封面及摘要页结构参照附件 3；说明中不再将往届公告作为当届要求。

逐项结论见 [FORMAT-AUDIT.md](docs/FORMAT-AUDIT.md)，版式参数及文献样式支持范围见 [FORMAT.md](docs/FORMAT.md)，实现来源见 [UPSTREAM.md](docs/UPSTREAM.md)。当前内容是独立构造的学术演示，不是官方赛题或真实研究报告；正式写作时须依据实际题目、数据和来源替换。

本仓库代码采用 [MIT License](LICENSE)。
