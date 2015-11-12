Image carousel
==============

A small image viewer/carousel.


Requirements
------------

Install on Debian::

    apt-get install python-pygame


Installation (on a pi)
----------------------

* Start with a regular Raspbian Jessie image.

* (set a password on the pi user ..)

* git clone ..

* Put this in .bashrc::

    if [ "$SHLVL" == 1 -a -z "$SSH_CONNECTION" ]; then
        cd statusscreen && ./carousel.py --fullscreen images
    fi

* Set up some (cron-ed) image generators/writers to write to images/.
  For VS: there is a separate git repository with these. (carousel-writers.git)

At this point the automatic login of the pi user will start the
carousel on boot.

You also need to stop lightdm from starting. Details fuzzy.
