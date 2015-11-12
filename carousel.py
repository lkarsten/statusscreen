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
import pygame

images = {}

def log(msg):
    now = datetime.now()
    print >>stderr, "%s %s" % (now.isoformat(), msg)

def reload_images(dir):
    global images
    for imagefile in glob(dir + "/*"):
        imagename = basename(imagefile)
        log("Loaded %s" % imagefile)
        try:
            img = pygame.image.load(imagefile).convert()
        except Exception as e:
            log("Error %s loading %s" % (imagefile, str(e)))
            continue

        img.set_colorkey((0, 0, 0))
        images[imagename] = img
    log("(Re)loaded %i images" % len(images))


if __name__ == "__main__":
    if len(argv) < 2:
        print "Usage: %s [--fullscreen] <inputdirectory>" % argv[0]
        print ""
        print "Input directory should have a set of loadable images."
        exit(-1)
    inputdir = argv[1]

    pygame.init()
    if "--fullscreen" in argv:
        argv.pop(argv.index("--fullscreen"))
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('carousel')

    reload_images(inputdir)

    last_reload = 0.0
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
                if event.key in [K_F5]:
                    last_reload = 0.0
                if event.key in [K_LEFT, K_SPACE]:
                    last_blit = 0.0
                elif event.key in [K_ESCAPE, K_RETURN, K_q]:
                    done = True
        if done:
            break

        if now > last_reload + 30:
            reload_images(inputdir)
            last_reload = now

        elif now > last_blit + 5:
            i += 1
            possible_images = images.values()
            if len(possible_images) == 0:
                log("No images to show, sleeping..")
                sleep(5)
                continue

            current_image = possible_images[i % len(possible_images)]
            blitpos = (200, 200)

            if 0:
                image_center = (current_image.get_height() / 2.,
                          current_image.get_width() / 2.)

                info = pygame.display.Info()
                screen_center = (info.current_h / 2., info.current_w / 2.)

                pprint(info)

                blitpos = (screen_center[0] - image_center[0],
                           screen_center[1] - image_center[1])
                blitpos = screen_center

            screen.fill((0, 0, 0))

            screen.blit(current_image, blitpos)
            pygame.display.flip()

            last_blit = now
        else:
            sleep(0.1)

    pygame.quit()
