<div align="center">

<h1>🏆 GMCM2026 LaTeX Template</h1>
<p><strong>2026「华为杯」第二十三届中国研究生数学建模竞赛</strong></p>
<p>简短、可替换的论文模板，包含封面、摘要和常用排版示例。</p>
<p>
  <a href="https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml"><img src="https://github.com/rudykon/GMCM2026-LaTeX-Template/actions/workflows/latex.yml/badge.svg" alt="Compile LaTeX"></a>
  <img src="https://img.shields.io/badge/Engine-XeLaTeX-2563EB" alt="Engine: XeLaTeX">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
</p>
<p>
  <a href="docs/preview.pdf">📄 模板预览</a> ·
  <a href="https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip">📦 下载源码</a> ·
  <a href="docs/FORMAT.md">📐 格式说明</a>
</p>

</div>

## 🚀 快速开始

准备包含中文支持、XeLaTeX 和 latexmk 的 TeX 环境，例如 TeX Live、MacTeX 或 MiKTeX。

1. 下载并解压源码，在 [config.tex](config.tex) 填写题目、学校、队号和队员。
2. 修改 [sections/](sections/) 中的摘要、正文与附录，在 [reference.bib](reference.bib) 维护文献。
3. 在项目根目录编译：

```bash
latexmk main.tex       # 带封面：main.pdf
latexmk anonymous.tex # 省略封面：anonymous.pdf
```

也可使用 `bash build.sh` 或 Windows 下的 `build.bat`；追加 `anonymous` 编译审阅稿，追加 `clean` 清理辅助文件并保留 PDF。

正式稿使用 `main.tex`。封面不编号，摘要从第 1 页开始，后续页码连续居中；默认不生成目录。普通编译无需 Python。

### ☁️ Overleaf 与字体

上传源码 ZIP，选择 **XeLaTeX** 编译器，主文件设为 `main.tex`；省略封面时选择 `anonymous.tex`。

模板优先使用宋体、黑体，缺失时回退到 Fandol；封面字体也提供替代方案。字体文件不随仓库分发，替代字形可能与官方 Word 不同，提交前请检查 PDF。字体、格式依据及资源来源见 [格式说明](docs/FORMAT.md)。

## 📝 替换示例内容

当前趣味题目为“基于NSGA-II的过期意大利面-42号混凝土低碳配合比优化”，仅用于展示排版。带封面预览共 **5 页**，保留公式、表格、流程图、静态插图、引用和短代码附录。

插图 [figures/example-plot.pdf](figures/example-plot.pdf) 使用合成数据，替换为自己的图片后修改正文中的 `\includegraphics` 路径、图题和引用；流程图可直接编辑 [figures/framework.tex](figures/framework.tex)。正文、参数及“待填”结果均应按实际赛题替换。

## ⚙️ 常用设置

| 内容 | 修改位置或方法 |
| --- | --- |
| 题目与参赛信息 | [config.tex](config.tex) 中的 `\gmcmsetup{...}` |
| 摘要、正文与附录 | [sections/](sections/) |
| 参考文献 | [reference.bib](reference.bib)，正文使用 `\citep{文献键}` |
| 导入填写后的 Word 封面 | 按 [封面说明](official/README.md) 设置 `cover-pdf` |
| 省略封面／显示目录 | 类选项 `anonymous`／`withtoc` |
| 黑白／彩色链接 | 类选项 `bwprint`／`colorprint` |
| 指定中文字体集 | `fontset=fandol`；安装对应字体后可用 `fontset=windows` |

参赛信息可写入被 Git 忽略的 `config.local.tex`，覆盖公开配置。省略封面不会清除正文或图片中手动填写的身份信息。

## 🗂️ 项目结构

| 文件 / 目录 | 用途 |
| --- | --- |
| [main.tex](main.tex) · [anonymous.tex](anonymous.tex) | 带封面入口与内部审阅稿入口 |
| [gmcm2026.cls](gmcm2026.cls) · [config.tex](config.tex) | 排版定义与论文设置 |
| [sections/](sections/) · [figures/](figures/) | 简短正文与插图示例 |
| [reference.bib](reference.bib) · [gmcm-numerical.bst](gmcm-numerical.bst) | 文献数据与著录样式 |
| [docs/](docs/) | PDF 预览、格式说明与官方附件 2、3 |
| [official/](official/) | 官方 Logo 及封面资源说明 |
| [scripts/](scripts/) | 编译结果检查、版式检查与 Logo 提取工具 |
| [.latexmkrc](.latexmkrc) · [build.sh](build.sh) · [build.bat](build.bat) | 编译配置与构建脚本 |

## ✅ 自动编译与检查

[GitHub Actions](https://github.com/rudykon/GMCM2026-LaTeX-Template/actions) 会编译两个入口并检查页面、引用与版式；成功后可下载 `GMCM2026-PDF` 构建产物。

本地检查需安装 Python 的 `pypdf` 和 Poppler 的 `pdftotext`，编译两个入口后执行：

```bash
python scripts/check_build.py
python scripts/check_bibliography.py
python scripts/check_layout.py
```

仅重新提取官方 Logo 时需要 LibreOffice 和 PyMuPDF，见 [资源说明](official/README.md)。

## 🤝 致谢与许可

模板依据项目内的 2026 年官方附件 2、3 编写，参考 [latexstudio/GMCMthesis](https://github.com/latexstudio/GMCMthesis) 与 [andy123t/GMCMthesis](https://github.com/andy123t/GMCMthesis) 的排版经验，类文件与文献样式独立实现。

本仓库代码采用 [MIT License](LICENSE)；官方附件、Logo、字体及其他第三方资源遵循各自的权利与许可，详见 [格式与来源说明](docs/FORMAT.md)。
