import jieba
import wordcloud
import consoleiotools as cit

@cit.as_session('获取文字')
def get_txt(txt=''):
    cit.ask("请输入要生成的文字内容：")
    return txt or cit.get_input()

@cit.as_session('分词')
def word_cut(txt):
    seg_list = jieba.cut(txt, cut_all=False)
    seg_str = " ".join(seg_list)
    cit.info('分词完毕')
    return seg_str

@cit.as_session('生成词云')
def generate_wordcloud(seg_str):
    wc = wordcloud.WordCloud(width=400, height=400, relative_scaling=0.5, scale=1, font_path="SourceHanSansSC-Medium.otf", background_color=None, mode='RGBA').generate(seg_str)
    wc.to_file('wordcloud.png')
    cit.info('图片已保存至当前文件夹内 wordcloud.png')

if __name__ == '__main__':
    cit.info('默认生成 400x400，背景透明的 png 图片')
    txt = get_txt()
    seg_str = word_cut(txt)
    generate_wordcloud(seg_str)
    cit.pause()

