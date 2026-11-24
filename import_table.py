"""Convert an exported annual report table into citable fiscal cells."""
import argparse
import csv
import json
import re
from pathlib import Path
import core


def convert(path):
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        table = csv.DictReader(stream)
        fields = table.fieldnames or []
        years = [f for f in fields if re.fullmatch(r"FY[0-9]{4}", f)]
        core.require(years and set(fields) == {"metric","unit",*years} and
                     len(fields) == len(set(fields)), "expected metric, unit, and distinct FY columns")
        for i, row in enumerate(table):
            core.require(None not in row, "extra CSV column")
            for key in years:
                rows.append({"id": f"t{i}-{key[2:]}", "source": f"{path.name}#row={i+2}&column={key}",
                             "metric":row["metric"], "year":key[2:], "value":row[key], "unit":row["unit"]})
    return core.validate(rows)


if __name__=="__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("csv",type=Path)
    args = cli.parse_args()
    print(json.dumps(convert(args.csv), ensure_ascii=False, indent=2))
