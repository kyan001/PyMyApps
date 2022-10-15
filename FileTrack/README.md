> Generate file list and compared to old ones.

* Trackings: File hashes to track changes.

* TrackFile: The output file to hold file trackings.

* File Exts: Files that you wanna track with specific extensions. As a list, must have at least 1 value (`["mp3",]`）

* TrackFile Format: Can choose from `TOML` or `JSON`

* Old TrackFile: Autodetect and parse old TrackFile to compared with.

* Usage:
  
  * Folder: Always using current folder as root folder.
  * New file: Generate a new file list.
  * Double-click on the script: Detect old list file by prefix and suffix.
  * Drag a list file: Using drag & drop file list as the old list file.
