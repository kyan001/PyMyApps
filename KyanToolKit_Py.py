# -*- coding: utf-8 -*-
##################################################################
# By Kyan
##################################################################
import os
import sys
import time
import getpass
import subprocess
import shlex
import urllib.request
import hashlib
import json
import io
import threading
import queue
from functools import wraps


class KyanToolKit_Py(object):

    @property
    def version(self):
        return '4.5'

    def __init__(self, trace_file="trace.xml"):
        self.trace_file = trace_file
        self.q = {
            'stdout': queue.Queue()
        }
        self.mutex = {
            'stdout': threading.Lock()
        }

    def __del__(self):
        pass

# -Decorators-----------------------------------------------------
    def lockStdout(input_func: callable):  # decorator
        '使函数占住 stdout，执行期间不让其他线程打印'
        @wraps(input_func)
        def callInputFunc(*args, **kwargs):
            self = args[0]
            mutex = self.mutex.get('stdout')
            if mutex.acquire():
                try:
                    return input_func(*args, **kwargs)
                finally:
                    mutex.release()
        return callInputFunc

    def async(input_func: callable):  # decorator
        """使函数单开一个线程执行"""
        @wraps(input_func)
        def callInputFunc(*args, **kwargs):
            t = threading.Thread(target=input_func, args=args, kwargs=kwargs)
            return t.start()
        return callInputFunc

    def printStartAndEnd(func_title="function"):  # decorator
        """使函数执行前和执行完毕后打印 start/end"""
        def get_func(input_func: callable):
            @wraps(input_func)
            def callInputFunc(*args, **kwargs):
                cls = args[0]
                cls.pStart()
                cls.pTitle(func_title)
                result = input_func(*args, **kwargs)
                cls.pEnd()
                return result
            return callInputFunc
        return get_func

    def inTrace(self, func: callable):  # decorator
        """将被修饰函数的进入和退出写入日志"""
        @wraps(func)
        def call(*args, **kwargs):
            self.TRACE("Enter " + func.__qualname__ + "()")
            result = func(*args, **kwargs)
            self.TRACE("Leave " + func.__qualname__ + "()")
            return result
        return call

# -Text Process---------------------------------------------------
    @classmethod
    def banner(cls, content_="Well Come"):
        '生成占3行的字符串'
        # char def
        sp_char = "#"
        # length calc
        itsays = content_.strip()
        effective_length = int(len(itsays))
        # gen contents
        side_space = ' ' * int(effective_length * ((1 - 0.618) / 0.618) / 2)
        content_line = sp_char + side_space + itsays + side_space + sp_char
        content_line_length = len(content_line)
        banner_border = sp_char * content_line_length
        return banner_border + '\n' + content_line + '\n' + banner_border

    @classmethod
    def echo(cls, words, prefix="", lvl=0):
        words = str(words)
        if prefix:
            prefix = '({})'.format(prefix.capitalize()) + ' '
        tabs = '    ' * int(lvl) if int(lvl) else ''
        print("| {p}{t}{w}".format(p=prefix, t=tabs, w=words))
        return cls

    @classmethod
    def pStart(cls):
        print('*')
        return cls

    @classmethod
    def pEnd(cls):
        print('!')
        return cls

    @classmethod
    def pTitle(cls, words):
        return cls.echo(words + ":")

    @classmethod
    def info(cls, words, **options):
        return cls.echo(words, "info", **options)

    @classmethod
    def warn(cls, words, **options):
        return cls.echo(words, "warning", **options)

    @classmethod
    def err(cls, words, **options):
        return cls.echo(words, "error", **options)

    @classmethod
    def md5(cls, words=""):
        if type(words) != bytes:  # md5的输入必须为bytes类型
            words = str(words).encode()
        return hashlib.md5(words).hexdigest()

# -Image Process--------------------------------------------------
    @staticmethod
    def imageToColor(url: str, scale=200, mode='rgb'):
        '将 url 指向的图片提纯为一个颜色'
        from PIL import Image
        import colorsys
        if url:
            response = urllib.request.urlopen(url)
            img_buffer = io.BytesIO(response.read())
            img = Image.open(img_buffer)
            img = img.convert('RGBA')
            img.thumbnail((scale, scale))
            statistics = {'r': 0, 'g': 0, 'b': 0, 'coef': 0}
            for cnt, (r, g, b, a) in img.getcolors(img.size[0] * img.size[1]):
                hsv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                saturation = hsv[1] * 255
                coefficient = (saturation * cnt * a) + 0.01  # 避免出现 0
                statistics['r'] += coefficient * r
                statistics['g'] += coefficient * g
                statistics['b'] += coefficient * b
                statistics['coef'] += coefficient
                color = (
                    int(statistics['r'] / statistics['coef']),
                    int(statistics['g'] / statistics['coef']),
                    int(statistics['b'] / statistics['coef'])
                )
            if mode.lower() == 'rgb':
                return color
            elif mode.lower() == 'hex':
                return "#%0.2X%0.2X%0.2X" % color
            else:
                return color
        else:
            return False

