from KyanToolKit import KyanToolKit as ktk
import consoleiotools as cit


class Updater:
    @classmethod
    def _exe(cls, arg: str):
        cmd = f"{cls.base_cmd} {arg}"
        ktk.runCmd(cmd)

    @classmethod
    def _read_cmd(cls, arg: str) -> str:
        cmd = f"{cls.base_cmd} {arg}"
        return ktk.readCmd(cmd)

    @classmethod
    def is_available(cls):
        return cls.base_cmd and ktk.isCmdExist(cls.base_cmd)

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


class BrewUpdater(Updater):
    base_cmd = 'brew'

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
    def upgrade(cls, pkg):
        if not pkg:
            raise Exception("package name cannot be empty.")
        cls._exe(f'upgrade {pkg}')


class BrewcaskUpdater(Updater):
    base_cmd = 'brew cask'

    @classmethod
    def list_outdated(cls):
        cls._exe('outdated')

    @classmethod
    def self_update(cls):
        pass

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
    def list_outdated(cls):
        cls._exe('list --outdated')

    @classmethod
    def self_update(cls):
        cls._exe('install --upgrade pip')

    @classmethod
    def upgrade_all(cls):
        # TODO
        pass

    @classmethod
    def upgrade(cls, pkg):
        if not pkg:
            raise Exception("package name cannot be empty.")
        cls._exe(f'install --upgrade {pkg}')


class NvmUpdater(Updater):
    base_cmd = 'nvm'

    @classmethod
    def list_outdated(cls):
        cls._exe('ls')

    # TODO
    pass


class ChocoUpdater(Updater):
    base_cmd = 'choco'

    # TODO
    pass
