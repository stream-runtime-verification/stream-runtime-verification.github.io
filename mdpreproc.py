#!/usr/bin/env python3
import json
import html
import sys

if len(sys.argv)<2:
    exit(-1)
refsfile = sys.argv[1]

citedatas = {
    "srv": {
        "prefix": "srv",
        "parseprefix": "srv",
        "refslist": []
        },
    "other": {
        "prefix": "",
        "parseprefix": "",
        "refslist": []
        }}

# Text section
def getrefint(datakey, refid):
    global citedatas
    refslist = citedatas[datakey]["refslist"]
    for ix, itemid in enumerate(refslist):
        if refid == itemid:
            return ix+1
    refslist.append(refid)
    citedatas[datakey]["refslist"] = refslist
    return len(refslist)

def formatcite(datakey, citeid):
    global citedatas
    citeint = getrefint(datakey, citeid)
    retline = "[" + str(citeint) + "](#" + citeid + ")"
    return retline

def processcites(datakey, rawcites):
    cites = list(map(lambda x: x.strip(), rawcites.split(",")))
    retline = '<sup>' + citedatas[datakey]["prefix"] + '\\['
    retline = retline + formatcite(datakey, cites[0])
    for cite in cites[1:]:
        retline = retline + ", " + formatcite(datakey, cite)
    retline = retline + '\\]</sup>'
    return retline

def findcites(datakey, line):
    global citedatas
    citations = line.split("\\cite" + citedatas[datakey]["parseprefix"] +"{")
    retline = citations[0]
    for citation in citations[1:]:
        cs = citation.split("}", 1)
        retline = retline + processcites(datakey, cs[0])
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

def printbib(datakey):
    global refsfile
    global citedatas
    with open(refsfile) as f:
        bibrefs = json.load(f)
    refslist = citedatas[datakey]["refslist"]
    referencedbibs = {x["id"]:x for x in bibrefs if x["id"] in refslist}
    bibdata = list(map(lambda x: referencedbibs[x], refslist))
    for entry in bibdata:
        print(printentry(entry))

# Main section
def processline(line):
    if line == "\\thebibliography":
        printbib("other")
        return
    if line == "\\thebibliographysrv":
        printbib("srv")
        return
    if line.lstrip().startswith("%"):
        return
    line = findcites("srv", line)
    line = findcites("other", line)
    print(line)
    return

for line in sys.stdin:
    processline(line.rstrip())
