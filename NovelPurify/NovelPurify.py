import sys, os, re, string
import tkinter, tkinter.filedialog
sys.path.append('../')
import KyanToolKit_Py
ktk = KyanToolKit_Py.KyanToolKit_Py()
#ktk.update()

def findCheckDelete(pattern, txt, undelete=False):
    '根据传入的 pattern 找到 txt 中的匹配，生成列表并由用户筛选，然后删除它们'
    matches = pattern.findall(txt)
    unmatched_words = list(set(matches))
    action = '保留' if undelete else '删除'
    confirm_txt = '「{}」以上所有项'.format(action)
    unmatched_words.append(confirm_txt)
    if len(matches):
        # print matches
        ktk.info('共找到 {} 个'.format(len(matches)))
        for kw in set(matches):
            ktk.info('"{}" : {}'.format(kw, matches.count(kw)), lvl=1)
        # generate final delete list
        while(True):
            ktk.pStart().echo('选择要「排除」的项：（当前 {} 个）'.format(len(unmatched_words)), prefix='问题')
            answer = ktk.getChoice(unmatched_words)
            if confirm_txt == answer:
                break
            else:
                unmatched_words.remove(answer)
    unmatched_words.remove(confirm_txt)
    if undelete:
        unmatched_words = list(set(matches) - set(unmatched_words))
    if unmatched_words:
        for word in unmatched_words:
            ktk.info('Deleting {}'.format(word))
            txt = txt.replace(word, "")
    ktk.info('完成').pEnd()
    return txt

def hanziPurify(txt):
    ktk.pStart()
    ktk.pTitle('净化拼音')
    def generateToneList(pinyin):
        pinyin = pinyin.replace('*', '\*')
        tone_table = {
            'a': ['ā', 'á', 'ǎ', 'à'],
            'e': ['ē', 'é', 'ě', 'è'],
            'i': ['ī', 'í', 'ǐ', 'ì'],
            'o': ['ō', 'ó', 'ǒ', 'ò'],
            'u': ['ū', 'ú', 'ǔ', 'ù'],
            'v': ['ǖ', 'ǘ', 'ǚ', 'ǜ'],
        }
        l = [pinyin]
        for tone_k, tone_v in tone_table.items():
            for tonelet in tone_v:
                if tonelet in pinyin:
                    l.append(pinyin.replace(tonelet, tone_k))
        return l

    def matchInTable(table, result_list=[]):
        '判断 txt 里面 match 多少个 table 中的拼音'
        ktk.pStart()
        if not table:
            raise Exception('table 不能为空')
        for hanzi, pinyin in table.items():
            pinyin_list = []
            if type(pinyin) == tuple: # '欲': (yu, yv)
                for py in pinyin:
                    pinyin_list += generateToneList(py)
            else: # '好': 'hao'
                pinyin_list += generateToneList(pinyin)
            pattern = re.compile(r'[^a-zA-Z]( *(?:{}) *)[^a-zA-Z]'.format('|'.join(pinyin_list)), flags=re.IGNORECASE)
            matches = pattern.findall(txt)
            if len(matches):
                result_list.append([hanzi, pattern])
                # print matches
                ktk.info('{}：{}，已匹配: {} 个'.format(hanzi, pinyin_list, len(matches)))
                for kw in set(matches):
                    ktk.info('"{}" : {}'.format(kw, matches.count(kw)), lvl=1)
        ktk.pEnd()
        return result_list

    hanzi_table = {
        '惑': 'huò',
        '露': 'lù',
        '摸': 'mō',
        '色': 'sè',
        '潮': 'cháo',
        '贱': 'jiàn',
        '插': 'chā',
        '小': 'xiǎo',
        '女': 'nǚ',
        '门': 'mén',
        '春': 'chūn',
        '射': 'shè',
        '胸': 'xiōng',
        '侍': 'shì',
        '蒙': 'méng',
        '荡': 'dàng',
        '毛': 'máo',
        '精': 'jīng',
        '花': 'huā',
        '洞': 'dòng',
        '性': 'xìng',
        '床': 'chuáng',
        '阴': 'yīn',
        '激': 'jī',
        '交': 'jiāo',
        '欲': ('yǜ', 'yù'),
        '药': 'yào',
        '浪': 'làng',
        '迷': 'mí',
        '肥': 'féi',
        '揉': 'róu',
        '妇': 'fù',
        '抽': 'chōu',
        '弄': 'nòng',
        '逼': 'bī',
        '私': 'sī',
        '波': 'bō',
        '魂': 'hun',
        '腿': 'tuǐ',
        '挺': 'tǐng',
        '穴': ('xvé', 'xué'),
    }

    word_table = {
        '十有八九': '十有**',
        '侍女': 'shìnv',
        '自己': 'zìjǐ',
        '什么': ('shénmè', 'shímè'),
        '没有': 'méiyoǔ',
        '清楚': 'qīngchǔ',
        '那么': 'nàme',
        '已经': 'yǐjīng',
        '时候': 'shíhòu',
        '时间': 'shíjiān',
        '裸露': 'luǒlù',
        '自由': 'zìyoú',
    }
    matched_patterns = []
    ktk.info('查找并替换词组')
    matched_patterns = matchInTable(word_table, matched_patterns)
    ktk.info('查找并替换单字')
    matched_patterns = matchInTable(hanzi_table, matched_patterns)
    if matched_patterns:
        ktk.pStart().echo('确认将「拼音」替换为以上「汉字」吗？', prefix='问题')
        answer = ktk.getChoice(['是', '否'])
        if '是' == answer:
            for i, (hanzi, pattern) in enumerate(matched_patterns):
                total = len(matched_patterns)
                ktk.echo('Replacing {}'.format(hanzi), prefix="{}/{total}".format(i+1, total=total))
                txt = pattern.sub(hanzi, txt)
            ktk.info('完成').pEnd()
    return txt

