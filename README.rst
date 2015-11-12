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
        cd statusscreen && ./carousel.py --fullscreen testimages/
    fi

* Set up some image generators/writers to write to testimages/. (cronjobs)


