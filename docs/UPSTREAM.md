# 参考项目与实现来源

本次参考于 2026-09-15 核对：

| 参考项目 | 核对的提交 | 主要参考内容 |
| --- | --- | --- |
| [latexstudio/GMCMthesis](https://github.com/latexstudio/GMCMthesis) | `f49b88a2d95c8588ff22f80c35978ab51756ac12` | 独立封面、摘要起始页、页面边距和标题层级 |
| [andy123t/GMCMthesis](https://github.com/andy123t/GMCMthesis) | `80613e086799143ecd44ae929e28abce46fec428` | 封面页码修复、字体适配、表格和代码附录用法 |

两者共享 GMCMthesis 项目沿革；latexstudio 的更新记录也列出了对 andy123t 改动的合并。

本仓库采用独立编写的 `gmcm2026.cls`。参考结构和排版参数，不直接分发上游类文件、文献样式、历年 Logo、宣传图片或示例论文。依赖由 TeX Live / MiKTeX 安装，不将发行版宏包改署为本仓库作品。

具体调整：

- 年份、届次、学校、队号和队员信息改为集中配置。
- 提供独立匿名入口，身份字段只用于封面，PDF 作者元数据留空。
- 正确重置按节编号的计数器，支持字母附录及可选目录。
- 默认 Fandol 中文字体，避免依赖 Courier New、隶书等特定系统字体。
- 采用发行版提供的 `gbt7714-numerical`，启用真实文献示例。
- 以轻量合成数据和标准库 Python 程序演示复现，不复用上游赛题正文。
- 增加跨平台构建入口与 GitHub Actions 编译检查。

本仓库自行编写的代码沿用根目录 [MIT License](../LICENSE)。
TeX 宏包、字体及参考项目分别遵循各自的许可。
