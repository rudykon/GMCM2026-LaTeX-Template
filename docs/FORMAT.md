# 版式与使用说明

核对日期：2026-09-16。依据本目录中的 2026 年附件 2《论文格式规范》和附件 3《论文模板》。本文集中说明版式、字体、引用和资源来源。

## 当前默认值

| 项目 | 默认设置 | 依据与边界 |
| --- | --- | --- |
| 纸张 | A4 | 附件 3 页面设置 |
| 页边距 | 上 30 mm，下 18.5 mm，左右 22.5 mm | 参考附件 3 的毫米近似值；下边距计入页脚，见下文 |
| 正文 | 小四号宋体，单倍行距，首行缩进 2 字 | 小四、宋体、单倍依附件 2；缺少系统宋体时回退到 FandolSong |
| 论文题目 | 三号黑体，居中 | 附件 2 |
| 一级标题 | 四号黑体，居中 | 附件 2 |
| 二、三级标题 | 小四宋体加粗 | 字号与字体依附件 2；加粗为模板选择 |
| 中文图表字 | 小四宋体 | 附件 2 的“其他汉字”要求 |
| 定理、引理、定义 | 名称及编号加粗，内容用楷体 | 模板选择 |
| 摘要页 | 系列赛事标题、题目横线、摘要、关键词 | 参照附件 3；题目、摘要、关键词同页依附件 2 |
| 页眉 | 无 | 附件 2；摘要页的赛事标题是页面正文 |
| 页码 | 封面不显示页码；摘要从 1 开始，页脚居中、连续编号 | 附件 2 |
| 目录 | 默认启用，位于摘要之后；`notoc` 可关闭 | 参考获奖论文的编排方式，属于模板选择 |
| 公式、图、表、算法 | 按节重新编号，如 5.1、6.1 | 模板选择；官方文字规范未规定编号样式 |
| 附录 | A 图表目录、B 结果数据、C 核心算法程序；页码连续，代码为彩色、无行号的浅灰框 | 参考所提供的 2025 年 A 题论文附录样式 |
| 参考文献 | BibTeX + gmcm-numerical，按引用次序排列 | 实现附件 2 的书籍、期刊、网页三种著录顺序 |

正文使用 `\setstretch{1}` 实现 LaTeX 单倍行距。Word 和 LaTeX 的字体度量不同，不能把“单倍”理解成每行高度等于一个字号。

页面使用 `includefoot,footskip=8mm`，将页脚计入版心；正文下边界约距纸张底部 26.5 mm，页脚基线约距底部 18.5 mm。Word 的页脚距离与 LaTeX `footskip` 基准不同，因此这些参数不表示正文区域与 Word 逐点相同。

## 封面与摘要页

默认封面使用从附件 3 提取的四个原始 Logo，并按原件设置学校、参赛队号和三位队员姓名。原件没有“选择题号”、独立年份或“参赛论文”标题，因此默认封面不印这些内容；`problem`、`year` 配置保留兼容。若希望直接使用在 Word 中填写完成的封面，也可按 [封面说明](official/README.md) 导入 A4 PDF。

封面和摘要页参照附件 3：系列赛事标题为 18 pt、赛事名称为 22 pt 华文新魏；摘要中的“题目”“摘要”“关键词”标签为 18 pt 隶书。本机有 `STXinwei`、`LiSu` 时使用相应字体，否则分别回退到黑体、楷体。论文题目本身仍按附件 2 使用三号黑体。正文优先使用系统宋体、黑体，缺少时采用 Fandol；拉丁字体优先 Times New Roman，缺少时采用 TeX Gyre Termes 等替代。

本示例按定制要求将封面三个标签等宽对齐、队员姓名居中，并将末条姓名横线延长到与参赛队号横线等长；末条横线因此比附件 3 原件更长。

`main.tex` 生成封面、标题摘要页、目录、正文、参考文献和附录。
`anonymous.tex` 仅供内部审阅，省略封面，其余内容相同。模板的学校、队号、姓名字段不会写入摘要、页眉或 PDF 作者元数据。

此选项不扫描和删除正文、图片、附件或源代码中的身份信息。附件 2 要求摘要“篇幅一般不超过两页，且无需译成英文”；摘要应包括建模思路、主要方法、模型、结果与结论、创新点和关键词。超过两页时模板会提醒，篇幅过长应自行精简，内容不会被截断。

## 字体下载与安装

