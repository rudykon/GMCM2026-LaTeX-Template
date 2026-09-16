<div align="center">

# 🏆 GMCM2026 LaTeX Template

2026「华为杯」第二十三届中国研究生数学建模竞赛论文模板

[📄 完整 PDF](docs/preview.pdf) · [📦 下载源码](https://github.com/rudykon/GMCM2026-LaTeX-Template/archive/refs/heads/main.zip) · [📐 格式说明](docs/FORMAT.md)

[![封面、正文与插图排版预览](docs/preview.png)](docs/preview.pdf)

</div>

## ✨ 模板特点

- 依据当届附件 2、3 设置封面、字体、标题和页码。
- 提供公式、三线表、流程图、插图、参考文献与代码附录示例。
- 当前预览共 **5 页**，内容简短，便于直接替换；编译无需 Python。

## 🚀 快速开始

准备支持中文的 TeX 环境（如 TeX Live、MacTeX 或 MiKTeX），使用 **XeLaTeX + latexmk**。

1. 下载并解压源码，按下表填写参赛信息、替换示例内容。
2. 在项目根目录编译：

```bash
latexmk main.tex       # 带封面，生成 main.pdf
latexmk anonymous.tex  # 省略封面，生成 anonymous.pdf
```

**Overleaf：**上传源码 ZIP，选择 XeLaTeX，主文件设为 `main.tex`。
本地也可使用 `bash build.sh` 或 `build.bat`；追加 `clean` 清理辅助文件并保留 PDF。

## 📝 修改位置

| 内容 | 文件 |
| --- | --- |
| 题目、学校、队号与队员 | [config.tex](config.tex) |
| 摘要、正文与附录 | [sections/](sections/) |
| 图片与流程图 | [figures/](figures/) |
| 参考文献 | [reference.bib](reference.bib) |

示例图使用合成数据，仅展示排版。替换图片时同步修改图题和正文引用，见[插图说明](figures/README.md)。

## ⚙️ 常用说明

正式稿使用 `main.tex`；封面不编号，摘要从第 1 页开始，默认不生成目录。`anonymous.tex` 仅省略封面，用于内部审阅。

模板优先使用宋体、黑体，缺失时自动回退；字体文件不随仓库提供。参赛信息也可写入被 Git 忽略的 `config.local.tex`。导入 Word 封面见[封面说明](official/README.md)，字体与版式细节见[格式说明](docs/FORMAT.md)。

## 🤝 许可与致谢

代码采用 [MIT License](LICENSE)；官方附件与 Logo 等遵循各自许可。参考项目及实现来源见[来源与致谢](docs/FORMAT.md#实现来源与许可)。
