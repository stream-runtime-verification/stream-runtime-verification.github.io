# SRV webpage source files

Modify content in the file `precontent.md`.

Build with `$ ./generate.bash`.

Open the file `index.html` with your web browser and check that the generated webpage is ok.

# Special markdown syntax
The source file `precontent.md` is preprocessed by the program `mdpreproc.py`, which handles the bibliography (interpreting `\cite`, `\citesrv`, `\thebibliography` and `\thebibliographysrv` macros), and allows LaTeX-like comments, ignoring lines that begin with a percentage sign (i.e. lines that match the regular expession `^\s*%.*`).

The file `index.html` is autogenerated and should not be modified by hand.