def unmatchedUrlPurify(txt):
    ktk.pStart().pTitle('未匹配的 url')
    chars_in_url = r"a-zA-Z0-9 \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\`\{\|\}\~\\"
    url_pattern = re.compile(r'[{0}]*(?:www|http|com|org|net|span|div)[{0}]*'.format(chars_in_url), flags=re.IGNORECASE)
    txt = findCheckDelete(url_pattern, txt)
    ktk.pEnd()
    return txt

def showParagraph(txt):
    ktk.pStart().pTitle('优化格式不正确的章节头')
    wrong_title_pattern = re.compile(r'([\S])(第[一二三四五六七八九十百 ]+[卷章回节])([\S])', flags=re.IGNORECASE)
    matches = wrong_title_pattern.findall(txt)
    wrong_titles = set(matches)
    if wrong_titles:
        ktk.info('共发现 {} 个格式错误的章节头'.format(len(wrong_titles)))
        right_title_pattern = r'\1 \2 \3'
        txt = wrong_title_pattern.sub(right_title_pattern, txt)
        ktk.info('优化完成').pEnd()
    ktk.pEnd()
    return txt

def showUnmatchedWord(txt):
    '显示尚未匹配到的英文字符串'
    threshold = 10;
    ktk.pStart().pTitle('未匹配的英文字符串：TOP {}'.format(threshold))
    tone_chars = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'
    word_pattern = re.compile(r'[^a-zA-Z]( *[a-zA-Z{0}][a-zA-Z.{0}]+ *)[^a-zA-Z]'.format(tone_chars), flags=re.IGNORECASE)
    matches = word_pattern.findall(txt)
    unmatched_words = list(set(matches))
    if unmatched_words:
        unm_word_dict = {}
        for uw in unmatched_words:
            unm_word_dict[uw] = matches.count(uw)
    uw_tops = sorted(unm_word_dict.items(), key=lambda Ditem:Ditem[1], reverse=True)[:threshold]
    for uw, count in uw_tops:
        ktk.info('"{}"：{}'.format(uw, count))
    ktk.pEnd()
    return txt

def save(filepath, txt):
    dir, fname = os.path.split(filepath)
    dir += os.sep if dir else ''
    new_fname = '{dir}pure.{fname}'.format(dir=dir, fname=fname)
    with open(new_fname, mode='w', encoding='utf-8') as f:
        f.write(txt)
        ktk.info('净化后的文件已储存在 {}'.format(new_fname))
    return True

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    if not filepath:
        tkapp = tkinter.Tk()
        filepath = tkinter.filedialog.askopenfilename()
        tkapp.destroy()
    try:
        with open(filepath, mode='r', encoding="utf-8") as f:
            txt = f.read()
            ktk.info('以 utf-8 格式打开文件')
    except UnicodeDecodeError:
        with open(filepath, mode='r', encoding='gbk') as f:
            txt = f.read()
            ktk.info('以 gbk 格式打开文件')
    txt = hanziPurify(txt)
    txt = unmatchedUrlPurify(txt)
    txt = showUnmatchedWord(txt)
    txt = showParagraph(txt)
    save(filepath, txt)

if __name__ == '__main__':
    main()
