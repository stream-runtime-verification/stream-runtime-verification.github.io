#!/usr/bin/env python3
import json
import html
import sys

if len(sys.argv)<2:
    exit(-1)
refsfile = sys.argv[1]
refslist = []

# Text section
def getrefint(refid):
    global refslist
    for ix, itemid in enumerate(refslist):
        if refid == itemid:
            return ix+1
    refslist.append(refid)
    return len(refslist)

def formatcite(citeid):
    citeint = getrefint(citeid)
    retline = "[" + str(citeint) + "](#" + citeid + ")"
    return retline

def processcites(rawcites):
    cites = list(map(lambda x: x.strip(), rawcites.split(",")))
    retline = '<sup>\\['
    retline = retline + formatcite(cites[0])
    for cite in cites[1:]:
        retline = retline + ", " + formatcite(cite)
    retline = retline + '\\]</sup>'
    return retline

def findcites(line):
    citations = line.split("\\cite{")
    retline = citations[0]
    for citation in citations[1:]:
        cs = citation.split("}", 1)
        retline = retline + processcites(cs[0])
        retline = retline + cs[1]
    return retline

# Biblio printing section
def printauthor(author):
    given = author["given"]
    family = author["family"]
    return html.escape(given[0] + ". " + family)

def printauthors(entry):
    authors = firstofkeys(entry, ["author", "editor"])
    entrystr = printauthor(authors[0])
    for author in authors[1:]:
        entrystr = entrystr + ", " + printauthor(author)
    return entrystr

def printtitle(entry):
    return "**" + entry["title"] + "**"

def firstofkeys(kv,keys):
    for k in keys:
        if k in kv:
            return kv[k]

def printcontainer(entry):
    container = firstofkeys(entry, ["container-title", "chapter-number"])
    if container is None:
        return ""
    return ". In: *" + container + "*"

def printyear(entry):
    return str(entry["issued"]["date-parts"][0][0])

def printref(entry):
    return '<a name="' + entry["id"] + '"></a>'

def printdoi(entry):
    if not "DOI" in entry:
        return ""
    target = "https://doi.org/" + entry["DOI"]
    return '<a href="' + target + '" target="_blank" class="doilogo">DOI</a>'

def printentry(entry):
    entrystr = "1. "
    entrystr = entrystr + printauthors(entry)
    entrystr = entrystr + ". " + printtitle(entry)
    entrystr = entrystr + printcontainer(entry)
    entrystr = entrystr + " (" + printyear(entry) + ")."
    entrystr = entrystr + printref(entry)
    entrystr = entrystr + printdoi(entry)
    return entrystr

def printbib():
    global refsfile
    with open(refsfile) as f:
        bibrefs = json.load(f)
    referencedbibs = {x["id"]:x for x in bibrefs if x["id"] in refslist}
    bibdata = list(map(lambda x: referencedbibs[x], refslist))
    for entry in bibdata:
        print(printentry(entry))

def processline(line):
    if line == "\\thebibliography":
        printbib()
        return
    if line.lstrip().startswith("%"):
        return
    print(findcites(line))
    return

for line in sys.stdin:
    processline(line.rstrip())
