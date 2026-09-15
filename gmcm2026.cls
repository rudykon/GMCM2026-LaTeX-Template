% SPDX-License-Identifier: MIT
% Independently implemented layout; see docs/UPSTREAM.md.
\NeedsTeXFormat{LaTeX2e}[2020/10/01]
\ProvidesClass{gmcm2026}[2026/09/15 v1.0 GMCM writing template]
\RequirePackage{iftex}
\RequireXeTeX
\newif\ifgmcm@cover
\newif\ifgmcm@toc
\newif\ifgmcm@color
\gmcm@covertrue
\gmcm@tocfalse
\gmcm@colorfalse
\DeclareOption{anonymous}{\gmcm@coverfalse}
\DeclareOption{withoutpreface}{\gmcm@coverfalse}
\DeclareOption{withtoc}{\gmcm@toctrue}
\DeclareOption{bwprint}{\gmcm@colorfalse}
\DeclareOption{colorprint}{\gmcm@colortrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexart}}
\ProcessOptions\relax
\LoadClass[UTF8,a4paper,zihao=-4]{ctexart}
\RequirePackage{geometry}
\geometry{top=30mm,bottom=25mm,left=22.5mm,right=22.5mm}
\RequirePackage{setspace}
\setstretch{1.38}
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}
\raggedbottom
% CTeX selects Chinese fonts; Latin fonts have a portable fallback.
\IfFontExistsTF{TeX Gyre Termes}
  {\setmainfont{TeX Gyre Termes}}{\setmainfont{Latin Modern Roman}}
\IfFontExistsTF{TeX Gyre Heros}
  {\setsansfont{TeX Gyre Heros}}{\setsansfont{Latin Modern Sans}}
\setmonofont{Latin Modern Mono}[
  Scale=MatchLowercase,AutoFakeBold=1.5]
\RequirePackage{amsmath,amssymb,amsthm,bm}
\RequirePackage{graphicx,xcolor}
\RequirePackage{array,tabularx,longtable,booktabs,multirow}
\RequirePackage{caption,subcaption}
\RequirePackage{enumitem}
\RequirePackage{algorithm,algpseudocode}
\RequirePackage{listings}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\RequirePackage[numbers,sort&compress]{natbib}
\RequirePackage{etoolbox,keyval,url}
\RequirePackage[unicode,bookmarksnumbered]{hyperref}
\RequirePackage{bookmark}
\definecolor{gmcmblue}{HTML}{315C7B}
\ifgmcm@color
  \hypersetup{colorlinks=true,allcolors=gmcmblue}
\else
  \hypersetup{hidelinks}
\fi
\graphicspath{{figures/}}
\DeclareGraphicsExtensions{.pdf,.png,.jpg,.jpeg}
\captionsetup{font=normalsize,labelsep=quad}
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}
\captionsetup[subfigure]{font=small}
\renewcommand{\arraystretch}{1.2}
\setlist{topsep=0.4em,itemsep=0.1em,parsep=0pt,leftmargin=*}
\ctexset{
  section={format=\centering\heiti\zihao{4},beforeskip=1.2em,afterskip=0.7em},
  subsection={format=\heiti\zihao{-4},beforeskip=0.8em,afterskip=0.4em},
  subsubsection={format=\heiti\zihao{-4},beforeskip=0.6em,afterskip=0.3em}
}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}
\numberwithin{equation}{section}
\counterwithin{figure}{section}
\counterwithin{table}{section}
\counterwithin{algorithm}{section}
\providecommand{\theHalgorithm}{}
\renewcommand{\theHalgorithm}{\theHsection.\arabic{algorithm}}
\floatname{algorithm}{算法}
\renewcommand{\algorithmicrequire}{\textbf{输入：}}
\renewcommand{\algorithmicensure}{\textbf{输出：}}
\newtheorem{theorem}{定理}[section]
\newtheorem{lemma}[theorem]{引理}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{定义}
\renewcommand{\proofname}{证明}
\renewcommand{\bibsection}{\section*{参考文献}
  \phantomsection\addcontentsline{toc}{section}{参考文献}}
