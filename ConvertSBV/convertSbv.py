import re
import sys
import tkinter.filedialog
import KyanToolKit
ktk = KyanToolKit.KyanToolKit()

# usage：
#   py convertSbv.py ori.sbv [srt]
# for .bat：
#   py convertSbv.py %1


def writeContent(filepath, content):
    with open(filepath, mode='w', encoding='utf-8') as fl:
        ktk.info("新文件设置为 utf-8 格式")
        fl.write(content)
        ktk.info("新文件写入完毕")


def convert_to_srt(orig_file, new_file):
    ktk.pStart()
    pattern = re.compile(r'[0-9]+:[0-9][0-9]:[0-9][0-9]\.[0-9][0-9][0-9],[0-9]+:[0-9][0-9]:[0-9][0-9]\.[0-9][0-9][0-9]')
    index = 0
    new_content = ''
    for mode in ("utf-8", 'gbk', 'cp1252', 'windows-1252', 'latin-1'):
        try:
            with open(orig_file, mode='r', encoding=mode) as fl:
                ktk.info('以 {} 格式打开文件'.format(mode))
                for ln in fl:
                    ln = ln.strip()
                    if pattern.match(ln):
                        index += 1
                        new_content += (str(index) + '\n')
                        new_ln = ln.replace(',', ' --> ').replace('.', ',')
                    else:
                        new_ln = ln
                    new_content += (new_ln + '\n')
                writeContent(new_file, new_content)
                break
        except UnicodeDecodeError:
            ktk.warn('打开文件：尝试 {} 格式失败'.format(mode))


def main():
    ktk.pStart()
    # get original .sbv file
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    if not filepath:
        tkapp = tkinter.Tk()
        filepath = tkinter.filedialog.askopenfilename(filetypes=[('sbv 文件', '.sbv'), ('所有', '.*')])
        tkapp.destroy()
    ktk.info('源文件：{}'.format(filepath))
    # get target format
    target_format = sys.argv[2] if len(sys.argv) > 2 else 'srt'
    ktk.info('格式：sbv -> {}'.format(target_format))
    # generate target name
    new_filename = filepath.replace('.sbv', '.srt')
    ktk.info('新文件：{}'.format(new_filename))
    ktk.pEnd()
    # convert
    if target_format == 'srt':
        convert_to_srt(filepath, new_filename)
    ktk.pressToContinue('[DONE]')


if __name__ == '__main__':
    main()
