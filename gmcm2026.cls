% SPDX-License-Identifier: MIT
% Independently implemented layout; see docs/FORMAT.md for sources.
\NeedsTeXFormat{LaTeX2e}[2020/10/01]
\ProvidesClass{gmcm2026}[2026/09/16 v1.4 GMCM 2026 template]
\RequirePackage{iftex}
\RequireXeTeX
\newif\ifgmcm@cover
\newif\ifgmcm@toc
\newif\ifgmcm@color
\newif\ifgmcm@autofonts
\gmcm@covertrue
\gmcm@toctrue
\gmcm@colorfalse
\gmcm@autofontstrue
\DeclareOption{anonymous}{\gmcm@coverfalse}
\DeclareOption{withoutpreface}{\gmcm@coverfalse}
\DeclareOption{withtoc}{\gmcm@toctrue}
\DeclareOption{notoc}{\gmcm@tocfalse}
\DeclareOption{bwprint}{\gmcm@colorfalse}
\DeclareOption{colorprint}{\gmcm@colortrue}
\DeclareOption*{%
  \edef\gmcm@checkoption{\noexpand\in@{fontset=}{\CurrentOption}}%
  \gmcm@checkoption
  \ifin@\gmcm@autofontsfalse\fi
  \PassOptionsToClass{\CurrentOption}{ctexart}}
\ProcessOptions\relax
\ifgmcm@autofonts\PassOptionsToClass{fontset=fandol}{ctexart}\fi
\LoadClass[UTF8,a4paper,zihao=-4]{ctexart}
\RequirePackage{geometry}
% Attachment 3: 1702/1048/1276/1274 twips, rounded to 0.1 mm.
% Include the footer in the bottom area to keep long pages clear of the number.
\geometry{top=30mm,bottom=18.5mm,left=22.5mm,right=22.5mm,
  includefoot,footskip=8mm,headheight=0pt,headsep=0pt}
\RequirePackage{setspace}
% Attachment 2 (2026-09-16) specifies single spacing.
\setstretch{1}
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}
\raggedbottom
% Prefer the official Word fonts when installed. An explicit fontset wins.
\ifgmcm@autofonts
  \IfFontExistsTF{SimSun}{%
    % SimSun has no italic face; keep Chinese text upright as required.
    \setCJKmainfont{SimSun}[AutoFakeBold=2.5,ItalicFont=SimSun]
    \setCJKfamilyfont{zhsong}{SimSun}[AutoFakeBold=2.5,ItalicFont=SimSun]
  }{\ClassWarningNoLine{gmcm2026}{SimSun unavailable; using FandolSong}}
  \IfFontExistsTF{SimHei}{%
    \setCJKsansfont{SimHei}
    \setCJKfamilyfont{zhhei}{SimHei}
  }{\ClassWarningNoLine{gmcm2026}{SimHei unavailable; using FandolHei}}
