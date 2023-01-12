#!/bin/bash
set -e
TMPDIR=/tmp/srvweb/
REFSJSON=${TMPDIR}/references.json
CONTENTMD=${TMPDIR}/content.md

mkdir -p ${TMPDIR}
pandoc -t csljson references.bib -o ${REFSJSON}
python3 mdpreproc.py ${REFSJSON} < precontent.md > ${TMPDIR}/content.md
pandoc --from markdown+escaped_line_breaks --standalone --template template.html ${CONTENTMD} -o index.html
rm -rf ${TMPDIR}
