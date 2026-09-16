%% SPDX-License-Identifier: MIT
%% Independently written, small BibTeX style for the THREE reference categories
%% in Attachment 2 of the 2026 GMCM rules: book, journal article, web resource.
%% No SORT: numbering follows first citation. Not a general GB/T 7714 style.
%% Use Chinese field separators and put the publication year last.
ENTRY
  { author editor title edition address publisher year pages
    journal volume number url urldate }
  {} {}
INTEGERS { name.index name.count entry.count }
STRINGS { names result part field.name }

FUNCTION {format.names}
{ 'names :=
  "" 'result :=
  #1 'name.index :=
  names num.names$ 'name.count :=
  { name.index name.count > { #0 } { #1 } if$ }
  { names name.index "{ff~}{vv~}{ll}{, jj}" format.name$ 'part :=
    part "others" = { "et~al." 'part := } { } if$
    result empty$
      { part 'result := }
      { result "，" * part * 'result := }
    if$
    name.index #1 + 'name.index :=
  } while$
  result
}

FUNCTION {required}
{ 'field.name :=
  duplicate$ empty$
    { pop$ "Missing " field.name * " in " * cite$ * warning$ "" }
    { }
  if$
}

FUNCTION {author.or.editor}
{ author empty$
    { editor "author/editor" required }
    { author }
  if$
  duplicate$ empty$ { } { format.names } if$
}

FUNCTION {comma.field}
{ duplicate$ empty$ { pop$ } { "，" write$ write$ } if$ }

FUNCTION {start.entry}
{ newline$
  "\bibitem{" write$ cite$ write$ "}" write$ newline$
  author.or.editor write$
  title "title" required comma.field
}

FUNCTION {end.entry}
{ "。" write$ newline$ }

FUNCTION {book}
{ start.entry
  edition empty$ { } { "（" write$ edition write$ "）" write$ } if$
  address "address" required comma.field
  "：" write$ publisher "publisher" required write$
  pages "pages (the cited range)" required comma.field
  year "year" required comma.field
  end.entry
}

FUNCTION {article}
{ start.entry
  journal "journal" required comma.field
  volume "volume" required comma.field
  number empty$ { } { "(" write$ number write$ ")" write$ } if$
  "：" write$ pages "pages" required write$
  year "year" required comma.field
  end.entry
}

FUNCTION {misc}
{ start.entry
  url "url" required
  duplicate$ empty$
    { pop$ }
    { "，\url{" write$ write$ "}" write$ }
  if$
  urldate "urldate (YYYY-MM-DD)" required comma.field
  end.entry
}

FUNCTION {online} { misc }
FUNCTION {webpage} { misc }
FUNCTION {default.type}
{ "Unsupported type for " cite$ *
  "; use book, article, or misc/online, or select another style." * warning$
  start.entry
  year comma.field
  end.entry
}

READ
FUNCTION {count.entry} { entry.count #1 + 'entry.count := }
FUNCTION {initialize} { #0 'entry.count := }
EXECUTE {initialize}
ITERATE {count.entry}
FUNCTION {begin.bib}
{ preamble$ empty$ { } { preamble$ write$ newline$ } if$
  "\begin{thebibliography}{" write$
  entry.count int.to.str$ write$ "}" write$ newline$
}
EXECUTE {begin.bib}
ITERATE {call.type$}
FUNCTION {end.bib}
{ newline$ "\end{thebibliography}" write$ newline$ }
EXECUTE {end.bib}
