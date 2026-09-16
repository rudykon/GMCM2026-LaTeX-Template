<div align="center">

# 🏆 GMCM2026 LaTeX Template

2026「华为杯」第二十三届中国研究生数学建模竞赛论文模板

[📄 完整 PDF](docs/preview.pdf) · [📦 下载源码](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip) · [📐 格式说明](docs/FORMAT.md)

[![封面、正文与插图排版预览](docs/preview.png)](docs/preview.pdf)

</div>

## 🚀 使用

1. 修改 [config.tex](config.tex) 中的题目与参赛信息。
2. 在 [sections/](sections/) 写正文，在 [reference.bib](reference.bib) 填文献，替换 [figures/](figures/) 中的示例图。
3. 准备支持中文的 TeX 环境，在项目根目录用 XeLaTeX + latexmk 编译：

```bash
latexmk main.tex       # 带封面
latexmk anonymous.tex  # 省略封面
```

Overleaf 选择 **XeLaTeX**，主文件设为 `main.tex`。字体缺失时自动回退，字体文件不随仓库提供；详见[格式与字体说明](docs/FORMAT.md)。

代码采用 [MIT License](LICENSE)；官方附件与 Logo 等遵循各自许可。[来源与致谢](docs/FORMAT.md#实现来源与许可)。
