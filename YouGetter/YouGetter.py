import configparser
import os
import cmd
import sys
import platform

import consoleiotools as cit

TARGET_FOLDER = "Desktop" if sys.platform.startswith('win') else "Downloads"
DEFAULT_PATH = os.path.join(os.path.expanduser('~'), TARGET_FOLDER)
CONFIG_FILE = 'yougetter.ini'
GFW_SITES = ('youtube.com', 'tumblr.com', 'twitter.com')


class InteractiveShell(cmd.Cmd):
    HELP_MSG = """[ Commands List ] __________________________
    ? / help : Show all commands
    ---------:---------------------------
     configs : Show current configs.
        info : Show the url info and all the qualities.
    ---------:---------------------------
         url : Set URL which needs to be downloaded.
       proxy : Set proxy for oversea sites.
      folder : Set where to save the downloaded files.
    filename : Set filename for the saved file.
        itag : Set itag to download with a different quality.
      format : Set format download with a different format.
     cookies : Set cookies for download.
    playlist : Set playlist mode for multi-video download.
       debug : Set if this run in debug mode.
    insecure : Set to ignore ssl errors.
    ---------:---------------------------
         run : Run you-get command and start downloading.
      dryrun : See the command.
        exit : Exit.
    """

    def __init__(self):
        super().__init__()
        self.config = {
            "proxy": None,
            "use_proxy": False,
            "folder": DEFAULT_PATH,
            "filename": None,
            "url": None,
            "itag": None,
            "debug": False,
            "cookies": None,
            "playlist": False,
            "insecure": False,
        }
        self.load_config()
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

    def make_command(self):
        command = 'you-get'
        command += f' --output-dir \"{self.config.get("folder")}\"' if self.config.get('folder') else ""  # -o
        command += f' --output-filename \"{self.config.get("filename")}\"' if self.config.get('filename') else ""  # -O
        command += f' --http-proxy \"{self.config.get("proxy")}\"' if self.config.get('use_proxy') and self.config.get('proxy') else ""  # -x
        command += f' --itag={self.config.get("itag")}' if self.config.get('itag') else ""
        command += f' --format={self.config.get("format")}' if self.config.get('format') else ""
        command += f' --cookies \"{self.config.get("cookies")}\"' if self.config.get('cookies') else ""  # -c
        command += ' --debug' if self.config.get('debug') else ""
        command += ' --insecure' if self.config.get('insecure') else ""  # -k
        command += ' --playlist' if self.config.get('playlist') else ""
        command += f' \"{self.config.get("url")}\"'
        return command

    def get_path_input(self, mode="file", default=None):
        cit.ask('Select one of the following:')
        selections = {
            'cancel': 'Cancel',
            'select': 'Select my own',
            'enter': 'Enter a new one',
        }
        if default:
            selections['default'] = f'Set to {default}'
        new_path = ""
        selection = cit.get_choice(list(sorted(selections.values())))
        if selection == selections.get('enter'):
            cit.ask('Enter a path: (Leave blank if no-change)')
            new_path = cit.get_input()
        elif selection == selections.get('cancel'):
            return None
        elif selections.get('default') and selection == selections.get('default'):
            new_path = default
        elif selection == selections.get('select'):
            import tkinter
            import tkinter.filedialog
            tkapp = tkinter.Tk()
            initial_dir = default or DEFAULT_PATH
            if mode == 'folder':
                new_path = tkinter.filedialog.askdirectory(initialdir=initial_dir)
            elif mode == 'file':
                new_path = tkinter.filedialog.askopenfilename(initialdir=initial_dir)
            tkapp.destroy()
        else:
            raise Exception(f"Selection {selection} is not valid.")
        if not new_path:
            return self.get_path_input(mode, default)
        if mode == 'folder' and not os.path.isdir(new_path):
            cit.warn('Folder does not exist.')
            cit.ask(f'Create `{new_path}`?')
            if cit.get_choice(['Yes', 'No']) == 'Yes':
                os.makedirs(new_path)
                cit.info(f"Folder create: {new_path}")
            else:
                cit.warn("Folder is NOT created.")
        if mode == 'file' and not os.path.isfile(new_path):
            cit.warn('File does not exist.')
        return new_path

    @cit.as_session
    def load_config(self):
        """Loading config from config file into config"""
        if not CONFIG_FILE:
            return None
        cit.info(f'Config file is {CONFIG_FILE}')
        if not os.path.isfile(CONFIG_FILE):
            cit.err("Config file does not exist.")
            return None
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        if config.has_section('proxy'):
            sect = config['proxy']
            proxy_ip = sect.get('ip')
            proxy_port = sect.get('port')
            if proxy_ip and proxy_port:
                self.config['proxy'] = f"{proxy_ip}:{proxy_port}"
                cit.info(f"Config Loaded: proxy={self.config['proxy']}")
            else:
                cit.warn("Config Load Failed: `proxy` unchanged.")
        if config.has_section('folder'):
            sect = config['folder']
            folder_win = sect.get('win')  # Folder for Windows
            folder_linux = sect.get('linux')  # Folder for Linux
            folder_mac = sect.get('mac')  # Folder for macOS
            if folder_win and sys.platform.startswith('win'):
                self.config['folder'] = folder_win
                cit.info(f"Config Loaded: folder={self.config['folder']}")
            elif folder_linux and os.name == 'posix':
                self.config['folder'] = folder_linux
                cit.info(f"Config Loaded: folder={self.config['folder']}")
            elif folder_mac and platform.system() == 'Darwin':
                self.config['folder'] = folder_mac
                cit.info(f"Config Loaded: folder={self.config['folder']}")
            else:
                cit.warn("Config Load Failed: `folder` unchanged.")

    def set_config(self, key, val=None, example="", mode=''):
        old_val = self.config.get(key)
        cit.info(f'Current {key} is: `{old_val}`')
        if not val:  # no val provided, ask for input.
            if mode in ('file', 'folder'):
                new_val = self.get_path_input(mode)
            elif mode == 'bool' or isinstance(old_val, bool):
                cit.ask(f'Switch {key} to:')
                new_val = cit.get_choice(["On", "Off"]) == "On"
            else:
                cit.ask(f'Enter a {key}: (Leave blank if no-change)')
                if example:
                    cit.info(f'Ex. {example}')
                new_val = cit.get_input()
        else:  # provided value.
            new_val = val
        if new_val or (new_val is False):  # None and "" will not change.
            self.config[key] = new_val
        if new_val == old_val:
            cit.info(f'`{key}` is NOT changed')
        else:
            cit.info(f'New `{key}` is: "{new_val}"')

    def do_configs(self, arg=None):
        """Show current config info"""
        cit.title('Current Configs')
        for key, val in self.config.items():
            cit.info(f'{key}\t: {val}')
        cit.pause()

    def do_info(self, arg=None):
        """Show the url info and all the qualities"""
        command = self.make_command()
        command += ' --info'
        os.system(command)

    def do_url(self, arg=None):
        """Enter the URL which needs to be downloaded"""
        self.set_config('url', val=arg, example='https://www.youtube.com/watch?v=abcdefg')
        if not self.config.get('url'):
            cit.err('You must specified a URL')
            return self.onecmd('url')
        for site in GFW_SITES:
            if site in self.config['url']:
                self.set_config('use_proxy', True)
                break

    def do_folder(self, arg=None):
        """Set where to save the downloaded files"""
        self.set_config('folder', val=arg, mode='folder')

    def do_itag(self, arg=None):
        """Set itag to download with a different quality"""
        self.set_config('itag', val=arg, example='127 (0 for not use)')

    def do_format(self, arg=None):
        self.set_config('format', val=arg, example='dash-hdflv2')

    def do_cookies(self, arg=None):
        self.set_config('cookies', val=arg, example='/home/user/cookies.sqlite', mode='file')

    def do_proxy(self, arg=None):
        """Set proxy for oversea sites"""
        self.set_config('proxy', val=arg, example='127.0.0.1:1080')

    def do_filename(self, arg=None):
        """Set the filename of the savedfiles"""
        self.set_config('filename', val=arg, example='hyouka_S01E01.mp4')

    def do_debug(self, arg=None):
        """Set if this run in debug mode"""
        self.set_config('debug', val=arg, mode='bool')

    def do_insecure(self, arg=None):
        self.set_config('insecure', val=arg, mode='bool')

    def do_playlist(self, arg=None):
        self.set_config('playlist', val=arg, mode='bool')

    @cit.as_session
    def do_run(self, arg=None, dry: bool = False):
        """Get the recommanded video to target folder"""
        if not self.config.get('url'):
            cit.err('You must specified a URL')
            return self.onecmd('url')
        command = self.make_command()
        cit.info(f'Final command: \n{command}')
        if dry:
            cit.warn("This is a dry run. Command is NOT executed.")
            cit.pause()
            return None
        cit.ask('Does this look good?')
        if cit.get_choice(['Yes', 'No']) == 'Yes':
            os.system(command)
            return self.do_exit()
        else:
            cit.warn('Canceled')
        cit.pause()

    def do_dryrun(self, arg=None):
        return self.do_run(dry=True)

    def do_exit(self, arg=None):
        return True


def main():
    ishell = InteractiveShell()
    ishell.cmdloop()


if __name__ == '__main__':
    main()
