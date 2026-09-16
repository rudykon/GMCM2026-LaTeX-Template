# 模板插图与可选演示图表

默认模板使用 `framework.tex` 中的 TikZ 流程图示例，可直接修改节点和连线。普通编译无需 Python。

本目录另保留三组 NSGA-II 演示图，默认正文未引用。全部数据来自合成情景，不是材料试验测量。

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

第一条命令需要 NumPy，第二条还需要 Matplotlib。图表生成脚本读取 `data/optimization_results.json`，同步生成可选数值宏和结果表格，**不会自动修改短模板或插入图片**。数据边界、算法设置及复现说明见 [学术演示说明](../docs/DEMO.md)。

自备图片可用 `\includegraphics` 插入，建议采用 PDF、PNG 或 JPEG。文件名尽量使用简短英文和连字符；`main.pdf` 等编译产物被忽略，但本目录中的图片 PDF 会正常纳入 Git。
