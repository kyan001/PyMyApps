import os
import json
import cson

__version__ = "1.1.1"
BOOSTNOTE_JSON = "boostnote.json"
NOTES_FOLDER = "notes"
TARGET_FOLDER = "notes_unboosted"
MARKDOWN_TYPE = "MARKDOWN_NOTE"


class Note:
    def __init__(self, cson_file=None):
        if cson_file:
            if not os.path.isfile(cson_file):
                raise Exception("file not found")
            if not cson_file.endswith(".cson"):
                raise Exception("file must be .cson")
            self.spath = cson_file
            with open(cson_file, mode="rb") as fl:
                boost_cson = cson.load(fl)
            self.title = boost_cson.get("title")
            self.type = boost_cson.get("type")
            self.folder = boost_cson.get("folder")
            self.content = boost_cson.get("content")
            self.is_trashed = boost_cson.get("isTrashed")
            self.is_starred = boost_cson.get("isStarred")
            self.tags = boost_cson.get("tags")
            self.created_at = boost_cson.get("createdAt")
            self.updated_at = boost_cson.get("updatedAt")

    def overwrite(self):
        if self.tpath and self.content:
            dirname = os.path.dirname(self.tpath)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            with open(self.tpath, mode='w', encoding='utf-8') as fl:
                fl.write(self.content)
        else:
            raise Exception("filepath not found")


# boostnote/notes folder check
if not os.path.isdir(NOTES_FOLDER):
    raise Exception("Can only executed under Boostnote folder")

# Generated Notes Folder check
if os.path.isdir(TARGET_FOLDER):
    BACKUP_FOLDER = TARGET_FOLDER + '.backup'
    if os.path.isdir(BACKUP_FOLDER):
        os.remove(BACKUP_FOLDER)
    os.rename(TARGET_FOLDER, BACKUP_FOLDER)

with open(BOOSTNOTE_JSON, mode='r', encoding='utf-8') as fl:
    boostnote_config = json.loads(fl.read())

subfolders = {}
for fldr_conf in boostnote_config['folders']:
    subfolders[fldr_conf['key']] = fldr_conf['name']

note_filenames = os.listdir(NOTES_FOLDER)
for note_filename in note_filenames:
    snote = Note(os.path.join(NOTES_FOLDER, note_filename))
    if snote.is_trashed:
        continue
    tnote = Note()
    tnote.title = snote.title.replace(" ", "_").replace(".", "_").replace("/", "_")
    tnote.ext = ".md" if snote.type == MARKDOWN_TYPE else ".txt"
    tnote.folder = subfolders.get(snote.folder)
    tnote.tpath = os.path.join(TARGET_FOLDER, tnote.folder, tnote.title + tnote.ext)
    tnote.content = snote.content
    tnote.overwrite()
