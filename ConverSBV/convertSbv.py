import re
import sys
import KyanToolKit
ktk = KyanToolKit.KyanToolKit()

# usage：py convertSbv.py ori.sbv srt
# for .bat：py convertSbv.py %1

if len(sys.argv) > 1:
    filename = sys.argv[1]
    if '.sbv' not in filename:
        ktk.err("file's suffix must be sbv")
        ktk.bye()
else:
    ktk.err('Please provide .sbv filename')
    ktk.bye()

if len(sys.argv) > 2:
    target_format = sys.argv[2]
else:
    target_format = 'srt'

new_filename = filename.replace('.sbv', '.srt')


def writeFile(ln):
    ft.write(ln + '\n')
    ktk.info('[Write] {}'.format(ln))

if target_format == 'srt':
    with open(filename, encoding='utf-8') as fo:
        ktk.info('File Opened: {}'.format(filename))
        new_ln = ''
        index = 0
        pattern = re.compile(r'[0-9]+:[0-9][0-9]:[0-9][0-9]\.[0-9][0-9][0-9],[0-9]+:[0-9][0-9]:[0-9][0-9]\.[0-9][0-9][0-9]')
        with open(new_filename, 'w', encoding='gbk') as ft:
            ktk.info('File Opened: {}'.format(new_filename))
            for ln in fo:
                ln = ln.strip()
                if pattern.match(ln):
                    index += 1
                    writeFile(str(index))
                    new_ln = ln.replace(', ', ' --> ').replace('.', ', ')
                else:
                    new_ln = ln
                writeFile(new_ln)
            ktk.info('EOF')
        ktk.info('File Closed: {}'.format(new_filename))
    ktk.info('File Closed: {}'.format(filename))
else:
    ktk.err('format {} is not supported'.format(target_format))
    ktk.bye()
ktk.bye('[DONE]')
