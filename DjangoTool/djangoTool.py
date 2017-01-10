#!/usr/bin/env python3
"""Run develop commands for django project"""
import os
import sys
import collections
import socket

import consoleiotools as cit
from KyanToolKit import KyanToolKit as ktk


__version__ = '1.2.1'


def manage_file_exist():
    """Detect if django project manage.py file exist

    returns
        bool: manage.py is under current path
    """
    return os.path.exists('./manage.py')


@cit.as_session('Installing Requirements')
def requirements_install():
    """Install necessary modules by pip & requirements.pip"""
    if not os.path.exists('./requirements.pip'):
        cit.err('No requirements.pip detected.')
        cit.bye()
    if 'win' in sys.platform:
        ktk.runCmd('pip3 install -r requirements.pip')
    else:
        ktk.runCmd('sudo pip3 install -r requirements.pip')


def run_by_py3(cmd):
    py3_cmd = 'py' if 'win32' in sys.platform else 'python3'
    ktk.runCmd("{py3} {cmd}".format(py3=py3_cmd, cmd=cmd))


@cit.as_session('Applying changes to database')
def migrate_db():
    """Apply changes to database"""
    run_by_py3('manage.py makemigrations')
    run_by_py3('manage.py migrate')


@cit.as_session('Enter DB shell')
def db_shell():
    """Enter Django database shell mode"""
    run_by_py3('manage.py dbshell')


@cit.as_session('Enter interactive shell')
def interactive_shell():
    """Enter Django shell mode"""
    run_by_py3('manage.py shell')


@cit.as_session('Runserver localhost')
def runserver_dev():
    """Runserver in development environment, only for localhost debug use"""
    run_by_py3('manage.py runserver')


@cit.as_session('Runserver LAN')
def runserver_lan():
    """Runserver in development environment, for Local Area Network debug use"""
    my_ip = socket.gethostbyname(socket.gethostname())
    cit.info('Your LAN IP address: {}'.format(my_ip))
    run_by_py3('manage.py runserver 0.0.0.0:8000')


@cit.as_session('System Checking')
def system_check():
    """Check if django projects has a problem"""
    run_by_py3('manage.py check')

@cit.as_session('Dump Data')
def dump_data():
    """Dump Database data to a json file"""
    run_by_py3('manage.py dumpdata > datadump.json')


@cit.as_session('Load Data')
def load_data():
    """Load Database data from a json file"""
    run_by_py3('manage.py loaddata datadump.json')


@cit.as_session('Create superuser')
def create_superuser():
    """Create superuser account for Django admin"""
    git_username = cit.get_input('Username:')
    git_email = cit.get_input('Email:')
    cit.info('Password is specified, ask someone for it')
    run_by_py3('manage.py createsuperuser --username {username} --email {email}'.format(username=git_username, email=git_email))


def show_menu():
    """Show commands menu

    returns:
        a callable function name
    """
    commands = collections.OrderedDict({
        'Install Requirements Modules': requirements_install,
        'Make & migrate database': migrate_db,
        'Create superuser account': create_superuser,
        'Runserver (localhost:8000)': runserver_dev,
        'Runserver (LAN ip:8000)': runserver_lan,
        'Shell: Interactive': interactive_shell,
        'Shell: DB': db_shell,
        'Django system check': system_check,
        'DB Data Dump': dump_data,
        'DB Data Load': load_data,
        'Exit': cit.bye,
    })
    cit.echo('Select one of these:')
    selection = cit.get_choice(sorted(commands.keys()))
    return commands.get(selection)


def main():
    ktk.clearScreen()
    cit.echo('Django Tool: version {}'.format(__version__))
    cit.br()
    if not manage_file_exist():
        cit.err('No manage.py detected. Please run this under projects folder')
        cit.bye()
    while True:
        to_run = show_menu()
        to_run()


if __name__ == '__main__':
    main()
