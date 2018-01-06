#!/usr/bin/env python3
"""Run develop commands for django project"""
import os
import sys
import socket
import webbrowser
import threading
import urllib.request
import hashlib
import functools

import consoleiotools as cit
from KyanToolKit import KyanToolKit as ktk


__version__ = '1.7.0'
DATADUMP = 'datadump.json'
TESTS_DIR = 'main.tests'
PIP_REQUIREMENTS = 'requirements.pip'


def manage_file_exist():
    """Detect if django project manage.py file exist

    returns
        bool: manage.py is under current path
    """
    return os.path.exists('./manage.py')


@cit.as_session('Update djangoTool.py')
def update_this():
    def compare(s1, s2):
        return s1 == s2, len(s2) - len(s1)

    url = "https://raw.githubusercontent.com/kyan001/PyMyApps/master/DjangoTool/djangoTool.py"
    try:
        req = urllib.request.urlopen(url)
        raw_codes = req.read()
        with open(__file__, 'rb') as f:
            current_codes = f.read().replace(b'\r', b'')
        is_same, diff = compare(current_codes, raw_codes)
        if is_same:
            cit.info("djangoTool.py is already up-to-date.")
        else:
            cit.ask("djangoTool.py has a newer version. Update? ({} char added)".format(diff))
            if cit.get_choice(['Yes', 'No']) == 'Yes':
                with open(__file__, 'wb') as f:
                    f.write(raw_codes)
                cit.info("Update Success.")
                run_by_py3(__file__)
                cit.bye()
            else:
                cit.warn("Update Canceled")
    except Exception as e:
        cit.err("djangoTool.py update failed: {}".format(e))


@cit.as_session('Installing Requirements')
def requirements_install():
    """Install necessary modules by pip & requirements.pip"""
    if not os.path.exists('./{}'.format(PIP_REQUIREMENTS)):
        cit.err('No {} detected.'.format(PIP_REQUIREMENTS))
        cit.bye()
    if 'win' in sys.platform:
        ktk.runCmd('pip3 install -r {}'.format(PIP_REQUIREMENTS))
    else:
        ktk.runCmd('sudo pip3 install -r {}'.format(PIP_REQUIREMENTS))


def run_by_py3(cmd):
    py3_cmd = 'py' if 'win32' in sys.platform else 'python3'
    ktk.runCmd("{py3} {cmd}".format(py3=py3_cmd, cmd=cmd))


@cit.as_session('Runserver localhost')
def runserver_dev():
    """Runserver in development environment, only for localhost debug use"""
    run_by_py3('manage.py runserver')
    webbrowser.open('http://127.0.0.1:8000/')


@cit.as_session('Runserver LAN')
def runserver_lan():
    """Runserver in development environment, for Local Area Network debug use"""
    my_ip = socket.gethostbyname(socket.gethostname())
    cit.info('Your LAN IP address: {}'.format(my_ip))
    run_by_py3('manage.py runserver 0.0.0.0:8000')


@cit.as_session('Run Testcases')
def run_testcases():
    """Run Django testcases"""
    run_by_py3('-Wall manage.py test {} --verbosity 2'.format(TESTS_DIR))


@cit.as_session('Dump Data')
def dump_data():
    """Dump Database data to a json file"""
    run_by_py3('manage.py dumpdata main > {}'.format(DATADUMP))


@cit.as_session('Load Data')
def load_data():
    """Load Database data from a json file"""
    run_by_py3('manage.py loaddata {}'.format(DATADUMP))


@cit.as_session('Retrieve Data')
def retrieve_data():
    """Retrieve dumped data file from remote server"""
    server_info = {
        'addr': cit.get_input('Server:'),
        'username': cit.get_input('Username:'),
        'dir': cit.get_input('File Dir:'),
    }
    if server_info['dir'][-1] == '/':
        server_info['dir'] = server_info['dir'][:-1]
    ktk.runCmd('scp {username}@{addr}:{dir}/{dd} .'.format(**server_info, dd=DATADUMP))


@cit.as_session('Git Assume Unchanged')
def assume_unchanged():
    cit.info('Current assume unchanged files:')
    ktk.runCmd('git ls-files -v | grep -e "^[hsmrck]"')
    filename = cit.get_input("Enter a TRACKED file's filename:")
    ktk.runCmd('git update-index --assume-unchanged {}'.format(filename))


@cit.as_session('Create superuser')
def create_superuser():
    """Create superuser account for Django admin"""
    git_username = cit.get_input('Username:')
    git_email = cit.get_input('Email:')
    run_by_py3('manage.py createsuperuser --username {username} --email {email}'.format(username=git_username, email=git_email))


def show_menu():
    """Show commands menu

    returns:
        a callable function name
    """
    commands = {
        'Install Requirements Modules': requirements_install,
        'Model: Make Migration': functools.partial(run_by_py3, 'manage.py makemigrations'),
        'Model: Migrate': functools.partial(run_by_py3, 'manage.py migrate'),
        'Create superuser account': create_superuser,
        'Runserver (localhost:8000)': runserver_dev,
        'Runserver (LAN ip:8000)': runserver_lan,
        'Shell: Interactive': functools.partial(run_by_py3, 'manage.py shell'),
        'Shell: DB': functools.partial(run_by_py3, 'manage.py dbshell'),
        'Run Testcases': run_testcases,
        'Django system check': functools.partial(run_by_py3, 'manage.py check'),
        'DB Data: Dump (App:main)': dump_data,
        'DB Data: Load ({})'.format(DATADUMP): load_data,
        'DB Data: Retrieve (scp {})'.format(DATADUMP): retrieve_data,
        'Git: Assume Unchanged': assume_unchanged,
        '*** Update djangoTool.py ***': update_this,
    }
    menu = sorted(commands.keys())
    if len(sys.argv) > 1:
        arg = sys.argv.pop()
        selection = arg if arg in commands else menu[int(arg) - 1]
    else:
        cit.echo('Select one of these:')
        selection = cit.get_choice(menu)
    return commands.get(selection)


def main():
    ktk.clearScreen()
    cit.echo('Django Tool: version {}'.format(__version__))
    cit.br()
    if not manage_file_exist():
        cit.err('No manage.py detected. Please run this under projects folder')
        cit.bye()
    try:
        while True:
            to_run = show_menu()
            to_run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
