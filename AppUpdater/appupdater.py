import os

import KyanToolKit as ktk
import consoleiotools as cit

from Updaters import *

UPDATER_CANDIDATES = (BrewUpdater, BrewcaskUpdater, PipUpdater, NvmUpdater, ChocoUpdater)


@cit.as_session
def availability_detect(candi_updaters: list):
    avail_updaters = []
    for updater in candi_updaters:
        if not updater:
            cit.err("updater is not exist.")
            continue
        if not updater.is_available():
            cit.warn(f"{updater} is not available.")
            continue
        cit.info(f"{updater} is available.")
        avail_updaters.append(updater)
    return avail_updaters


@cit.as_session
def list_outdated_1by1(updaters: list):
    for updater in updaters:
        if not hasattr(updater, 'list_outdated'):
            cit.err(f"{updater} does not have list_outdated()")
        else:
            updater.list_outdated()


@cit.as_session
def self_update_1by1(updaters: list):
    for updater in updaters:
        if not hasattr(updater, 'self_update'):
            cit.err(f"{updater} does not have self_update()")
        else:
            updater.self_update()


@cit.as_session
def upgrade_all_1by1(updaters: list):
    for updater in updaters:
        if not hasattr(updater, 'upgrade_all'):
            cit.err(f"{updater} does not have upgrade_all()")
        else:
            updater.upgrade_all()


@cit.as_session
def select_updaters(avail_updaters: list):
    selected_updaters = []
    SENTINEL_ALL = "** ALL **"
    SENTINEL_DONE = "** DONE **"
    menu = [SENTINEL_DONE] + avail_updaters + [SENTINEL_ALL]
    while True:
        cit.info(f"Selected Updaters: {selected_updaters}")
        cit.ask("Please Select Updaters:")
        selection = cit.get_choice(menu)
        if selection == SENTINEL_DONE:
            return selected_updaters
        if selection == SENTINEL_ALL:
            return avail_updaters
        selected_updaters.append(selection)
        menu.remove(selection)


if __name__ == '__main__':
    updaters = availability_detect(UPDATER_CANDIDATES)
    updaters = select_updaters(updaters)
    if cit.get_input("Show Outdated Packages? (y/n)").strip().lower() == 'y':
        list_outdated_1by1(updaters)
    else:
        cit.info("Skiped")
    if cit.get_input("Update Package Manager Itself? (y/n)").strip().lower() == 'y':
        self_update_1by1(updaters)
    else:
        cit.info("Skiped")
    if cit.get_input("Update All Packages for each Package Manager? (y/n)").strip().lower() == 'y':
        upgrade_all_1by1(updaters)
    else:
        cit.info("Skiped")
