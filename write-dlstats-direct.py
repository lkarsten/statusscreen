#!/usr/bin/env python
"""
    Write an image with download counters.

    Author: Lasse Karstensen <lasse.karstensen@gmail.com>, October 2015.
"""
import urllib
import json
import subprocess
import pygame
from sys import stderr, argv
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from os import rename
from pprint import pprint

fmt = "%Y-%m-%d"

def compute():
    j = urllib.urlopen("https://repo.varnish-cache.org/dlstats/daily.json")
    stats = json.loads(j.read())

    r = {}
    r["last-modified"] = datetime.strptime(j.headers["last-modified"], '%a, %d %b %Y %H:%M:%S GMT')

    today = r["last-modified"]    # use the data we have, if something stops.
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


if __name__ == "__main__":
    if len(argv) == 1:
        print "Usage: %s output.png" % argv[0]
        exit(-1)

    dataset = compute()
    pygame.init()

    s = pygame.Surface((800, 600))
    s.fill((0,0,0))

    smallfont = pygame.font.SysFont(pygame.font.get_default_font(), 24)
    font = pygame.font.SysFont(pygame.font.get_default_font(), 96, bold=True)
    bigfont = pygame.font.SysFont(pygame.font.get_default_font(), 320, bold=True)

    daily = bigfont.render("%i" % dataset["today"], 1, (255, 255, 255))
    headline = font.render("downloads today", 1, (255, 255, 255))
    updated = smallfont.render("last updated %s" % dataset["last-modified"], 1, (196, 196, 196))

    s.blit(daily, (180, 100))
    s.blit(headline, (180, 400))
    s.blit(updated, (180, 500))

    tmpfile = NamedTemporaryFile(suffix="png").name
    pygame.image.save(s, tmpfile)
    rename(tmpfile, argv[1])
