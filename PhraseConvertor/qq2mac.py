import sys
import os
import tkinter
import tkinter.filedialog
import xml.etree.ElementTree
import xml.dom.minidom

import consoleiotools as cit


@cit.as_session('生成短语字典')
def generate_dict_list(content):
    dlist = []
    for ln in content.split('\n'):
        if not ln:
            continue
        shortcut, afterequal = ln.split('=')
        index, phrase = afterequal.split(',')
        pdict = {
            'shortcut': shortcut.strip(),
            'phrase': phrase.strip(),
            'index': index.strip(),
        }
        cit.info('{}: {}'.format(shortcut, phrase))
        dlist.append(pdict)
    cit.info('共计 {} 个'.format(len(dlist)))
    return dlist


@cit.as_session('转化短语字典为 xml 格式')
def dict_to_xml(pdlist):
    def add_to_dict(dict_node, key, value):
        node = xml.etree.ElementTree.Element(key)
        node.text = value
        dict_node.append(node)

    plist_node = xml.etree.ElementTree.Element('plist')
    plist_node.set('version', '1.0')
    array_node = xml.etree.ElementTree.Element('array')
    for d in pdlist:
        dict_node = xml.etree.ElementTree.Element('dict')
        add_to_dict(dict_node, 'key', 'phrase')
        add_to_dict(dict_node, 'string', d.get('phrase'))
        add_to_dict(dict_node, 'key', 'shortcut')
        add_to_dict(dict_node, 'string', d.get('shortcut'))
        array_node.append(dict_node)
    plist_node.append(array_node)
    cit.info('共计 {} 个 node'.format(len(array_node)))
    uglyxml = xml.etree.ElementTree.tostring(plist_node, encoding='utf8', method='xml').decode()
    prettyxml = xml.dom.minidom.parseString(uglyxml).toprettyxml()
    return prettyxml


@cit.as_session('包裹 xml')
def wrap_xml(xcontent):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
    final_string = header + xcontent
    cit.info('共计 {} 个字符'.format(len(final_string)))
    return final_string


@cit.as_session('保存 .plist 文件')
def save(filepath, content):
    dir, fname = os.path.split(filepath)
    fbasename, fext = os.path.splitext(fname)
    fbasename = fbasename.replace('QQ拼音', 'MAC')
    dir += os.sep if dir else ''
    new_fname = '{dir}{fbasename}{ext}'.format(dir=dir, fbasename=fbasename, ext='.plist')
    with open(new_fname, mode='w', encoding='utf-8') as f:
        f.write(content)
        cit.info('新文件已储存在 {}'.format(new_fname))
    return True


def main():
    cit.start()
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    if not filepath:
        tkapp = tkinter.Tk()
        filepath = tkinter.filedialog.askopenfilename(filetypes=[('QQ拼音自定义短语配置文件', '.ini'), ('文本文件', '.txt'), ('所有', '.*')])
        tkapp.destroy()
    for mode in ("utf-8", 'gbk', 'cp1252', 'windows-1252', 'latin-1'):
        try:
            with open(filepath, mode='r', encoding=mode) as f:
                content = f.read()
                cit.info('以 {} 格式打开文件'.format(mode))
                break
        except UnicodeDecodeError:
            cit.warn('打开文件：尝试 {} 格式失败'.format(mode))
    cit.info('打开文件 {}'.format(filepath))
    phrase_dict_list = generate_dict_list(content)
    xml_content = dict_to_xml(phrase_dict_list)
    new_content = wrap_xml(xml_content)
    save(filepath, new_content)
    cit.pause()


if __name__ == '__main__':
    main()