\fi
\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{%
  % File names also work with TinyTeX without a system fontconfig registration.
  \IfFontExistsTF{texgyretermes-regular.otf}{%
    \setmainfont{texgyretermes}[Extension=.otf,UprightFont=*-regular,
      BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
  }{\setmainfont{lmroman10}[Extension=.otf,UprightFont=*-regular,
      BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]}}
\IfFontExistsTF{texgyreheros-regular.otf}{%
  \setsansfont{texgyreheros}[Extension=.otf,UprightFont=*-regular,
    BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic]
}{\setsansfont{lmsans10}[Extension=.otf,UprightFont=*-regular,
    BoldFont=*-bold,ItalicFont=*-oblique,BoldItalicFont=*-boldoblique]}
\setmonofont{lmmono10-regular.otf}[
  Scale=MatchLowercase,AutoFakeBold=1.5]
% Attachment 3 uses these decorative fonts. Do not bundle
% proprietary fonts; document the portable fallbacks instead.
\IfFontExistsTF{STXinwei}{%
  \newCJKfontfamily\gmcmcontestfont{STXinwei}%
}{\newcommand{\gmcmcontestfont}{\heiti}}
\IfFontExistsTF{LiSu}{%
  \newCJKfontfamily\gmcmfrontfont{LiSu}%
}{\newcommand{\gmcmfrontfont}{\kaishu}}
\RequirePackage{amsmath,amssymb,amsthm,bm}
\RequirePackage{graphicx,xcolor}
\RequirePackage{pdfpages}
\RequirePackage{array,tabularx,longtable,booktabs,multirow}
\RequirePackage{caption,subcaption}
\RequirePackage{enumitem}
\RequirePackage{algorithm,algpseudocode}
\RequirePackage{listings}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning}
\RequirePackage[numbers,square,sort&compress]{natbib}
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
\captionsetup[subfigure]{font=normalsize}
\renewcommand{\arraystretch}{1.2}
\setlist{topsep=0.4em,itemsep=0.1em,parsep=0pt,leftmargin=*}
\ctexset{
  section={format=\centering\heiti\zihao{4},beforeskip=1.2em,afterskip=0.7em},
  subsection={format=\songti\bfseries\zihao{-4},beforeskip=0.8em,afterskip=0.4em},
  subsubsection={format=\songti\bfseries\zihao{-4},beforeskip=0.6em,afterskip=0.3em}
}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}
% Dotted leaders also connect top-level headings to their page numbers.
\renewcommand*\l@section[2]{%
  \ifnum\c@tocdepth>\z@
    \addpenalty\@secpenalty
    \addvspace{0.7em\@plus\p@}%
    \begingroup\bfseries
      \@dottedtocline{1}{0em}{1.8em}{#1}{#2}%
    \endgroup
  \fi}
\numberwithin{equation}{section}
\counterwithin{figure}{section}
\counterwithin{table}{section}
\counterwithin{algorithm}{section}
\providecommand{\theHalgorithm}{}
\renewcommand{\theHalgorithm}{\theHsection.\arabic{algorithm}}
\floatname{algorithm}{算法}
\renewcommand{\algorithmicrequire}{输入：}
\renewcommand{\algorithmicensure}{输出：}
\newtheoremstyle{gmcm}{0.6em}{0.6em}{\normalfont\kaishu}{}%
  {\normalfont\songti\bfseries}{。}{0.5em}%
  {\thmname{#1}\thmnumber{ #2}\thmnote{（#3）}}
\theoremstyle{gmcm}
\newtheorem{theorem}{定理}[section]
\newtheorem{lemma}[theorem]{引理}
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
  basicstyle=\normalsize\ttfamily\songti,keywordstyle=\bfseries,
  commentstyle=\color{black!60},stringstyle=\color{black},
  numbers=left,numberstyle=\scriptsize\color{black!60},
  numbersep=8pt,xleftmargin=2em,
  frame=single,rulecolor=\color{black!25},
  breaklines=true,columns=fullflexible,keepspaces=true,
  showstringspaces=false,tabsize=4,captionpos=t
}
% Appendix code uses colored syntax in a light gray box, independently of
% hyperlink colors, without line numbers or a separate listing caption.
\lstdefinestyle{gmcmappendix}{%
  basicstyle=\small\ttfamily\songti,
  numbers=none,frame=single,framerule=0.3pt,
  backgroundcolor=\color{black!2.5},rulecolor=\color{black!25},
  framesep=4pt,xleftmargin=6pt,xrightmargin=6pt,
  aboveskip=0.8em,belowskip=0.8em,
  keywordstyle=\color{magenta!80!black},
  commentstyle=\color{teal!60!black},
  stringstyle=\color{violet}}
% Identity fields are used only by the cover.
\def\gmcm@year{2026}
\def\gmcm@edition{第二十三届}
\def\gmcm@problem{A}
\def\gmcm@team{待填写}
\def\gmcm@school{待填写}
\def\gmcm@membera{待填写}
\def\gmcm@memberb{待填写}
\def\gmcm@memberc{待填写}
\def\gmcm@coverpdf{}
\define@key{gmcm}{title}{\title{#1}}
\define@key{gmcm}{year}{\def\gmcm@year{#1}}
\define@key{gmcm}{edition}{\def\gmcm@edition{#1}}
\define@key{gmcm}{problem}{\def\gmcm@problem{#1}}
\define@key{gmcm}{team}{\def\gmcm@team{#1}}
\define@key{gmcm}{school}{\def\gmcm@school{#1}}
\define@key{gmcm}{member-a}{\def\gmcm@membera{#1}}
\define@key{gmcm}{member-b}{\def\gmcm@memberb{#1}}
\define@key{gmcm}{member-c}{\def\gmcm@memberc{#1}}
\define@key{gmcm}{cover-pdf}{\def\gmcm@coverpdf{#1}}
\newcommand{\gmcmsetup}[1]{\setkeys{gmcm}{#1}}
\newcommand{\gmcm@contest}{“华为杯”\gmcm@edition 中国研究生数学建模竞赛}
\AtBeginDocument{%
  \hypersetup{pdftitle={\@title},pdfauthor={},pdfsubject={},pdfkeywords={}}}
% Coordinates reproduce Attachment 3's cover structure. The logos are extracted
% from its original embedded images, including its crop of the university logo.
\newcommand{\gmcm@nativecover}{%
  \IfFileExists{docs/official/logos.pdf}{}{%
    \ClassError{gmcm2026}{Official logo asset missing: docs/official/logos.pdf}%
      {Restore docs/official/logos.pdf from the template distribution.}}
  \begin{tikzpicture}[remember picture,overlay]
    \begin{scope}[shift={(current page.north west)},x=1mm,y=-1mm,
      every node/.style={inner sep=0pt,outer sep=0pt}]
      \node[anchor=north west] at (43.2153,31.9267)
        {\includegraphics{docs/official/logos.pdf}};
      \node at (105,79) {\gmcmcontestfont\zihao{-2} 中国研究生创新实践系列大赛};
      \node at (105,94) {\gmcmcontestfont\zihao{2} “华为杯”\gmcm@edition 中国研究生};
      \node at (105,110) {\gmcmcontestfont\zihao{2} 数学建模竞赛};
      % Give all cover labels the same left edge and four-character width.
      \node[anchor=west] at (34.9,144)
        {\songti\bfseries\zihao{-2}\makebox[4em][s]{学\hfill 校}};
      \node[anchor=west] at (34.9,164)
        {\songti\bfseries\zihao{-2}\makebox[4em][s]{参赛队号}};
      \node[anchor=west] at (34.9,187)
        {\songti\bfseries\zihao{-2}\makebox[4em][s]{队员姓名}};
      \node[text width=109mm,align=center] at (120,143)
        {\songti\zihao{3}\gmcm@school};
      \node[text width=109mm,align=center] at (120,163)
        {\songti\zihao{3}\gmcm@team};
      \node[anchor=west] at (65.8,176) {\songti\zihao{-2} 1.};
      \node[anchor=west] at (65.8,187.5) {\songti\zihao{-2} 2.};
      \node[anchor=west] at (65.8,199) {\songti\zihao{-2} 3.};
      % Center names in the name column; keep row numbers separate.
      \node at (121.3,176)
        {\songti\zihao{-2}\gmcm@membera};
      \node at (121.3,187.5)
        {\songti\zihao{-2}\gmcm@memberb};
      \node at (121.3,199)
        {\songti\zihao{-2}\gmcm@memberc};
      \draw[line width=1.5bp] (31.4,149.1) -- (178.7,149.1);
      \draw[line width=1.5bp] (31.4,169.1) -- (178.7,169.1);
      \draw[line width=1bp] (63.9,180.6) -- (178.7,180.6);
      \draw[line width=1bp] (63.9,192.1) -- (178.7,192.1);
      \draw[line width=1.5bp] (31.4,203.7) -- (178.7,203.7);
    \end{scope}
  \end{tikzpicture}%
  \null\clearpage
}
\renewcommand{\maketitle}{%
  \ifgmcm@cover
    \hypersetup{pageanchor=false}
    \pagenumbering{gobble}
    \thispagestyle{empty}
    \pdfbookmark[0]{参赛信息封面}{gmcm.cover}
    \ifx\gmcm@coverpdf\@empty
      \gmcm@nativecover
    \else
      % Import a filled, original official A4 cover; never recreate its logos.
      \IfFileExists{\gmcm@coverpdf}{%
        \includepdf[pages=1,noautoscale=true,
          pagecommand={\thispagestyle{empty}}]{\gmcm@coverpdf}%
      }{\ClassError{gmcm2026}{Cover PDF not found: \gmcm@coverpdf}%
        {Export the filled official cover as an A4 PDF, or clear cover-pdf.}}
    \fi
  \fi
  \hypersetup{pageanchor=true}
  \pagenumbering{arabic}
  \pagestyle{plain}
  \vspace*{10mm}
  \begin{center}
    {\gmcmcontestfont\zihao{-2} 中国研究生创新实践系列大赛\par}
    \vspace{5mm}
    {\gmcmcontestfont\zihao{2} “华为杯”\gmcm@edition 中国研究生\par
      \vspace{3mm}数学建模竞赛\par}
  \end{center}
  \vspace{8mm}
  \noindent\begin{tabularx}{\textwidth}{@{}l>{\centering\arraybackslash}X@{}}
    {\gmcmfrontfont\zihao{-2} 题\quad 目：} &
    {\heiti\zihao{3}\@title}\\\cmidrule{2-2}
  \end{tabularx}\par
}
\renewenvironment{abstract}{%
  \pdfbookmark[0]{摘要}{gmcm.abstract}
  \begin{center}\zihao{-2}\gmcmfrontfont 摘\quad 要：\end{center}
  \begingroup\setlength{\parindent}{2em}
  \noindent\hspace*{\parindent}\ignorespaces
}{\par\endgroup
  % End the page first, so material pending in the page builder is counted.
  \clearpage
  \ifnum\value{page}>3\relax
    \ClassWarningNoLine{gmcm2026}{Abstract exceeds two pages;
      the 2026 rules recommend generally no more than two pages}%
  \fi}
\newcommand{\keywords}[1]{%
  \par\medskip\noindent{\gmcmfrontfont\zihao{-2} 关键词：}#1\par}
\newcommand{\maketoc}{%
  \ifgmcm@toc
    \pdfbookmark[0]{目录}{gmcm.contents}
    \tableofcontents\clearpage
  \fi
  \bookmarksetup{startatroot}}
\let\gmcm@originalappendix\appendix
\renewcommand{\appendix}{%
  \clearpage\gmcm@originalappendix
  \ctexset{section/name={附录\space,},section/number=\Alph{section},
    section/tocline={附录\space\Alph{section}\texorpdfstring{\quad}{\space}##2},
    subsection/numberformat=\bfseries}%
  \lstset{style=gmcmappendix}}
\endinput
