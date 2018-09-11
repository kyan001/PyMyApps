import sys
import os
import tkinter.filedialog
import consoleiotools as cit

# usage：
#   py mergeSrt.py info.eng.srt
# for .bat：
#   py mergeSrt.py %1


class SrtInfo:
    def __init__(self, filepath=None):
        if filepath:
            self.folder, basename = os.path.split(os.path.abspath(filepath))
            *self.name, self.lang, self.format = basename.split(".")
        else:
            self.folder = ""
            self.name = ()
            self.lang = ""
            self.format = ""

    @property
    def basename(self):
        return ".".join(self.name + [self.lang, self.format])

    @property
    def abspath(self):
        return os.path.join(self.folder, self.basename)

    @classmethod
    def copy(cls, source, target):
        target.folder = source.folder
        target.name = source.name
        target.lang = source.lang
        target.format = source.format

    def __str__(self):
        return str({
            "folder": self.folder,
            "name": self.name,
            "language": self.lang,
            "format": self.format
        })

    def is_valid(self):
        if not self.format == 'srt':
            self.error = f"'{self.format}' 不支持，请使用 '.srt' 文件"
            return False
        if not os.path.isfile(self.abspath):
            self.error = f"'{self.abspath}' file not found."
            return False
        return True

    def write(self, content):
        with open(self.abspath, mode='a', encoding='utf-8') as f:
            f.write(content)

    def read(self):
        for mode in ("utf-8", 'gbk', 'cp1252', 'windows-1252', 'latin-1'):
            try:
                with open(self.abspath, mode='r', encoding=mode) as f:
                    cit.info(f'以 {mode} 格式打开文件 {self.basename}')
                    return f.read()
            except UnicodeDecodeError:
                cit.warn('打开文件：尝试 {} 格式失败'.format(mode))


def main():
    cit.start()
    # get .eng.srt or .chn.srt file
    srt_lower_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not srt_lower_path:
        tkapp = tkinter.Tk()
        srt_lower_path = tkinter.filedialog.askopenfilename(filetypes=[('srt 文件', '.srt'), ('所有', '.*')])
        tkapp.destroy()
    cit.info(f'基准字幕：{srt_lower_path}')
    # get another srt file
    srtl = SrtInfo(srt_lower_path)
    cit.info(f'字幕目录：{srtl.folder}')
    srtu = SrtInfo()
    if srtl.is_valid():
        SrtInfo.copy(srtl, srtu)
        srtu.lang = 'chn' if srtl.lang == 'eng' else 'eng'
        cit.info(f'下方字幕：{srtl.basename}')
    else:
        cit.err(f"下方字幕错误: {srtl.error}")
        cit.bye()
    if srtu.is_valid():
        cit.info(f'上方字幕：{srtu.basename}')
    else:
        cit.err(f"上方字幕错误: {srtu.error}")
        cit.bye()
    # generate new srt file
    srtd = SrtInfo()
    SrtInfo.copy(srtu, srtd)
    srtd.lang = 'duo'
    cit.info(f'双语字幕：{srtd.basename}')
    if srtd.is_valid():
        cit.warn(f'{srtd.basename} 已存在，正在备份')
        os.rename(srtd.abspath, srtd.abspath + '.backup')
    # copy
    srtd.write(srtl.read())
    srtd.write("\n")
    srtd.write(srtu.read())
    cit.pause('[DONE]')


if __name__ == '__main__':
    main()
