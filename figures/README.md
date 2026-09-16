# 模板插图与可选演示图表

默认模板保留 `framework.tex` 中的 TikZ 流程图，以及 `pareto.pdf` 彩色插图。后者在 `sections/results.tex` 中通过 `\includegraphics` 引入，并提供图题、标签和正文引用；替换图片路径即可使用自己的图片。普通编译无需 Python。

本目录保存三组 NSGA-II 演示图，默认正文仅引用 Pareto 图展示插图格式。全部数据来自合成情景，不是材料试验测量，也不是短模板中新开展的计算。

| 文件名 | 内容与解释范围 |
| --- | --- |
| `pareto.pdf`、`pareto.png` | 主随机种子的近似 Pareto 解集及代表方案，用于观察碳排、成本和强度响应的取舍 |
| `convergence.pdf`、`convergence.png` | 主运行的迭代历史；各目标的极值可能来自不同方案，不能据此证明全局收敛 |
| `sensitivity.pdf`、`sensitivity.png` | 固定名义决策变量后的参数复算与强度响应下调；未对扰动情景重新优化 |

PDF 适合插入论文，PNG 供快速浏览。更新演示算法或模型参数后，在项目根目录执行：

~~~bash
python code/nsga2_demo.py --check
python scripts/prepare_paper.py
~~~

第一条命令需要 NumPy，第二条还需要 Matplotlib。图表生成脚本读取 `data/optimization_results.json`，同步生成可选数值宏和结果表格，不修改正文。已引用的同名图片会在下次编译时更新。数据边界、算法设置及复现说明见 [学术演示说明](../docs/DEMO.md)。

自备图片可用 `\includegraphics` 插入，建议采用 PDF、PNG 或 JPEG。文件名尽量使用简短英文和连字符；`main.pdf` 等编译产物被忽略，但本目录中的图片 PDF 会正常纳入 Git。
