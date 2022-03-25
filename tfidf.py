#!/usr/bin/env python

from pathlib import Path
from collections import Counter
import dis
import math
import sys


def gather(ops, co):
    for instr in dis.get_instructions(co):
        ops[instr.opname] += 1
    for const in co.co_consts:
        if hasattr(const, 'co_code'):
            gather(ops, const)

docs = []
# n = 0
for t in Path('cpython/Lib/test').glob('**/*.py'):
    # n += 1
    # if n > 10: break
    with t.open('rb') as src:
        try:
            co = compile(src.read(), '?', 'exec')
            gather(ops := Counter(), co)
            docs.append(ops)
        except SyntaxError:
            print(t.name)

TOTAL_DOCS = len(docs)
def term_in_docs(term):
    return max(1, sum((term in d) for d in docs))
IDF = {
    term: math.log(TOTAL_DOCS / term_in_docs(term))
    for term in dis.opmap
}

def tfidf(doc):
    terms = doc.total()
    ws = []
    for t, k in doc.items():
        w = (k/terms) * IDF[t]
        ws.append((w, t))
    ws.sort(reverse=True)
    return ws

for d in docs:
    kw = tfidf(d)[:8]
    print(', '.join(b.lower() for _, b in kw))

#print(sys.version)