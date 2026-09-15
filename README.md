# GMCM2026 LaTeX Template

2026「华为杯」第二十三届中国研究生数学建模竞赛 LaTeX 写作模板。

[![Compile LaTeX](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml/badge.svg)](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

参考 [latexstudio/GMCMthesis](https://github.com/latexstudio/GMCMthesis) 与 [andy123t/GMCMthesis](https://github.com/andy123t/GMCMthesis) 的论文结构和排版经验，补齐独立封面、匿名版本、文献引用及代码附录。开箱即可编译，无需准备示例图片。

[查看示例 PDF](docs/preview.pdf) · [下载源码 ZIP](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip)

**格式核对（2026-09-15）：**已依据 2025 官方规范修正行距、标题字体和文献格式。2026 标准文档尚未取得，默认文字封面也不含当届四个 Logo，当前用于写作准备。详见 [逐项核对记录](docs/FORMAT-AUDIT.md)。

## 快速开始

1. [下载源码 ZIP](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip) 并解压。
2. 修改 `config.tex` 的题目、题号和参赛信息。
3. 修改 `sections/` 中的正文与摘要，维护 `reference.bib`。
4. 在模板根目录执行：

~~~bash
latexmk
~~~

生成 `main.pdf`。省略参赛信息封面的版本：

~~~bash
latexmk anonymous.tex
~~~

生成 `anonymous.pdf`，仅供内部审阅。2025 官方要求提交版保留封面，不能把这个无封面版本直接用于提交。文字封面不编号，摘要从第 1 页开始，之后连续编号。默认不生成目录。

**Overleaf：**上传源码 ZIP，选择 XeLaTeX 编译器。主文件设为 `main.tex`；内部审阅可选择 `anonymous.tex`。默认使用发行版自带的 Fandol 中文字体，属于宋体/黑体/楷体的跨平台替代，与官方 Word 字体不完全相同。

## 本地环境

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
| 保留信息封面 | 编译 `main.tex` |
| 导入官方封面 | 按 [说明](official/README.md) 设置 `cover-pdf`，保留当届原版 Logo 和布局 |
| 省略信息封面（内部稿） | 编译 `anonymous.tex`，或添加 `anonymous` 类选项 |
| 显示目录（内部稿） | 在 `main.tex` 的类选项中加入 `withtoc` |
| 黑白打印 | 默认 `bwprint`，链接无彩色边框 |
| 彩色链接 | 将 `bwprint` 改为 `colorprint` |
| 跨平台中文字体 | 默认 `fontset=fandol` |
| 使用 Windows 中文字体 | 本机安装相应字体后改为 `fontset=windows` |
| 图片替换 | 放入 `figures/framework.pdf` 或 `framework.png` |
| 引用文献 | 更新 `reference.bib`；引用书籍时填实际页段，正文可用 `\citep[页码]{文献键}` |
| 排版代码 | 修改 `code/`；附录使用 `\codefile` 引入 |

参赛信息也可写入 `config.local.tex`，覆盖公开配置；该文件已被 Git 忽略。省略封面不会自动删除正文、图片或代码中手动写入的身份信息。

## 文件结构

| 文件 / 目录 | 用途 |
| --- | --- |
| `main.tex`、`anonymous.tex` | 两个编译入口 |
| `gmcm2026.cls` | 页面、标题、编号、封面和排版命令 |
| `config.tex` | 论文与参赛信息 |
| `sections/` | 摘要、建模、结果、评价与附录 |
| `figures/` | 自备图片与可直接编译的矢量示例 |
| `reference.bib`、`gmcm-numerical.bst` | 真实文献示例；按竞赛规范编排书籍、期刊和网页三类文献 |
| `code/` | 可复现的 Python / MATLAB 示例 |
| `.latexmkrc`、`build.sh`、`build.bat` | 编译配置与脚本 |
| `scripts/` | 检查 PDF、引用顺序、文献字段和示例数值 |
| `docs/` | 排版依据与参考项目说明 |

GitHub Actions 会编译两个入口并检查结果，成功后可从 [Actions](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions) 下载 `GMCM2026-PDF`。本地运行自动检查还需 `pypdf`（`python -m pip install pypdf`）和 Poppler 的 `pdftotext`（Ubuntu/Debian：`sudo apt-get install poppler-utils`），然后执行 `python scripts/check_build.py`。

## 格式依据

[2026 官方邀请函](https://cpipc.acge.org.cn/cw/contestNews/detail/4/2c9080189dcfa24e019dddacc24a1314?page=0)要求按《竞赛论文标准文档》编写。本次已取得 [2025 官方开赛公告及附件](https://cpipc.acge.org.cn/cw/contestNews/detail/4/2c90801b9914a68201994b1403512e96?page=2)，据此修正单倍行距、小四宋体标题、摘要页结构和文献格式。2026 当届封面、统一摘要页和任何新增要求仍待官方原件确认。

逐项结论见 [FORMAT-AUDIT.md](docs/FORMAT-AUDIT.md)，版式参数及文献样式支持范围见 [FORMAT.md](docs/FORMAT.md)，实现来源见 [UPSTREAM.md](docs/UPSTREAM.md)。示例数据、占位文字和文献均需按自己的论文替换。

本仓库代码采用 [MIT License](LICENSE)。
