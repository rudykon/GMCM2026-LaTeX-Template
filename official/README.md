# 官方封面的导入位置

取得 **2026 当届官方论文模板** 后，填写其中的学校、队号、队员姓名，保留原版 Logo 和布局，将封面导出为 A4 PDF，命名为 `official/cover.pdf`。

在 `config.local.tex` 中设置：

```tex
\gmcmsetup{cover-pdf={official/cover.pdf}}
```

编译 `main.tex` 时，PDF 的第 1 页会按原尺寸替换文字封面，后续摘要从第 1 页编号。LaTeX 不会自动填写导入 PDF 中的个人信息；导入前先在官方文档中填写。文件不存在时编译会报错。

`anonymous.tex` 仍省略所有封面，仅供内部审阅。2025 年官方明确要求提交版保留封面；2026 提交要求须以当届文件为准。

`official/cover.pdf` 已被 Git 忽略，避免将填写后的封面自动提交到公开仓库。手工打包仍需自行检查文件内容。本目录不附往届 Logo 或伪造的 2026 封面。
