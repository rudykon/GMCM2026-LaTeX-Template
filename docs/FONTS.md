# 本机字体安装记录

2026 年 9 月 16 日，已将模板所需字体安装到当前 Linux 用户的字体目录：

```text
~/.local/share/fonts/gmcm2026
```

共 8 个字体文件，供本机 XeLaTeX 使用。字体仅在本机用户目录安装，不随本模板仓库分发；迁移到其他机器后需另行安装。模板会自动优先使用这些字体。

| 文件 | 字体家族 | 样式 |
| --- | --- | --- |
| `SimSun.ttf` | 宋体 / SimSun | 常规 |
| `SimHei.ttf` | 黑体 / SimHei | 常规 |
| `STXinwei.ttf` | 华文新魏 / STXinwei | 常规 |
| `LiSu.ttf` | 隶书 / LiSu | 常规 |
| `Times.TTF` | Times New Roman | 常规 |
| `Timesbd.TTF` | Times New Roman | 粗体 |
| `Timesi.TTF` | Times New Roman | 斜体 |
| `Timesbi.TTF` | Times New Roman | 粗斜体 |

## 来源

四款中文字体取自公开的 [springli07/GMCM_LaTeX_overleaf 模板仓库](https://github.com/springli07/GMCM_LaTeX_overleaf/tree/a4df69ca77b58ed9eff353c3593305c01d6fc78a)，固定提交为 `a4df69ca77b58ed9eff353c3593305c01d6fc78a`。这是第三方模板中的字体副本，不是微软官方字体下载包。各文件下载地址如下：

- [SimSun.ttf](https://raw.githubusercontent.com/springli07/GMCM_LaTeX_overleaf/a4df69ca77b58ed9eff353c3593305c01d6fc78a/SimSun.ttf)
- [SimHei.ttf](https://raw.githubusercontent.com/springli07/GMCM_LaTeX_overleaf/a4df69ca77b58ed9eff353c3593305c01d6fc78a/SimHei.ttf)
- [STXinwei.ttf](https://raw.githubusercontent.com/springli07/GMCM_LaTeX_overleaf/a4df69ca77b58ed9eff353c3593305c01d6fc78a/STXinwei.ttf)
- [LiSu.ttf](https://raw.githubusercontent.com/springli07/GMCM_LaTeX_overleaf/a4df69ca77b58ed9eff353c3593305c01d6fc78a/LiSu.ttf)

Times New Roman 的四种样式提取自 SourceForge Core Fonts 项目的 [times32.exe](https://downloads.sourceforge.net/corefonts/times32.exe)，安装包 MD5 为 `ed39c8ef91b9fb80f76f702568291bd5`。

安装目录中的 `installation.json` 记录了每个文件的字体家族、下载地址和 SHA-256 校验值。

## 检查字体

查看字体匹配结果，输出路径应指向上述安装目录：

```bash
for family in SimSun SimHei STXinwei LiSu 'Times New Roman'; do
  fc-match -f '%{family}: %{file}\n' "$family"
done
```

重新编译后，查看 PDF 实际使用的字体及嵌入情况：

```bash
pdffonts main.pdf
```

`name` 列显示 PDF 中使用的字体，`emb` 列为 `yes` 表示字体已嵌入。只有文档实际用到的字体及样式会出现在该列表中。

## 本次验证

扩展学术演示后已重新编译 `main.pdf`（16 页）与 `anonymous.pdf`（15 页），并更新 `docs/preview.pdf`。`check_build.py` 与 `check_layout.py` 均通过。PDF 中已实际嵌入 SimSun、SimHei、STXinwei、LiSu 和 Times New Roman；论文题目、一级标题、正文分别为 16、14、12 pt。编译日志无缺字、字体样式缺失或排版溢出。
