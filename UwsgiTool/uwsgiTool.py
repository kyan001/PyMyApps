#!/usr/bin/env python3
# usage:
#    ./uwsgiTool.py
#    python3 uwsgiTool.py
#    ./uwsgiTool.py start/stop/reload

import os
import sys

import consoleiotools as cit
import KyanToolKit
ktk = KyanToolKit.KyanToolKit()

__version__ = '1.3.3'


def main():
    # precheck
    ktk.needPlatform("linux")
    # defines
    uwsgi_xml = get_config_file("./uwsgi.xml")  # uwsgi config file
    pid_file = get_pid_file()  # exist when running
    # run
    if pid_file and uwsgi_xml:
        show_running_status(pid_file)
        operation = get_operation()
        run_operation(operation, uwsgi_xml, pid_file)
    else:
        cit.bye()


def get_pid_file():
    """generate pid_file path and name according to script's dirname

    returns:
        '/var/run/uwsgi_dirname.pid'
    """
    dir_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    return "/var/run/uwsgi_{}.pid".format(dir_name)


def get_config_file(xml_file='./uwsgi.xml'):
    """check if uswgi config file exists"""
    dir_path = os.path.dirname(os.path.abspath(__file__))
    default_xml_file = "{}/uwsgi.xml".format(dir_path)
    if xml_file and os.path.isfile(xml_file):
        cit.info("uwsgi config file: " + xml_file)
        return xml_file
    elif os.path.isfile(default_xml_file):
        return get_config_file(default_xml_file)
    else:
        cit.err("uwsgi config file not found: " + xml_file)
        return None


def show_running_status(pid_file):
    """check if this uwsgi is already running"""
    if os.path.exists(pid_file):
        cit.warn("uwsgi is running @ " + pid_file)
        return True
    else:
        cit.info("No uwsgi running")
        return False


def get_operation():
    """start a new uwsgi, stop a running uwsgi, or reload the config and codes"""
    operations = ["start", "stop", "reload"]
    if len(sys.argv) != 2:
        return cit.get_choice(operations)
    elif sys.argv[1] in operations:
        return sys.argv[1]
    else:
        cit.err("Wrong Params: " + sys.argv[1])
        cit.bye()


def run_operation(oprtn, config_file, pid_file):
    if "start" == oprtn:
        if os.path.exists(pid_file):
            cit.ask('uwsgi is already running, start a new one? (Y/n)\n(Doing this will overwrite pid_file)')
            if cit.get_input().lower() != 'y':
                cit.info('User canceled start operation')
                return False
        ktk.runCmd("sudo uwsgi -x '{c}' --pidfile '{p}'".format(c=config_file, p=pid_file))
    elif "stop" == oprtn:
        ktk.runCmd("sudo uwsgi --stop " + pid_file)
        ktk.runCmd("sudo rm " + pid_file)
    elif "reload" == oprtn:
        ktk.runCmd("sudo uwsgi --reload " + pid_file)
    else:
        cit.err("Wrong operation: " + oprtn)
        cit.bye()


if __name__ == '__main__':
    main()
