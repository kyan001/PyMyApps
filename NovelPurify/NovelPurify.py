import sys, os, re, string
import tkinter.filedialog
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
        ktk.pStart()
        if not table:
            raise Exception('table 不能为空')
        for hanzi, pinyin in table.items():
            pinyin_list = generateToneList(pinyin)
            pattern = re.compile('[^a-zA-Z]( *(?:'+'|'.join(pinyin_list)+') *)[^a-zA-Z]', flags=re.IGNORECASE)
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
    }
    word_table = {
        '十有八九': '十有**',
        '兵痞子': '兵**',
        '侍女': 'shìnv',
        '世界': 'shìjiè',
        '自己': 'zìjǐ',
        '什么': 'shíme',
        '没有': 'méiyoǔ',
        '清楚': 'qīngchǔ',
        '那么': 'nàme',
        '周围': 'zhōuwéi',
        '已经': 'yǐjīng',
        '时候': 'shíhòu',
        '时间': 'shíjiān',
    }
    matched_patterns = []
    matched_patterns = matchInTable(word_table, matched_patterns)
    matched_patterns = matchInTable(hanzi_table, matched_patterns)
    if matched_patterns:
        ktk.pStart().echo('确认将「拼音」替换为以上「汉字」吗？', prefix='问题')
        answer = ktk.getChoice(['是', '否'])
        if '是' == answer:
            for hanzi, pattern in matched_patterns:
                ktk.info('Replacing {}'.format(hanzi))
                txt = pattern.sub(hanzi, txt)
            ktk.info('完成').pEnd()
    return txt

def unmatchedWordPurify(txt):
    ktk.pStart().pTitle('未匹配的英文字符串')
    tone_chars = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ'
    word_pattern = re.compile('[^a-zA-Z]( *[a-zA-Z.{}]+ *)[^a-zA-Z]'.format(tone_chars), flags=re.IGNORECASE)
    txt = findCheckDelete(word_pattern, txt, undelete=True)
    ktk.pEnd()
    return txt

def unmatchedUrlPurify(txt):
    ktk.pStart().pTitle('未匹配的 url')
    url_pattern = re.compile('([a-zA-Z.:/ ]*(?:www|http|com|org|net)[a-zA-Z0-9 \t{pncttn}]*)'.format(pncttn=string.punctuation), flags=re.IGNORECASE)
    txt = findCheckDelete(url_pattern, txt)
    ktk.pEnd()
    return txt

def unmatchedUrlBlockPurify(txt):
    ktk.pStart().pTitle('未匹配的 url 段落')
    url_block_pattern_www = re.compile('[\n]([^\r\n]*(?:www|http|com|org|net)[^\r\n]*)[\n]', flags=re.IGNORECASE)
    txt = findCheckDelete(url_block_pattern_www, txt)
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
    filepath = "jiangye.txt"
    if not filepath:
        filepath = tkinter.filedialog.askopenfilename()
    with open(filepath, mode='r', encoding="utf-8") as f:
        txt = f.read()
    txt = hanziPurify(txt)
    txt = unmatchedUrlPurify(txt)
    txt = unmatchedUrlBlockPurify(txt)
    txt = unmatchedWordPurify(txt)
    save(filepath, txt)
main()