\setlength{\bibsep}{0.25em}
\newcommand{\figref}[1]{图~\ref{#1}}
\newcommand{\tabref}[1]{表~\ref{#1}}
\newcommand{\secref}[1]{第~\ref{#1}~节}
\newcommand{\algorithmref}[1]{算法~\ref{#1}}
\newcommand{\codefile}[2][]{\lstinputlisting[#1]{#2}}
\renewcommand{\lstlistingname}{代码}
\lstset{
  basicstyle=\small\ttfamily,keywordstyle=\bfseries,
  commentstyle=\color{black!60},stringstyle=\color{black},
  numbers=left,numberstyle=\scriptsize\color{black!60},
  numbersep=8pt,xleftmargin=2em,
  frame=single,rulecolor=\color{black!25},
  breaklines=true,columns=fullflexible,keepspaces=true,
  showstringspaces=false,tabsize=4,captionpos=t
}
% Identity fields are used only by the cover.
\def\gmcm@year{2026}
\def\gmcm@edition{第二十三届}
\def\gmcm@problem{A}
\def\gmcm@team{待填写}
\def\gmcm@school{待填写}
\def\gmcm@membera{待填写}
\def\gmcm@memberb{待填写}
\def\gmcm@memberc{待填写}
\define@key{gmcm}{title}{\title{#1}}
\define@key{gmcm}{year}{\def\gmcm@year{#1}}
\define@key{gmcm}{edition}{\def\gmcm@edition{#1}}
\define@key{gmcm}{problem}{\def\gmcm@problem{#1}}
\define@key{gmcm}{team}{\def\gmcm@team{#1}}
\define@key{gmcm}{school}{\def\gmcm@school{#1}}
\define@key{gmcm}{member-a}{\def\gmcm@membera{#1}}
\define@key{gmcm}{member-b}{\def\gmcm@memberb{#1}}
\define@key{gmcm}{member-c}{\def\gmcm@memberc{#1}}
\newcommand{\gmcmsetup}[1]{\setkeys{gmcm}{#1}}
\newcommand{\gmcm@contest}{“华为杯”\gmcm@edition 中国研究生数学建模竞赛}
\AtBeginDocument{%
  \hypersetup{pdftitle={\@title},pdfauthor={},pdfsubject={},pdfkeywords={}}}
\renewcommand{\maketitle}{%
  \ifgmcm@cover
    \hypersetup{pageanchor=false}
    \pagenumbering{gobble}
    \thispagestyle{empty}
    \pdfbookmark[0]{参赛信息封面}{gmcm.cover}
    \begin{center}
      \vspace*{12mm}
      {\zihao{2}\heiti \gmcm@year\par}
      \vspace{10mm}
      {\zihao{2}\heiti “华为杯”\gmcm@edition\par}
      \vspace{3mm}
      {\zihao{1}\heiti 中国研究生数学建模竞赛\par}
      \vspace{20mm}
      {\zihao{2}\heiti 参赛论文\par}
      \vspace{20mm}
      \begingroup
      \zihao{4}
      \renewcommand{\arraystretch}{2.1}
      \begin{tabularx}{0.84\textwidth}{@{}lX@{}}
        学校 & \gmcm@school\\ \cmidrule(l){2-2}
        参赛队号 & \gmcm@team\\ \cmidrule(l){2-2}
        选择题号 & \gmcm@problem\\ \cmidrule(l){2-2}
        队员姓名 & 1.\quad \gmcm@membera\\ \cmidrule(l){2-2}
                 & 2.\quad \gmcm@memberb\\ \cmidrule(l){2-2}
                 & 3.\quad \gmcm@memberc\\ \cmidrule(l){2-2}
      \end{tabularx}
      \endgroup
    \end{center}
    \clearpage
  \fi
  \hypersetup{pageanchor=true}
  \pagenumbering{arabic}
  \pagestyle{plain}
  \begin{center}
    {\zihao{4}\heiti \gmcm@contest\par}
    \vspace{8mm}
    {\zihao{3}\heiti\@title\par}
  \end{center}
}
\renewenvironment{abstract}{%
  \pdfbookmark[0]{摘要}{gmcm.abstract}
  \begin{center}\zihao{4}\heiti 摘\quad 要\end{center}
  \begingroup\setlength{\parindent}{2em}
  \noindent\hspace*{\parindent}\ignorespaces
}{\par\endgroup\clearpage}
\newcommand{\keywords}[1]{%
  \par\medskip\noindent{\heiti 关键词：}#1\par}
\newcommand{\maketoc}{%
  \ifgmcm@toc
    \pdfbookmark[0]{目录}{gmcm.contents}
    \tableofcontents\clearpage
  \fi}
\let\gmcm@originalappendix\appendix
\renewcommand{\appendix}{%
  \clearpage\gmcm@originalappendix
  \ctexset{section/name={附录\space,},section/number=\Alph{section}}}
\endinput
