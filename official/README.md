# 官方封面资源与导入

默认封面直接使用从 [2026 年附件 3：论文模板](../docs/附件3：“华为杯”第二十三届中国研究生数学建模竞赛论文模板.doc) 提取的原始 Logo：中国研究生创新实践系列大赛、研究生数学建模竞赛、华为、西安交通大学。学校、参赛队号和三位队员姓名由 `config.tex` 或 `config.local.tex` 填入；原件未列题号栏，因此不印 `problem` 字段。

`logos.pdf` 已随模板提供，普通 LaTeX 编译不需要 LibreOffice 或 Python。PDF 保留附件内四幅图像的原始像素，按 Word 显示尺寸组合，并保留正、负裁剪参数；西安交通大学图像沿用原件的右侧裁剪量 71.548%，显示校徽。图形间距与封面位置按附件 3 的转换页测量，LaTeX 以自然尺寸嵌入，不再二次缩放。

第二个 Logo 使用附件内的原始 289 × 289 像素，按原件的 78.25 × 75.30 bp 显示框排版。为改善 PDF 阅读器兼容性，PNG 图像以 DeviceRGB 嵌入，并去除第二个 Logo 中完全不透明的冗余蒙版；其他图像的真实透明区域保留。

## 资源来源与再生

四幅图像来自附件 3 转换后的 DOCX 首段内嵌资源，顺序如下：

| 图形 | DOCX 内资源路径 |
| --- | --- |
| 中国研究生创新实践系列大赛 | `word/media/image1.png` |
| 研究生数学建模竞赛 | `word/media/image2.png` |
| 华为 | `word/media/image3.jpeg` |
| 西安交通大学 | `word/media/image4.png` |

当前随附 `logos.pdf` 的 SHA-256 为 `10b275f772d02f1ac43349cf5137921b5a6f61e2b656d69accc46cee75d7866e`。原始附件的 SHA-256 见 [核对记录](../docs/FORMAT-AUDIT.md)。重新导出时 PDF 文档标识可能变化，不要求再生文件与当前文件逐字节相同。

仅在重新提取资源时，需要 LibreOffice 和 Python 的 PyMuPDF。可在项目根目录运行：

```bash
python -m pip install PyMuPDF
gmcm_official_tmp=$(mktemp -d)
soffice --headless --convert-to docx --outdir "$gmcm_official_tmp" \
  'docs/附件3：“华为杯”第二十三届中国研究生数学建模竞赛论文模板.doc'
python scripts/extract_official_logos.py \
  "$gmcm_official_tmp/附件3：“华为杯”第二十三届中国研究生数学建模竞赛论文模板.docx" \
  official/logos.pdf
```

转换结果写入临时目录，原始附件 2、附件 3 不会被覆盖。脚本通过 DOCX 中的图形关系读取四幅原图及裁剪参数，并生成供 XeLaTeX 使用的 PDF。

## 导入填写后的封面

如需直接导入填写后的 Word 封面，打开附件 3，填写其中的学校、参赛队号、队员姓名，保留原版图形和布局，将封面导出为 A4 PDF，命名为 `official/cover.pdf`。

在 `config.local.tex` 中设置：

```tex
\gmcmsetup{cover-pdf={official/cover.pdf}}
```

编译 `main.tex` 时，PDF 的第 1 页会按原尺寸替换默认封面，后续摘要从第 1 页编号。LaTeX 不会自动填写导入 PDF 中的个人信息；导入前先在官方文档中填写。文件不存在时编译会报错。

默认封面不显示页码。Word 转换时可能在封面生成页码 0；导入外部 PDF 前应检查并去掉该页码，后续编号以附件 2 的“从摘要页开始”“从 1 开始连续编号”为准。

`anonymous.tex` 省略封面，仅供内部审阅；正式稿使用 `main.tex`，保留附件 3 的封面结构。摘要及后续页面不应出现能显示答题人身份的信息。

`official/cover.pdf` 已被 Git 忽略，避免将填写后的封面自动提交到公开仓库。手工打包仍需自行检查文件内容。

官方原件和 Logo 的权利归其相应权利人，本项目的 MIT 许可不覆盖这些资源。Logo 直接取自本次附件，不重绘、不借用往届图形。
