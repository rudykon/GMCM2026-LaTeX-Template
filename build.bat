@echo off
setlocal
cd /d "%~dp0"
where latexmk >nul 2>nul
if errorlevel 1 (
  echo latexmk is required. Install TeX Live or MiKTeX with Perl.
  exit /b 1
)
if "%~1"=="" goto main
if /i "%~1"=="main" goto main
if /i "%~1"=="anonymous" goto anonymous
if /i "%~1"=="clean" goto clean
echo Usage: build.bat [main^|anonymous^|clean]
exit /b 2
:main
latexmk main.tex
exit /b %errorlevel%
:anonymous
latexmk anonymous.tex
exit /b %errorlevel%
:clean
latexmk -c main.tex anonymous.tex
exit /b %errorlevel%
