# GMCM2026 LaTeX Template

2026 华为杯全国研究生数学建模竞赛 LaTeX 基础模板。

这是论文写作起点，并非官方模板或格式合规认证版。提交前请按当届竞赛要求核对封面、匿名信息和论文格式。

## 编译

推荐：

- TeX Live 2025+
- XeLaTeX

在模板目录运行（推荐）：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

也可以手动编译两次，以更新目录和交叉引用：

```bash
xelatex main.tex
xelatex main.tex
```

在 Overleaf 中上传模板文件，将编译器设为 XeLaTeX，主文件设为 `main.tex`。

## 目录

- `main.tex`：主文件。
- `figures/`：图片目录；缺少示例图片时显示占位框。
- `reference.bib`：文献库；示例条目需替换成真实文献。
- `.gitignore`：忽略编译中间文件。

## 使用参考文献

用真实文献替换 `reference.bib` 中的示例条目，在正文中加入 `\cite{文献键}`。删除手写的 `\section{参考文献}`，取消 `\bibliography{reference}` 的注释，再用上述 `latexmk` 命令编译。

## 已包含

- 中文排版
- 数学公式
- 三线表
- 算法环境
- 图片插入
- 附录
- 参考文献接口

该模板为比赛论文写作基础版，可继续扩展 GMCMthesis 风格。
