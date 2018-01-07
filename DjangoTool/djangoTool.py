#!/usr/bin/env python3
"""Run develop commands for django project"""
import os
import sys
import socket
import webbrowser
import urllib.request
import hashlib
import functools

import consoleiotools as cit
from KyanToolKit import KyanToolKit as ktk


__version__ = '1.9.1'
DATADUMP = 'datadump.json'
TESTS_DIR = 'main.tests'
PIP_REQUIREMENTS = 'requirements.pip'
COMMANDS = {'-- Exit --': cit.bye}  # Dict of menu commands.


def manage_file_exist():
    """Detect if django project manage.py file exist

    Returns
        bool: manage.py is under current path
    """
    return os.path.exists('./manage.py')


def register(desc_or_func):
    """reg func into command menu dict

    Usage:
        @register('description')
        def func():

        @register
        def func():

    Globals:
        COMMANDS: Dict of menu commands.
            KEY: desc / the 1st line of func.__doc__ / func.__name__
            VAL: func
    """
    if callable(desc_or_func):
        func = desc_or_func
        desc = func.__doc__ or func.__name__
        desc = desc.replace('\t', '').split('\n')[0]
        return register(desc)(func)
    else:
        desc = desc_or_func

    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        COMMANDS[desc] = func
        return wrapper
    return deco


def run_by_py3(cmd):
    ktk.runCmd("{py3} {cmd}".format(py3=ktk.getPyCmd(), cmd=cmd))


def show_menu():
    """Show commands menu

    Globals:
        COMMANDS: Dict of menu commands.
            Key: description of func
            Val: func
    """
    #     'Django system check': functools.partial(run_by_py3, ),
    # }
    menu = sorted(COMMANDS.keys())
    if len(sys.argv) > 1:
        arg = sys.argv.pop()
        selection = arg if arg in COMMANDS else menu[int(arg) - 1]
    else:
        cit.echo('Select one of these:')
        selection = cit.get_choice(menu)
    return COMMANDS.get(selection)


@register('*** Update djangoTool.py ***')
@cit.as_session
def update_djangotool():
    """Check and update djangoTool.py from github"""
    url = "https://raw.githubusercontent.com/kyan001/PyMyApps/master/DjangoTool/djangoTool.py"
    if ktk.updateFile(__file__, url):
        run_by_py3(__file__)
        cit.bye(0)


@register("Install Requirements Modules")
@cit.as_session
def requirements_install():
    """Install necessary modules by pip with requirements.pip

    Globals:
        PIP_REQUIREMENTS: the filename of requirements.pip
    """
    if not os.path.exists('./{}'.format(PIP_REQUIREMENTS)):
        cit.err('No {} detected.'.format(PIP_REQUIREMENTS))
        cit.bye()
    if 'win' in sys.platform:
        ktk.runCmd('pip3 install -r {}'.format(PIP_REQUIREMENTS))
    else:
        ktk.runCmd('sudo pip3 install -r {}'.format(PIP_REQUIREMENTS))


@register('Runserver (localhost:8000)')
@cit.as_session
def runserver_dev():
    """Runserver in development environment, only for localhost debug use"""
    webbrowser.open('http://127.0.0.1:8000/')
    run_by_py3('manage.py runserver')


@register('Runserver (LAN ip:8000)')
@cit.as_session
def runserver_lan():
    """Runserver in development environment, for Local Area Network debug use"""
    my_ip = socket.gethostbyname(socket.gethostname())
    cit.info('Your LAN IP address: {}'.format(my_ip))
    run_by_py3('manage.py runserver 0.0.0.0:8000')


@register
@cit.as_session
def run_testcases():
    """Run Django Testcases"""
    run_by_py3('-Wall manage.py test {} --verbosity 2'.format(TESTS_DIR))


@register('DB Data: Dump (App:main)')
@cit.as_session
def dump_data():
    """Dump Database data to a json file

    Globals:
        DATADUMP: the filename of target json file
    """
    run_by_py3('manage.py dumpdata main > {}'.format(DATADUMP))


@register('DB Data: Load (App:main)')
@cit.as_session
def load_data():
    """Load Database data from a json file

    Globals:
        DATADUMP: the filename of target json file
    """
    run_by_py3('manage.py loaddata {}'.format(DATADUMP))


@register('DB Data: Retrieve (by scp)')
@cit.as_session
def retrieve_data():
    """Retrieve dumped data file from remote server

    Globals:
        DATADUMP: the filename of target json file
    Inputs:
        addr: Server IP / Address
        username: username on server
        dir: dir on server, DATADUMP file should in it.
    """
    server_info = {
        'addr': cit.get_input('Server:'),
        'username': cit.get_input('Username:'),
        'dir': cit.get_input('File Dir:'),
    }
    if server_info['dir'][-1] == '/':
        server_info['dir'] = server_info['dir'][:-1]
    ktk.runCmd('scp {username}@{addr}:{dir}/{dd} .'.format(**server_info, dd=DATADUMP))


@register('Git: Assume Unchanged')
@cit.as_session
def assume_unchanged():
    """Show and add a file to 'No-tracking' in Git"""
    cit.info('Current assume unchanged files:')
    ktk.runCmd('git ls-files -v | grep -e "^[hsmrck]"')
    filename = cit.get_input("Enter a TRACKED file's filename: (Ctrl + C to stop)")
    ktk.runCmd('git update-index --assume-unchanged {}'.format(filename))


@register
@cit.as_session
def create_superuser():
    """Create Superuser Account

    Superuser is a user in Django User System with superuser flag.
    Asks: username / email / password for the new superuser
    """
    username = cit.get_input('Username:')
    email = cit.get_input('Email:')
    run_by_py3('manage.py createsuperuser --username {username} --email {email}'.format(username=username, email=email))


@register('Model: Make Migration')
@cit.as_session
def make_migration():
    """make migration: detect and generate changes of models"""
    run_by_py3('manage.py makemigrations')


@register('Model: Migrate')
@cit.as_session
def migrate():
    """migrate: apply models changes to database"""
    run_by_py3('manage.py migrate')


@register('Shell: Interactive')
@cit.as_session
def interactive_shell():
    """Enter interactive shell mode

    Example Commands:
        >>> from main.models import User
        >>> User.objects.all()
    """
    run_by_py3('manage.py shell')


@register('Shell: Database')
@cit.as_session
def database_shell():
    """Enter the database's shell mode

    Example Commands:
        MySQL> select * from User;
    """
    run_by_py3('manage.py dbshell')


@register
@cit.as_session
def system_check():
    """Django System Check"""
    run_by_py3('manage.py check')


if __name__ == '__main__':
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
        cit.info('Thanks for using. Bye bye!')
        cit.bye(0)
