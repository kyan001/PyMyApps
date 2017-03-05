import configparser
import os
import cmd
import tkinter
import tkinter.filedialog

import consoleiotools as cit


class CONF(object):
    DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')
    CONFIGFILE = 'yougetter.ini'
    GFWSITES = ['youtube', 'tumblr', 'twitter']
    proxy = None
    folder = DESKTOP_PATH
    name = None
    url = None
    itag = None
    use_proxy = False
    debug = False

    @classmethod
    def attr(cls, key, value=None):
        if value is None:
            return getattr(cls, key)
        else:
            return setattr(cls, key, value)

    @classmethod
    def try_set(cls, key, example="", value=None):
        old_value = cls.attr(key)
        cit.info('Current {k} is: "{v}"'.format(k=key, v=old_value))
        if not value:
            cit.ask('Enter a {k}: (Leave blank if no change)'.format(k=key))
            if example:
                cit.ask('Example: {}'.format(example))
            new_value = cit.get_input()
        else:
            new_value = value
        if new_value:
            new_value = True if new_value == 'yes' else new_value
            new_value = False if new_value == 'no' else new_value
            cls.attr(key, new_value)
        if new_value == old_value:
            cit.info('{k} is not changed'.format(k=key))
        else:
            cit.info('New {k} is: "{v}"'.format(k=key, v=cls.attr(key)))


class InteractiveShell(cmd.Cmd):
    HELP_MSG = """
[ Commands List ] __________________________
    ? / help : Show all commands
    ---------:---------------------------
      config : Show current config info
        info : Show the url info and all the qualities
    ---------:---------------------------
         url : Set URL which needs to be downloaded
       proxy : Set proxy for oversea sites
      folder : Set where to save the downloaded files
        name : Set the filename of the savedfiles
        itag : Set itag to download with a different quality
       debug : Set if this run in debug mode
    ---------:---------------------------
         get : Get the recommanded video to target folder
      youget : Direct using you-get <arg>
        exit : Exit
    """

    def __init__(self):
        super().__init__(self)
        self.prompt = self.HELP_MSG + 'YouGetter> '
        self.onecmd('url')

    def precmd(self, line):
        cit.br()
        cit.start()
        return line.lower()

    def postcmd(self, stop, line):
        cit.end()
        cit.br()
        return stop

    def do_youget(self, arg=None):
        """Direct using you-get <arg>"""
        os.system('you-get {}'.format(arg))

    def do_config(self, arg=None):
        """Show current config info"""
        attrs = ["proxy", "folder", "name", "url", "itag", "use_proxy", "debug"]
        cit.title('Current Configs')
        for key in attrs:
            cit.info('{k}\t: {v}'.format(k=key, v=CONF.attr(key)))
        cit.pause()

    def do_info(self, arg=None):
        """Show the url info and all the qualities"""
        cmd = 'you-get --info'
        cmd += ' --http-proxy "{}"'.format(CONF.proxy) if CONF.use_proxy and CONF.proxy else ""  # -x
        cmd += ' --debug' if CONF.debug else ""
        cmd += ' "{}"'.format(CONF.url)
        os.system(cmd)

    def do_get(self, arg=None):
        """Get the recommanded video to target folder"""
        if CONF.url:
            cmd = 'you-get'
            cmd += ' --output-dir "{}"'.format(CONF.folder) if CONF.folder else ""  # -o
            cmd += ' --output-filename "{}"'.format(CONF.name) if CONF.name else ""  # -O
            cmd += ' --http-proxy "{}"'.format(CONF.proxy) if CONF.use_proxy and CONF.proxy else ""  # -x
            cmd += ' --itag={}'.format(CONF.itag) if CONF.itag else ""
            cmd += ' --debug' if CONF.debug else ""
            cmd += ' "{}"'.format(CONF.url)
            cit.info('Final command:')
            cit.echo(cmd)
            cit.ask('Is this look good?')
            answer = cit.get_choice(['Yes', 'No'])
            if answer == 'Yes':
                os.system(cmd)
                self.do_exit()
            else:
                cit.warn('Canceled')
            cit.pause()
        else:
            cit.err('You must specified a url first')
            return self.onecmd('url')

    def do_url(self, arg=None):
        """Enter the URL which needs to be downloaded"""
        CONF.try_set('url', example='https://www.youtube.com/watch?v=abcdefg', value=arg)
        if not CONF.url:
            cit.err('You must specified a URL')
            return self.onecmd('url')
        for site in CONF.GFWSITES:
            if site in CONF.url:
                CONF.use_proxy = True
                break
            CONF.use_proxy = False

    def do_folder(self, arg=None):
        """Set where to save the downloaded files"""
        if CONF.folder:
            cit.info('Current folder is: {}'.format(CONF.folder))
        cit.ask('What do you want to do with the folder:')
        selections = {
            'keep': 'Keep this',
            'desktop': 'Save to my Desktop',
            'independent': 'Independent folder on my Desktop',
            'select': 'Select my own',
            'enter': 'Enter a new one',
        }
        next_step = cit.get_choice(list(sorted(selections.values())))
        if next_step == selections['enter']:
            cit.ask('Enter a name: (Leave blank if no-change)')
            cit.ask('example: TokyoHot')
            new_folder = cit.get_input()
        elif next_step == selections['keep']:
            pass
        elif next_step == selections['desktop']:
            new_folder = CONF.DESKTOP_PATH
        elif next_step == selections['independent']:
            name = CONF.name if CONF.name else cit.get_input('Enter a folder name:')
            new_folder = os.path.join(CONF.DESKTOP_PATH, name)
        elif next_step == selections['select']:
            tkapp = tkinter.Tk()
            new_folder = tkinter.filedialog.askdirectory(initialdir='CONF.DESKTOP_PATH')
            tkapp.destroy()
        if new_folder and CONF.folder != new_folder:
            CONF.folder = new_folder
            cit.info('Folder has set to "{}"'.format(CONF.folder))
        else:
            cit.info('Folder has not changed')
        if not os.path.isdir(CONF.folder):
            cit.warn('Folder does not exist, created')
            os.makedirs(CONF.folder)

    def do_debug(self, arg=None):
        """Set if this run in debug mode"""
        CONF.try_set('debug', example='yes/no', value=arg)

    def do_itag(self, arg=None):
        """Set itag to download with a different quality"""
        CONF.try_set('itag', example='127 (no or 0 for not use)', value=arg)

    def do_proxy(self, arg=None):
        """Set proxy for oversea sites"""
        CONF.try_set('proxy', example='127.0.0.1:1080', value=arg)

    def do_name(self, arg=None):
        """Set the filename of the savedfiles"""
        CONF.try_set('name', example='hyouka_S01E01.mp4', value=arg)

    def do_exit(self, arg=None):
        return True


@cit.as_session('Loading configs')
def load_config():
    """Loading config from configfile into CONF"""
    cit.info('Config file is {}'.format(CONF.CONFIGFILE))
    config = configparser.ConfigParser()
    if os.path.isfile(CONF.CONFIGFILE):
        config.read(CONF.CONFIGFILE)
        if config.has_section('proxy'):
            sect = config['proxy']
            proxy_ip = sect.get('ip')
            proxy_port = sect.get('port')
            CONF.proxy = "{}:{}".format(proxy_ip, proxy_port)


def main():
    load_config()
    InteractiveShell().cmdloop()


if __name__ == '__main__':
    main()
