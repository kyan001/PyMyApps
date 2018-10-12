import os
import json
import cson

__version__ = "1.2.1"
BOOSTNOTE_JSON = "boostnote.json"
NOTES_FOLDER = "notes"
TARGET_FOLDER = "notes_unboosted"
MARKDOWN_TYPE = "MARKDOWN_NOTE"


class Note:
    def __init__(self, dict_: dict=None):
        if dict_:
            for k in dict_:
                self.__dict__[k] = dict_[k]

    def __str__(self):
        return str(self.__dict__)


class MarkdownNote:
    def __init__(self, boostnote=None):
        if boostnote:
            self.from_boost(boostnote)

    def from_boost(self, boostnote):
        self.note = boostnote.note

    def to_file(self, filepath):
        if not filepath:
            raise Exception("Filepath cannot be empty")
        if not self.note:
            raise Exception("Note info not found")
        dirname = os.path.dirname(filepath)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(filepath, mode='w', encoding='utf-8') as fl:
            fl.write(self.note.content)


class BoostNote:
    def __init__(self, filepath=None):
        if filepath:
            self.from_file(filepath)

    def from_file(self, cson_filepath):
        if not os.path.isfile(cson_filepath):
            raise Exception("file not found")
        if not cson_filepath.endswith(".cson"):
            raise Exception("file must be .cson")
        with open(cson_filepath, mode="rb") as fl:
            self.note = Note(cson.load(fl))  # "title", "type", "folder", "content", "isTrashed", "isStarred", "tags", "createdAt", "updatedAt"


class BoostConf:
    def __init__(self, filepath=None):
        self.__subfolders = {}
        if filepath:
            self.from_file(filepath)

    def from_file(self, json_filepath):
        if not os.path.isfile(json_filepath):
            raise Exception("file not found")
        if not json_filepath.endswith(".json"):
            raise Exception("file must be .json")
        with open(json_filepath, mode='r', encoding='utf-8') as fl:
            conf = json.loads(fl.read())
            self.folders = conf.get("folders")
            self.version = conf.get("version")

    @property
    def subfolders(self):
        if not self.__subfolders:
            for info in self.folders:
                self.__subfolders[info.get("key")] = info.get("name")
        return self.__subfolders


if __name__ == "__main__":
    # boostnote/notes folder check
    if not os.path.isdir(NOTES_FOLDER):
        raise Exception("Can only executed under Boostnote folder")

    # Generated Notes Folder check
    if os.path.isdir(TARGET_FOLDER):
        BACKUP_FOLDER = TARGET_FOLDER + '.backup'
        if os.path.isdir(BACKUP_FOLDER):
            os.remove(BACKUP_FOLDER)
        os.rename(TARGET_FOLDER, BACKUP_FOLDER)

    # Get boostnote configs
    boostconf = BoostConf(BOOSTNOTE_JSON)

    # Convert each note
    note_filenames = os.listdir(NOTES_FOLDER)
    for note_filename in note_filenames:
        bn = BoostNote(os.path.join(NOTES_FOLDER, note_filename))
        if bn.note.isTrashed:
            continue
        if bn.note.type == MARKDOWN_TYPE:
            mdn = MarkdownNote(bn)
            mdn.note.title = bn.note.title
            mdn.note.folder = boostconf.subfolders.get(bn.note.folder)
            mdn.note.content = bn.note.content
            filename = mdn.note.title.replace(" ", "_").replace(".", "_").replace("/", "_") + ".md"
            filepath = os.path.join(TARGET_FOLDER, mdn.note.folder, filename)
            mdn.to_file(filepath)
