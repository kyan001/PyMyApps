import os

import consolecmdtools as cct
import consoleiotools as cit


class Updater:
    @classmethod
    def _exe(cls, arg: str):
        cmd = f"{cls.base_cmd} {arg}"
        return cct.run_cmd(cmd) == 0

    @classmethod
    def _read_cmd(cls, arg: str) -> str:
        cmd = f"{cls.base_cmd} {arg}"
        return cct.read_cmd(cmd)

    @classmethod
    def is_available(cls):
        return cls.base_cmd and cct.is_cmd_exist(cls.base_cmd)

    @classmethod
    def self_update(cls):
        pass

    @classmethod
    def upgrade_all(cls):
        pass

    @classmethod
    def upgrade(cls, pkg: str):
        pass

    @classmethod
    def list_outdated(cls):
        pass

    @classmethod
    def list_all(cls):
        pass


class BrewUpdater(Updater):
    base_cmd = 'brew'

    @classmethod
    def list_all(cls):
        cls._exe('list')

    @classmethod
    def list_outdated(cls):
        result = cls._read_cmd('outdated')
        cit.info("\n".join(result.split()))
        return True if result else False

    @classmethod
    def self_update(cls):
        cls._exe('update')

    @classmethod
    def upgrade_all(cls):
        cls._exe('upgrade')

    @classmethod
    def upgrade(cls, pkg: str):
        if not pkg:
            raise Exception("package name cannot be empty.")
        cls._exe(f'upgrade {pkg}')


class BrewcaskUpdater(Updater):
    base_cmd = 'brew cask'

    @classmethod
    def list_all(cls):
        cls._exe('list')

    @classmethod
    def list_outdated(cls):
        cls._exe('outdated')

    @classmethod
    def self_update(cls):
        cit.warn("Brew Cask Update Itself by `brew update`")

    @classmethod
    def upgrade_all(cls):
        cls._exe('upgrade')

    @classmethod
    def upgrade(cls, pkg):
        if not pkg:
            raise Exception("package name cannot be empty.")
        cls._exe(f'upgrade {pkg}')


class PipUpdater(Updater):
    base_cmd = 'pip3'

    @classmethod
    def list_all(cls):
        cls._exe('list')

    @classmethod
    def list_outdated(cls):
        cls._exe('list --outdated')

    @classmethod
    def self_update(cls):
        cls._exe('install --upgrade pip')

    @classmethod
    def upgrade_all(cls):
        # TODO
        cit.warn("pip upgrade_all() is TODO")

    @classmethod
    def upgrade(cls, pkg):
        if not pkg:
            raise Exception("package name cannot be empty.")
        cls._exe(f'install --upgrade {pkg}')


class NvmUpdater(Updater):
    nvm_folder = os.path.expanduser('~/.nvm')
    nvm_shell = os.path.join(nvm_folder, 'nvm.sh')
    base_cmd = f'source {nvm_shell}; nvm'

    @classmethod
    def is_available(cls):
        return cls.base_cmd and os.path.exists(cls.nvm_shell)

    @classmethod
    def list_all(cls):
        cls._exe('ls')

    @classmethod
    def list_outdated(cls):
        cls._exe("ls-remote | grep -A 100 -B 2 '\->'")

    @classmethod
    def self_update(cls):
        cct.run_cmd(f"git -C {cls.nvm_folder} pull")

    @classmethod
    def upgrade_all(cls):
        @cit.as_session
        def upgrade_nodejs():
            cit.info("Upgrading Node.js:")
            cit.warn("You can uninstall old node.js by using following command: \n`nvm ls`\n`nvm uninstall <version>`")
            cls._exe('install node')
            cls._exe('use node')

        @cit.as_session
        def upgrade_npm():
            cit.info("Upgradeing NPM:")
            cls._exe("install-latest-npm")

        upgrade_nodejs()
        upgrade_npm()


class ChocoUpdater(Updater):
    base_cmd = 'choco'

    @classmethod
    def list_all(cls):
        cls._exe('list --local')

    @classmethod
    def list_outdated(cls):
        cls._exe('outdated')

    @classmethod
    def self_update(cls):
        cls._exe('upgrade chocolatey')

    @classmethod
    def upgrade_all(cls):
        cit.warn("upgrade all")

    @classmethod
    def upgrade(cls, pkg):
        if not pkg:
            raise Exception("package name cannot be empty.")
        cls._exe(f'upgrade {pkg}')
