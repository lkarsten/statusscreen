#!/usr/bin/env python
"""
    Simple image carousel using SDL.

    Author: Lasse Karstensen <lasse.karstensen@gmail.com>, October 2015.

"""
import urllib
import json
import subprocess
from sys import stderr
from datetime import datetime, timedelta
from os import unlink, rename
from pprint import pprint

fmt = "%Y-%m-%d"

def compute():
    r = {}
    j = urllib.urlopen("https://repo.varnish-cache.org/dlstats/daily.json")
    stats = json.loads(j.read())
    today = datetime.today()
    r["today"] = stats[today.strftime(fmt)]
    r["thismonth"] = 0
    for i in range(0, 30):
        then = today - timedelta(days=i)
        key = then.strftime(fmt)
        if key not in stats:
            print >>stderr, "Missing data for %s" % key
            continue
        r["thismonth"] += int(stats[key])

    r["lastyear"] = 0
    for i in range(0, 30):
        then = today - timedelta(days=i + 365)
        key = then.strftime(fmt)
        if key not in stats:
            print >>stderr, "Missing data for %s" % key
            continue
        r["lastyear"] += int(stats[key])

    return r


def transform_and_write(dataset, outputfile="vco-dl.png"):
    imagefile = "Varnish_cache_downloads.svg"
    m = open(imagefile).read()

    m = m.replace("#10000#", str(dataset["today"]))
    m = m.replace("%10000%", str(dataset["thismonth"]))

    m = m.replace("&amp;10000&amp;", "")
    m = m.replace("?10000?", str(dataset["lastyear"]))

    with open("tmp.svg", "wb") as outfp:
        outfp.write(m)

    subprocess.call(["convert", "tmp.svg", "tmp.png"])
    rename("tmp.png", outputfile)
    unlink("tmp.svg")

if __name__ == "__main__":
    dataset = compute()
    transform_and_write(dataset)
