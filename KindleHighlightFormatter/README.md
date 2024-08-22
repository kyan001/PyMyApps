# Kindle Highlight Formatter

Export Kindle's highlights.

## HTML -> Markdown
* Export HTML:
    1. Support Kindle APP for iOS/iPadOS/macOS, Kindle APP for Android is not tested.
    2. Open the book that you want to export its highlights.
    3. In the top-right corner, click the bookmark icon to open "Annotations" sidebar.
    4. Click "share", then the "File" option and the "Email" option will do.
    5. "Citation Style" is "None", then click "Save as" or "Export".
* Convert HTML to Markdown:

```bash
pip install -r requirements.txt  # install all the dependencies
python kindle_highlight_formatter.py  # convert by following the prompts
```