# -System Fucntions-----------------------------------------------
    @classmethod
    def clearScreen(cls):
        """清屏"""
        if "win" in sys.platform:
            os.system('cls')
        elif "linux" in sys.platform:
            os.system('clear')
        else:
            cls.err("No clearScreen for " + sys.platform)

    @lockStdout
    def pressToContinue(cls, msg="\nPress Enter to Continue...\n"):
        """按任意键继续"""
        # PY2: raw_input(msg)
        input(msg)

    @classmethod
    def byeBye(cls, msg="See you later"):  # BWC
        """打印消息并退出程序"""
        cls.bye(msg)

    @classmethod
    def bye(cls, msg=''):
        """打印消息并退出程序"""
        exit(msg)

    @classmethod
    @printStartAndEnd('Run Command')
    def runCmd(cls, cmd: str) -> bool:
        """run command and show if success or failed"""
        cls.echo(cmd, "command")
        result = os.system(cmd)
        cls.checkResult(result)

    @classmethod
    def readCmd(cls, cmd: str) -> str:
        """run command and return the str format stdout"""
        args = shlex.split(cmd)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        (proc_stdout, proc_stderr) = proc.communicate(input=None)  # proc_stdin
        return proc_stdout.decode()  # stdout & stderr is in bytes format

# -Get Information------------------------------------------------
    @lockStdout
    def getInput(self, question='', prompt='> '):
        if '' != question:
            print(question)
        # PY2: return raw_input(prompt_).strip()
        return str(input(prompt)).strip()

    def getChoice(self, choices_: list) -> str:
        """用户可输入选项数字或选项内容，得到用户选择的内容"""
        assemble_print = ""
        for index, item in enumerate(choices_):
            assemble_print += '\n' if index else ''
            assemble_print += "| " + " {}) ".format(str(index + 1)) + str(item)
        user_choice = self.getInput(assemble_print)
        if user_choice in choices_:
            return user_choice
        elif user_choice.isdigit():
            numerical_choice = int(user_choice)
            if numerical_choice > len(choices_):
                self.err("Invalid Choice").bye()
            return choices_[numerical_choice - 1]
        else:
            self.err("Please enter a valid choice")
            return self.getChoice(choices_)

    @classmethod
    def ajax(cls, url: str, param={}, method='get') -> dict:
        param = urllib.parse.urlencode(param)
        if method.lower() == 'get':
            req = urllib.request.Request(url + '?' + param)
        elif method.lower() == 'post':
            param = param.encode('utf-8')
            req = urllib.request.Request(url, data=param)
        else:
            raise Exception("invalid method '{}' (GET/POST)".format(method))
        rsp = urllib.request.urlopen(req)
        if rsp:
            rsp_json = rsp.read().decode('utf-8')
            rsp_dict = json.loads(rsp_json)
            return rsp_dict
        return None

# -Pre-checks---------------------------------------------------
    @classmethod
    @printStartAndEnd("Platform Check")
    def needPlatform(cls, expect_platform: str):
        cls.info("Need: " + expect_platform)
        cls.info("Current: " + sys.platform)
        if expect_platform not in sys.platform:
            cls.byeBye("Platform Check Failed")

    @classmethod
    @printStartAndEnd("User Check")
    def needUser(cls, expect_user: str):
        cls.info("Need: " + expect_user)
        cls.info("Current: " + cls.getUser())
        if cls.getUser() != expect_user:
            cls.byeBye("User Check Failed")

# -Debug---------------------------------------------------------
    def TRACE(self, input_: str, trace_type='INFO'):
        trace_content = ''.join(input_)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        current_function = sys._getframe().f_back
        current_function_name = current_function.f_code.co_name
        current_line = current_function.f_code.co_firstlineno
        current_filename = current_function.f_code.co_filename
        trace_header = '\n<{type} FILE="{file}" LINE="{line}" TIME="{time}" FUNC="{func}()">\n'.format(
            type=trace_type, file=current_filename, line=str(current_line),
            time=current_time, func=current_function_name
        )
        with open(self.trace_file, 'a') as trace:
            trace.write(trace_header + trace_content + "\n</" + trace_type + ">\n")

    @async
    def update(self):
        ktk_url = "https://raw.githubusercontent.com/kyan001/KyanToolKit_Unix/master/KyanToolKit_Py.py"
        version_old = self.version
        try:
            ktk_req = urllib.request.urlopen(ktk_url)
            ktk_codes = ktk_req.read()
            ktk_codes_md5 = self.md5(ktk_codes)
            with open("KyanToolKit_Py.py", "rb") as ktk_file:
                ktk_file_md5 = self.md5(ktk_file.read())
            if ktk_codes_md5 != ktk_file_md5:
                with open("KyanToolKit_Py.py", "wb") as ktk_file:
                    ktk_file.write(ktk_codes)
                self.asyncPrint("\n\n[KyanToolKit_Py.py] Updated \n(From Version: {})\n\n".format(version_old))
            else:
                self.asyncPrint("\n\n[KyanToolKit_Py.py] No Need Update \n(Version: {})\n\n".format(version_old))
            return True
        except Exception as e:
            self.asyncPrint("\n\n[KyanToolKit_Py.py] Update Failed ({})\n\n".format(str(e)))
            self.asyncPrint("\n")
            return False

# -Internal Uses-------------------------------------------------
    @classmethod
    def checkResult(cls, result: bool):
        if 0 == result:
            cls.echo("Done", "result")
        else:
            cls.echo("Failed", "result")

    @classmethod
    def getUser(cls):
        return getpass.getuser()

    def asyncPrint(self, words: str):
        '不直接打印，等 stdout 线程锁打开时再输出'
        q = self.q.get('stdout')
        if words:
            q.put(words)
        self.printQueue()

    @async
    @lockStdout
    def printQueue(self):
        '找适当的时间，将 stdout 队列全部打印出来'
        q = self.q.get('stdout')
        while not q.empty():
            print(q.get())

if __name__ == '__main__':
    ktk = KyanToolKit_Py()
    ktk.update()
