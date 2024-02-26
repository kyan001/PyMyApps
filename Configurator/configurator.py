import os
import tomllib

import consoleiotools as cit
import consolecmdtools as cct


__version__ = "1.0.2"
CONFIGURATOR_CONF_NAME = 'configurator.toml'


def _soft_raise(text: str):
    """Print the error message, pause the program and exit."""
    cit.err(text)
    cit.pause()
    cit.bye()


def parse_src_or_dst(path_or_cmd: str) -> cct.Path:
    """Parse the source or destination path or command.

    Args:
        path_or_cmd (str): The source or destination path or command.

    Returns:
        cct.Path: The parsed path.
    """
    if not path_or_cmd:
        return None
    if os.path.isfile(path_or_cmd):  # path_or_cmd is a file
        return cct.get_path(path_or_cmd)
    if cct.is_cmd_exist(path_or_cmd):  # path_or_cmd is a command
        return cct.get_path(cct.read_cmd(path_or_cmd).strip())
    return cct.get_path(path_or_cmd)  # path_or_cmd is not a existing file or a valid command, guess it's a file path


def ensure_packages(packages: iter) -> bool:
    """Ensure the given packages are installed.

    Args:
        packages (iter): The packages to install.

    Returns:
        bool: True if all packages are installed, False otherwise.
    """
    for package in packages:
        package_name = package.get('name')
        package_cmd = package.get('cmd')
        package_manager = package.get('manager')
        if cct.is_cmd_exist(package_cmd):
            continue
        cit.info(f"Installing package: {package_name}")
        if package_manager:
            result = cct.install_package(package_name, package_manager)
        else:
            result = cct.install_package(package_name)
        if not result:
            cit.err(f"Failed to install package: {package_name}!")
            return False
    return True


def get_configurator(path: str) -> dict:
    """Get the configurator as a dict.

    Args:
        path (str): The path of the configurator config file.

    Returns:
        dict: The configurator config.
    """
    EXAMPLE_CONF_URL = "https://github.com/kyan001/PyMyApps/raw/master/Configurator/configurator.toml"
    configurator_conf_path = cct.get_path(path)
    if not configurator_conf_path.exists:
        cit.warn(f"Configurator config file `{path}` not found!")
        cit.info(f"Creating default config file `{path}`")
        with open(configurator_conf_path, 'w') as fl:
            fl.write(cct.read_url(EXAMPLE_CONF_URL).decode())
            cit.info(f"Example `{path}` created!")
        cit.panel(f"Please update `{path}` and run this script again!")
        cit.pause()
        cit.bye()
    with open(configurator_conf_path, 'rb') as fl:
        configurator = tomllib.load(fl)
    if not configurator:
        _soft_raise(f"Bad configurator config file `{path}`!")
    # attribute validation and calibration
    if not configurator.get('name'):
        configurator['name'] = configurator_conf_path.parent.basename
    if configurator.get('install'):
        for package in configurator.get('install'):
            if not package.get('name'):
                _soft_raise(f"Package name not found in {package}!")
            if not package.get('cmd'):
                package['cmd'] = package['name']
    if configurator.get('config'):
        for config in configurator.get('config'):
            if not config.get('src'):
                _soft_raise(f"Source config file path not found in {config}!")
            src = parse_src_or_dst(config.get('src'))
            if not src.exists and not os.path.isabs(config.get('src')):  # try to find the source file in the same directory as the configurator config file
                src = cct.get_path(os.path.join(configurator_conf_path.parent, config.get('src')))
            if not src.exists:
                _soft_raise(f"Source config file not found: {src}!")
            config['src'] = src
            if not config.get('dst'):
                _soft_raise(f"Destination config file path not found in {config}!")
            config['dst'] = parse_src_or_dst(config.get('dst'))
            if not config.get('name'):
                config['name'] = src.basename
    return configurator


def discover_configurator_confs(pattern: str = CONFIGURATOR_CONF_NAME, root: str = "") -> list[str]:
    """Discover configurator config files in the given directory or its subdirectories.

    Args:
        pattern (str, optional): The name of the configurator config file. Defaults to CONFIGURATOR_CONF_NAME.
        root (str, optional): The directory to search. Defaults to "".

    Returns:
        list[str]: A list of configurator config file paths.
    """
    if not root:
        root = cct.get_path(__file__).parent
    configurator_conf_paths = []
    for path in cct.bfs_walk(root):
        path = cct.get_path(path)
        if path.basename == pattern:
            configurator_conf_paths.append(path)
    return configurator_conf_paths


def run_configrator(configurator_conf_path: str):
    """Run the configurator.

    Args:
        configurator_conf_path (str): The path of the configurator config file.
    """
    # configurator info
    configurator = get_configurator(configurator_conf_path)
    cit.rule(f"{configurator.get('name')} Configurator")
    cit.info(f"Folder: {configurator_conf_path.parent}")
    if dependencies := configurator.get('install'):
        cit.info(f"Dependencies: {[package.get('name') for package in dependencies]}")
    if configlets :=configurator.get("config"):
        cit.info(f"Configs: {[configlet.get('name') for configlet in configlets]}")

    # install dependencies
    if dependencies and not ensure_packages(dependencies):
        _soft_raise("Failed to install dependencies!")

    # update config files
    if configlets:
        for configlet in configlets:
            cit.start()
            cit.title(f"Configurating {configlet.get('name')}")
            cit.info(f"Source: `{configlet.get('src')}`")
            cit.info(f"Destination: `{configlet.get('dst')}`")
            src = configlet.get('src')
            dst = configlet.get('dst')
            if src.exists and dst.exists:
                diffs = cct.diff(dst, src)
                if diffs:
                    cit.info("Diff:")
                    cit.print("\n".join(diffs))
                    if cit.get_input("Update config file? (y/n)", default='y').lower() != 'y':
                        cit.warn(f"Config file for `{configlet.get('name')}` is not updated!")
                        continue
                else:
                    cit.info(f"Config file for `{configlet.get('name')}` is up-to-date!")
                    continue
            cct.copy_file(src, dst, backup=True, ensure=True, msgout=cit.info)


def main():
    avail_configurator_conf_paths = discover_configurator_confs()
    if len(avail_configurator_conf_paths) == 0:
        cit.warn("No configurator config file found!")
    elif len(avail_configurator_conf_paths) == 1 and cct.get_path(avail_configurator_conf_paths[0]).parent == (cct.get_path(__file__).parent):
        run_configrator(avail_configurator_conf_paths[0])
    else:
        cit.ask("Which configurator to use?")
        configurator_conf_paths = cit.get_choices(avail_configurator_conf_paths, allable=True, exitable=True)
        for configurator_conf_path in configurator_conf_paths:
            run_configrator(configurator_conf_path)


if __name__ == "__main__":
    main()
    cit.pause()
