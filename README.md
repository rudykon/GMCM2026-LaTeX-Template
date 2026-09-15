# GMCM2026 LaTeX Template

2026「华为杯」第二十三届中国研究生数学建模竞赛 LaTeX 写作模板。

[![Compile LaTeX](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml/badge.svg)](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

参考 [latexstudio/GMCMthesis](https://github.com/latexstudio/GMCMthesis) 与 [andy123t/GMCMthesis](https://github.com/andy123t/GMCMthesis) 的论文结构和排版经验，补齐独立封面、匿名版本、文献引用及代码附录。开箱即可编译，无需准备示例图片。

[查看示例 PDF](docs/preview.pdf) · [下载源码 ZIP](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip)

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

生成 `anonymous.pdf`。封面不编号，摘要从第 1 页开始，之后连续编号。默认不生成目录。

**Overleaf：**上传源码 ZIP，选择 XeLaTeX 编译器。主文件设为 `main.tex` 或 `anonymous.tex`；两者共用正文。使用发行版自带的 Fandol 中文字体，不依赖 Windows 字体。

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
| 省略信息封面 | 编译 `anonymous.tex`，或添加 `anonymous` 类选项 |
| 显示目录 | 在 `main.tex` 的类选项中加入 `withtoc` |
| 黑白打印 | 默认 `bwprint`，链接无彩色边框 |
| 彩色链接 | 将 `bwprint` 改为 `colorprint` |
| 跨平台中文字体 | 默认 `fontset=fandol` |
| 使用 Windows 中文字体 | 本机安装相应字体后改为 `fontset=windows` |
| 图片替换 | 放入 `figures/framework.pdf` 或 `framework.png` |
| 引用文献 | 更新 `reference.bib`，正文用 `\citep{文献键}` |
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
| `reference.bib` | 真实文献示例，采用 `gbt7714-numerical` 样式 |
| `code/` | 可复现的 Python / MATLAB 示例 |
| `.latexmkrc`、`build.sh`、`build.bat` | 编译配置与脚本 |
| `scripts/check_build.py` | 检查 PDF、引用和示例数值 |
| `docs/` | 排版依据与参考项目说明 |

GitHub Actions 会编译两个入口并检查结果，成功后可从 [Actions](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions) 下载 `GMCM2026-PDF`。本地运行自动检查还需 `pypdf`（`python -m pip install pypdf`）和 Poppler 的 `pdftotext`（Ubuntu/Debian：`sudo apt-get install poppler-utils`），然后执行 `python scripts/check_build.py`。

## 格式依据

[2026 官方邀请函](https://cpipc.acge.org.cn/cw/contestNews/detail/4/2c9080189dcfa24e019dddacc24a1314?page=0)要求按《竞赛论文标准文档》编写。当前仓库采用可编辑的 2026 文字封面和参考项目的版式参数；尚未完成与当届标准文档的逐项比对，不能作为官方格式认证版。正式提交时以当届文件为准。

版式参数见 [FORMAT.md](docs/FORMAT.md)，参考版本与实现说明见 [UPSTREAM.md](docs/UPSTREAM.md)。示例数据、占位文字和文献均需按自己的论文替换。

本仓库代码采用 [MIT License](LICENSE)。
