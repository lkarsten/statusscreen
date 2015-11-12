#!/usr/bin/env python
"""
    Simple image carousel using SDL.

    Author: Lasse Karstensen <lasse.karstensen@gmail.com>, October 2015.

"""
from sys import argv, stderr
from os.path import join, basename
from glob import glob
from time import time, sleep
from datetime import datetime
from pprint import pprint
from pygame.locals import *
from os import stat
import pygame

images = {}

logfp = None

def log(msg):
    global logfp
    if logfp is None:
        logfp = open("log-carousel.txt", "a")

    m = "%s %s" % (datetime.now().isoformat(), msg)
    print >>logfp, m
    print >>stderr, m


def load_images(dir):
    global images
    for imagefile in glob(dir + "/*"):
        fileinfo = stat(imagefile)
        imagename = basename(imagefile)

        if imagename not in images or fileinfo.st_mtime > images[imagename][0]:
            log("Loading %s" % imagefile)
            try:
                img = pygame.image.load(imagefile).convert()
            except Exception as e:
                log("Error %s loading %s" % (imagefile, str(e)))
                continue
            img.set_colorkey((0, 0, 0))
            images[imagename] = (fileinfo.st_mtime, img)


if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: %s [--fullscreen] <inputdirectory>" % argv[0]
        print ""
        print "Input directory should have a set of loadable images."
        exit(-1)

    pygame.init()
    if "--fullscreen" in argv:
        argv.pop(argv.index("--fullscreen"))
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        scale = 1.0
    else:
        scale = 0.75
        screen = pygame.display.set_mode((int(1920*scale), int(1080*scale)))
    inputdir = argv[1]

    pygame.mouse.set_visible(False)
    pygame.display.set_caption('carousel')

    last_blit = 0.0
    done = False
    i = 0

    while not done:
        now = time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key in [K_RIGHT, K_SPACE]:
                    last_blit = 0.0
                elif event.key in [K_ESCAPE, K_RETURN, K_q]:
                    done = True
        if done:
            break

        elif now > last_blit + 20:
            i += 1
            load_images(inputdir)
            possible_images = images.values()
            if len(possible_images) == 0:
                log("No images to show, sleeping..")
                sleep(5)
                continue

            current_image = possible_images[i % len(possible_images)][1]
            if scale < 1.0:
                current_image = pygame.transform.scale(current_image,
                    [ int(x*scale) for x in current_image.get_size()])

            image_center = current_image.get_rect().center
            screen_center = screen.get_rect().center
            blitpos = [ t[0]-t[1] for t in zip(screen_center, image_center) ]

            screen.fill((0, 0, 0))
            screen.blit(current_image, blitpos)
            pygame.display.flip()

            last_blit = now
        else:
            sleep(0.1)

    log("Normal exit")
    pygame.quit()
