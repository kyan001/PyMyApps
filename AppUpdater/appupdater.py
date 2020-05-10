import os

import KyanToolKit as ktk
import consoleiotools as cit

from Updater import BrewUpdater, BrewcaskUpdater, PipUpdater

UPDATERS = (BrewUpdater, BrewcaskUpdater, PipUpdater)


def ls_outdated():
    for updater in UPDATERS:
        if updater.is_available():
            updater.ls_outdated()


def self_update():
    for updater in UPDATERS:
        if updater.is_available():
            updater.self_update()


if __name__ == '__main__':
    ls_outdated()
