"""Annual Report Table QA domain retrieval and answer rules."""
NAME = '04-annual-report-table-qa'

import re
from decimal import Decimal
from common import norm, require
FIELDS = ("metric", "year", "value", "unit")

def validate(rows):
    keys = set()
    for r in rows:
        key = norm(r["metric"]), r["year"]
        require(key not in keys and re.fullmatch(r"[0-9]{4}",key[1]), "invalid or duplicate fiscal cell")
        require(re.fullmatch(r"-?[0-9]{1,16}(?:[.][0-9]{1,8})?",r["value"]), "invalid decimal")
        keys.add(key)

def solve(rows,q):
    q = q.rstrip("?")
    patterns = [("lookup",r"(?:what was |show )?(.+?) in (?:fy)?([0-9]{4})"),
                ("change",r"change in (.+?) from (?:fy)?([0-9]{4}) to (?:fy)?([0-9]{4})"),
                ("compare",r"compare (.+?) in (?:fy)?([0-9]{4}) and (?:fy)?([0-9]{4})")]
    for action,pattern in patterns:
        m = re.fullmatch(pattern,q)
        if not m:
            continue
        metric,*years = m.groups()
        cells = {r["year"]:r for r in rows if norm(r["metric"]) == metric}
        if not all(y in cells for y in years) or len(set(years)) != len(years):
            return
        ev = [cells[y] for y in years]
        values = [r["value"]+" "+r["unit"] for r in ev]
        if action == "lookup":
            return values[0],ev,action
        if action == "compare":
            return " | ".join(y+": "+v for y,v in zip(years,values)),ev,action
        if ev[0]["unit"] == ev[1]["unit"]:
            delta = Decimal(ev[1]["value"]) - Decimal(ev[0]["value"])
            return f"{delta} {ev[0]['unit']}",ev,action
