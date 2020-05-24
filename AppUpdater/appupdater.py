import os

import KyanToolKit as ktk
import consoleiotools as cit

from Updaters import *

UPDATER_CANDIDATES = (BrewUpdater, BrewcaskUpdater, PipUpdater, NvmUpdater, ChocoUpdater)
UPDATERS = []


@cit.as_session
def availability_detect():
    for updater in UPDATER_CANDIDATES:
        if not updater:
            cit.err("updater is not exist.")
            continue
        if not updater.is_available():
            cit.warn("{} is not available.".format(updater))
            continue
        cit.info("{} is available.".format(updater))
        UPDATERS.append(updater)


@cit.as_session
def list_outdated():
    for updater in UPDATERS:
        updater.list_outdated()


@cit.as_session
def self_update():
    for updater in UPDATERS:
        if not hasattr(updater, 'self_update'):
            cit.err("{} does not have self_update()".format(updater))
        else:
            updater.self_update()



if __name__ == '__main__':
    availability_detect()
    if cit.get_input("Show outdated APPs? (y/n)").strip().lower() == 'y':
        list_outdated()
    else:
        cit.info("Skiped")
    if cit.get_input("Update Package Manager? (y/n)").strip().lower() == 'y':
        self_update()
    else:
        cit.info("Skiped")
