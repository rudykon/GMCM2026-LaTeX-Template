# 插图示例

- `example-plot.pdf`：正文使用的静态示例图。数据为合成数据，仅展示图片排版，不代表研究结论。
- `framework.tex`：可直接编辑的 TikZ 流程图。

图片的插入、图题、标签与交叉引用见 `sections/problem2.tex`：

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.72\linewidth]{figures/example-plot.pdf}
  \caption{图片说明}
  \label{fig:example}
\end{figure}
```

在正文用 `图~\ref{fig:example}` 引用。替换为自己的 PDF、PNG 或 JPEG 即可，编译不需要绘图程序或数据文件。
