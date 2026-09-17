# 模板字体

模板自动按下列文件名加载字体，无需安装到系统；Overleaf 使用 XeLaTeX 编译。

| 文件 | 字体与用途 |
| --- | --- |
| `SimSun.ttf` | 宋体：正文、二三级标题 |
| `SimHei.ttf` | 黑体：论文题目、一级标题 |
| `STXinwei.ttf` | 华文新魏：封面赛事名称 |
| `LiSu.ttf` | 隶书：摘要页标签 |
| `Times.TTF`、`Timesbd.TTF`、`Timesi.TTF`、`Timesbi.TTF` | Times New Roman：常规、粗体、斜体、粗斜体 |

这批文件与此前发布的字体补充包一致。中文字体文件取自 [GMCM_LaTeX_overleaf 的固定版本](https://github.com/springli07/GMCM_LaTeX_overleaf/tree/a4df69ca77b58ed9eff353c3593305c01d6fc78a)，Times New Roman 文件取自 [Core Fonts 的 times32.exe](https://downloads.sourceforge.net/corefonts/times32.exe)。字体遵循各自许可，不适用模板代码的 MIT 许可。

文件名区分大小写。缺少文件时，模板尝试系统字体或免费替代字体；其他文件名可通过 `config.local.tex` 指定，详见[字体说明](../docs/FORMAT.md#字体下载与安装)。
