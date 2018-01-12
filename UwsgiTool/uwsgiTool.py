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

__version__ = '1.5.6'


def main():
    # precheck
    # ktk.needPlatform("linux")
    cit.info('Uwsgi Tool: version {}'.format(__version__))
    cit.br()
    # defines
    uwsgi_xml = get_config_file("./uwsgi.xml")  # uwsgi config file
    pid_file = get_pid_file()  # exist when running
    log_file = get_log_file()
    # run
    if pid_file and uwsgi_xml:
        show_running_status(pid_file)
        operation = get_operation()
        run_operation(operation, uwsgi_xml, pid_file, log_file)
    else:
        cit.bye()


@cit.as_session
def update_uwsgitool():
    """Check and update djangoTool.py from github"""
    url = 'https://raw.githubusercontent.com/kyan001/PyMyApps/master/UwsgiTool/uwsgiTool.py'
    if ktk.updateFile(__file__, url):
        ktk.runCmd('{py} "{f}"'.format(py=ktk.getPyCmd(), f=__file__))
        cit.bye(0)


def get_pid_file():
    """generate pid_file path and name according to script's dirname

    returns:
        '/var/run/uwsgi_dirname.pid'
    """
    dir_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    return "/var/run/uwsgi_{}.pid".format(dir_name)


def get_log_file():
    """generate log_file path and name according to script's dirname

    returns:
        '/var/log/uwsgi_dirname.log'
    """
    dir_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    return "/var/log/uwsgi_{}.log".format(dir_name)


@cit.as_session
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


@cit.as_session
def show_running_status(pid_file):
    """check if this uwsgi is already running"""
    if os.path.exists(pid_file):
        cit.warn("uwsgi is running @ " + pid_file)
        return True
    else:
        cit.info("No uwsgi running")
        return False


@cit.as_session('Select one of these:')
def get_operation():
    """start a new uwsgi, stop a running uwsgi, or reload the config and codes"""
    operations = ["*** update uwsgiTool ***", "start", "stop", "reload"]
    if len(sys.argv) != 2:
        return cit.get_choice(operations)
    elif sys.argv[1] in operations:
        selected = sys.argv[1]
        cit.info("Selected: {}".format(selected))
        return selected
    else:
        cit.err("Wrong Params: " + sys.argv[1])
        cit.bye()


def run_operation(oprtn, config_file, pid_file, log_file):
    if "start" == oprtn:
        if os.path.exists(pid_file):
            cit.ask('uwsgi is already running, start a new one? (Y/n)\n(Doing this will overwrite pid_file)')
            if cit.get_input().lower() != 'y':
                cit.info('User canceled start operation')
                return False
        ktk.runCmd("sudo uwsgi -x '{c}' --pidfile '{p}' --daemonize '{d}'".format(c=config_file, p=pid_file, d=log_file))
    elif "stop" == oprtn:
        ktk.runCmd("sudo uwsgi --stop " + pid_file)
        ktk.runCmd("sudo rm " + pid_file)
    elif "reload" == oprtn:
        ktk.runCmd("sudo uwsgi --reload " + pid_file)
    elif "*** update uwsgiTool ***" == oprtn:
        update_uwsgitool()
    else:
        cit.err("Wrong operation: " + oprtn)
        cit.bye()


if __name__ == '__main__':
    main()