仓库不分发字体文件。缺少原字体时可先安装免费替代字体完成编译；要接近附件 3 和本仓库预览的字形，则安装下表中的原字体。

### 免费字体：下载后即可编译

| 字体包 | 下载入口 | 模板中的用途 |
| --- | --- | --- |
| Fandol | [下载 ZIP](https://mirrors.ctan.org/fonts/fandol.zip) · [CTAN 说明](https://ctan.org/pkg/fandol) | 宋体、黑体缺失时使用 FandolSong、FandolHei；提供楷体回退 |
| TeX Gyre | [下载 ZIP](https://mirrors.ctan.org/fonts/tex-gyre.zip) · [CTAN 说明](https://ctan.org/pkg/tex-gyre) | Times New Roman 缺失时使用 Termes，并提供西文无衬线字体 Heros |

使用官方 TeX Live、MacTeX 或 TinyTeX 时，优先通过包管理器下载并安装，字体会放到 TeX 可搜索的位置：

```bash
tlmgr install fandol tex-gyre
latexmk main.tex
```

MiKTeX 用户在 MiKTeX Console 的 Packages 中搜索并安装 `fandol`、`tex-gyre`。通过 Linux 发行版安装的 TeX 应使用该发行版的包管理器补齐中文与 TeX Gyre 字体包，或按下文手动安装，避免混用 `tlmgr` 管理系统文件。Overleaf 的完整 TeX Live 环境通常已包含这两个包，选择 XeLaTeX 即可。

若 TeX Live / MacTeX / TinyTeX 需要手动安装，下载 ZIP 并解压，运行 `kpsewhich -var-value=TEXMFHOME` 查询个人 TeX 目录。在该目录下新建 `fonts/opentype/fandol/`，放入 Fandol 的全套 `.otf` 文件；新建 `fonts/opentype/tex-gyre/`，至少放入 `texgyretermes-*.otf` 和 `texgyreheros-*.otf` 的常规、粗体、斜体与粗斜体。然后检查：

```bash
kpsewhich FandolSong-Regular.otf
kpsewhich texgyretermes-regular.otf
```

两条命令都应输出字体文件路径；若没有输出，核对目录，并以刚才查询到的个人 TeX 目录为参数运行 `mktexlsr` 后重试。仅把 ZIP 放在项目中，或仅安装到系统字体目录，不一定能让 TeX 按文件名找到这些字体。免费字体能完成排版，但不等同于附件 3 中的原字体。

### 预览所用字体：官方获取途径

| 字体 | 获取方式 |
| --- | --- |
| 宋体 `SimSun` | Windows 提供；文件通常为 `simsun.ttc`，见[微软字体说明](https://learn.microsoft.com/en-us/typography/font-list/simsun) |
| 黑体 `SimHei` | Windows“设置 → 可选功能 → 添加功能”中安装“简体中文补充字体 / Chinese (Simplified) Supplemental Fonts”，见[微软安装说明](https://learn.microsoft.com/en-us/windows/deployment/windows-missing-fonts) |
| 华文新魏 `STXinwei` | 微软列为 Office 提供的字体；从已有授权 Office 安装获取 `STXINWEI.ttf`，见[微软字体说明](https://learn.microsoft.com/en-us/typography/font-list/stxinwei) |
| 隶书 `LiSu` | 使用已有授权字体文件；未找到可核实的官方独立下载入口，缺少时模板使用楷体 |
| Times New Roman | Windows / Office 提供，包含 `times.ttf`、`timesbd.ttf`、`timesi.ttf`、`timesbi.ttf` 四个字形文件，见[微软字体说明](https://learn.microsoft.com/en-us/typography/font-list/times-new-roman) |

Windows 可按 `Win + R`，输入 `ms-settings:optionalfeatures` 打开可选功能，下载补充字体需要联网。微软没有为上述原字体统一提供免费的独立下载包；其他系统可使用免费替代字体，或安装自己有权使用的原字体文件。Office 中可用的云字体不一定能被 XeLaTeX 识别，需确认字体已经安装到系统，或按下文从文件加载。

### 本地安装与检查

- **Windows：**解压后选中 `.ttf`、`.ttc` 或 `.otf` 字体文件，右键安装，随后重启编辑器。
- **macOS：**双击字体文件，在“字体册”中安装，随后重新编译。
- **Linux：**将解压后的字体复制到 `~/.local/share/fonts/gmcm2026/`，运行 `fc-cache -f`，再重新编译。例如已把所需字体集中放在项目的 `fonts/` 中：

  ```bash
  mkdir -p ~/.local/share/fonts/gmcm2026
  find fonts -type f \( -iname '*.ttf' -o -iname '*.ttc' -o -iname '*.otf' \) -exec cp {} ~/.local/share/fonts/gmcm2026/ \;
  fc-cache -f
  latexmk -g main.tex
  ```

Linux 可用 `fc-match SimSun` 查看匹配结果；该命令可能返回替代字体，应核对输出中的实际字体名。安装 Poppler 工具后，用 `pdffonts main.pdf` 检查 PDF 实际使用和嵌入的字体。更换字体后需重新检查分页与封面效果。

### Overleaf 或项目内加载字体

使用免费替代字体时无需上传字体。若要使用自己的原字体，在项目根目录新建 `fonts/` 上传字体文件，并在 `config.local.tex` 中按文件名加载。模板会读取此配置，但不会自动扫描 `fonts/`；仅上传文件并不能保证生效。方法参考 [Overleaf 自定义字体说明](https://www.overleaf.com/learn/latex/Questions/I_have_a_custom_font_I%27d_like_to_load_to_my_document._How_can_I_do_this%3F)。

以下示例假定文件名与代码完全一致，大小写也须一致。请按实际文件名修改，例如将 `SimSun.ttf` 改为 `simsun.ttc`；不要将 `.ttc` 文件改后缀冒充 `.ttf`。缺少某种字体时，删除对应的整组设置，即保留模板的自动回退。

```latex
% config.local.tex：与已有的参赛信息配置放在一起即可。
% 宋体：同时覆盖正文与显式使用的 \songti。
\setCJKmainfont{SimSun.ttf}[Path=fonts/,AutoFakeBold=2.5,ItalicFont=SimSun.ttf]
\setCJKfamilyfont{zhsong}{SimSun.ttf}[Path=fonts/,AutoFakeBold=2.5,ItalicFont=SimSun.ttf]

% 黑体：同时覆盖无衬线字体与 \heiti。
\setCJKsansfont{SimHei.ttf}[Path=fonts/]
\setCJKfamilyfont{zhhei}{SimHei.ttf}[Path=fonts/]

% Times New Roman：保留四种字形。
\setmainfont{times.ttf}[Path=fonts/,BoldFont=timesbd.ttf,
  ItalicFont=timesi.ttf,BoldItalicFont=timesbi.ttf]

% 封面赛事名称：华文新魏。
\setCJKfamilyfont{gmcmxinwei}{STXINWEI.ttf}[Path=fonts/]
\renewcommand{\gmcmcontestfont}{\CJKfamily{gmcmxinwei}}

% 摘要页标签：隶书。
\setCJKfamilyfont{gmcmlisu}{LiSu.ttf}[Path=fonts/]
\renewcommand{\gmcmfrontfont}{\CJKfamily{gmcmlisu}}
```

`fonts/` 与 `config.local.tex` 已加入 Git 忽略规则，不随正常 Git 提交上传；手动打包 ZIP 时仍需自行选择文件。

## 目录、附录与引用

目录默认显示一、二、三级标题，并收录参考文献、附录及附录小节。正文使用不带星号的标题命令，即可自动编号并进入目录：

```latex
\section{模型建立与求解} % 一级标题
\subsection{优化模型} % 二级标题
\subsubsection{目标函数} % 三级标题
```

带星号的标题（如 `\subsection*{优化模型}`）不会自动进入目录。使用 `latexmk` 编译会自动更新目录页码；如需关闭目录，写成 `\documentclass[bwprint,notoc]{gmcm2026}`。`withtoc` 选项仍可显式开启目录。

附录样式参考所提供的 2025 年 A 题论文《多层协同优化的神经网络处理器核内调度算法研究》（中国石油大学（华东））的图表目录、结果数据和程序附录。一级标题居中，采用“附录 A/B/C”编号；小节左对齐，编号如“C.1”。三部分各自另起页，页码与正文连续：

- **附录 A 图表目录：**通过 `\listoffigures`、`\listoftables`、`\listofalgorithms` 自动生成插图、表格与算法列表，含正文及附录中的带题注条目；使用 `latexmk` 更新页码。
- **附录 B 结果数据：**保留少量明确标注的合成输入和输出，供核对程序及展示表格排版，不代表材料试验或完整配合比结果。
- **附录 C 核心算法程序：**以 Python 展示目标计算、非支配解筛选，用简短 MATLAB 函数复核目标值；仅演示核心步骤，未实现完整 NSGA-II。示例代码未取自参考论文。

在 `\appendix` 之后，用 `\section{核心算法程序}`、`\subsection{目标函数计算（Python）}` 等命令生成标题，附录之间用 `\clearpage` 分页。代码默认使用彩色关键字、字符串和注释，配浅灰背景、细边框、不显示行号，并支持自动换行和跨页。`lstlisting` 或 `\codefile` 自动应用此样式，通过 `language=Python` 或 `language=Matlab` 指定语言。文档类的 `bwprint` / `colorprint` 选项控制链接颜色，不改变附录代码的彩色样式。

公式用 `\label` 与 `\eqref`；图片、表格、算法用 `\figref`、`\tabref`、`\algorithmref`。
表题在表上，图题在图下。计数器按节重置，附录编号形如 A.1。

二、三级标题使用加粗宋体；`theorem`、`lemma`、`definition` 环境的名称、编号及可选名称加粗，正文使用楷体。例如 `\begin{theorem}[支配关系的传递性] ... \end{theorem}`。
算法示例见 `sections/model.tex`，使用 `algorithm` 与 `algorithmic` 环境，按顶部横线、标题分隔线、底部横线排版；`\Require`、`\Ensure` 分别标注输入与输出，`\State`、`\For` 等命令编写伪代码。

参考文献标题由文献环境自动生成，不要再手工添加同名章节。
`gmcm-numerical.bst` 支持：

| BibTeX 类型 | 必要字段 | 著录顺序 |
| --- | --- | --- |
| book | author（或 editor）、title、address、publisher、pages、year | 作者，书名，出版地：出版社，起止页码，出版年 |
| article | author、title、journal、volume、pages、year；number 如有则填 | 作者，论文名，期刊名，卷(期)：起止页码，出版年 |
| misc / online / webpage | author、title、url、urldate | 作者，资源标题，网址，访问日期 |

`edition` 可填写完整的版次文字，例如 `2nd ed.`；`urldate` 使用 `YYYY-MM-DD`。
书籍页码应填实际引用范围，并在正文写 `\citep[实际页码]{书籍文献键}`。不要照抄其他文献的页码。
缺少必要字段或使用未支持的类型会产生 BibTeX 警告。会议论文、学位论文等未在该简化样式中专门实现，需按当届规范扩展样式或选择合适的文献工具；不要为了消除警告将其错误归类成网页。

引用公开资料（包括网上、博客资料）须同时在正文和参考文献中注明，引用程序须注明来源。修改文献后使用 `latexmk` 自动执行 XeLaTeX / BibTeX 编译链。

## 示例与替换

正文为简短写作模板，保留公式、流程图、三线表、文献引用与代码示例，正文结果用“待填”占位。附录中的少量合成数据用于核对示例代码输出。
`figures/example-plot.pdf` 为自制的合成数据静态插图，仅展示图片排版，替换方法见 [插图说明](../figures/README.md)。数据表和程序片段直接写在 LaTeX 附录中，项目不包含独立实验工程或数据集文件。

正式写作时应按实际题目和数据重新建立模型，更新摘要、图表、程序、文献与结论。源程序通过 listings 排版，不在 LaTeX 编译期间执行。

若赛题要求上传计算结果和编程源程序，应在该题规定的时间内上传竞赛系统以备检查。代码附录不能代替上传；附件 2 未规定统一的上传时间、文件命名或文件类型。

## 原始附件

两份官方附件保留原样，SHA-256 如下：

```text
附件 2  46d2e2a87e90608ace764203d5326d7c7e41f01a5eb79986724a6f159fd70e16
附件 3  195b06cf670ec1aeb796bfd07e6d3e98e36d16db119308dcf4d0756319fe2e29
```

## 实现来源与许可

本项目独立编写类文件与文献样式，参考以下项目的结构和用法，未复制其类文件、文献样式或论文正文：

| 参考项目 | 记录的提交 |
| --- | --- |
| [latexstudio/GMCMthesis](https://github.com/latexstudio/GMCMthesis) | `f49b88a2d95c8588ff22f80c35978ab51756ac12` |
| [andy123t/GMCMthesis](https://github.com/andy123t/GMCMthesis) | `80613e086799143ecd44ae929e28abce46fec428` |

自行编写的代码采用根目录 [MIT License](../LICENSE)。官方附件、Logo、TeX 宏包、字体及参考项目遵循各自的权利和许可。
