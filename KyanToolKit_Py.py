# -*- coding: utf-8 -*-
##################################################################
# By Kyan
##################################################################
import os, sys
import time, types
import getpass
import subprocess, shlex
import urllib.request, hashlib, json, io
import threading, queue
from functools import wraps

class KyanToolKit_Py(object):
    version = '4.3'
    def __init__(self, trace_file="trace.xml"):
        self.trace_file = trace_file
        self.q = {
            'stdout' : queue.Queue()
        }
        self.mutex = {
            'stdout' : threading.Lock()
        }

    def __del__(self):
        pass

#--Decorators-----------------------------------------------------
    def lockStdout(input_func): #decorator
        '使函数占住stdout，执行期间不让其他线程打印'
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

    def async(input_func): #decorator
        '使函数单开一个线程执行'
        @wraps(input_func)
        def callInputFunc(*args, **kwargs):
            t = threading.Thread(target=input_func, args=args, kwargs=kwargs)
            return t.start()
        return callInputFunc

    def printStartAndEnd(func_title="function"):#decorator
        '使函数执行前和执行完毕后打印start/end'
        def get_func(input_func):
            @wraps(input_func)
            def callInputFunc(*args, **kwargs):
                self = args[0]
                self.pStart()
                self.pTitle(func_title)
                result = input_func(*args, **kwargs)
                self.pEnd()
                return result
            return callInputFunc
        return get_func

    def inTrace(self, func): #decorator
        '将被修饰函数的进入和退出写入日志'
        @wraps(func)
        def call(*args, **kwargs):
            self.TRACE("Enter " + func.__qualname__ + "()")
            result = func(*args,**kwargs)
            self.TRACE("Leave " + func.__qualname__ + "()")
            return result
        return call

#--Text Process---------------------------------------------------
    def banner(self, content_="Well Come"):
        '生成占3行的字符串'
        # char def
        self.special_char = "#"
        self.space_char = " "
        self.GOLDENSECTION = 0.618
        # length calc
        itsays = content_.strip()
        effective_length = int(len(itsays))
        # gen contents
        content_line = self.special_char \
                        + str(self.space_char * int(effective_length/self.GOLDENSECTION*(1-self.GOLDENSECTION)/2)) \
                        + itsays \
                        + str(self.space_char * int(effective_length/self.GOLDENSECTION*(1-self.GOLDENSECTION)/2)) \
                        + self.special_char
        content_line_length = len(content_line)
        banner_border = self.special_char * content_line_length
        return banner_border + '\n' + content_line + '\n' + banner_border

    def echo(self, words, prefix="", lvl=0):
        words = str(words)
        if prefix:
            prefix = '({})'.format(prefix.capitalize()) + ' '
        tabs = '    ' * int(lvl) if int(lvl) else ''
        print("| {p}{t}{w}".format(p=prefix, t=tabs, w=words))
        return self

    def pStart(self):
        print('*')
        return self

    def pEnd(self):
        print('!')
        return self

    def pTitle(self, words):
        return self.echo(words + ":")

    def info(self, words, **options):
        return self.echo(words, "info", **options)

    def warn(self, words, **options):
        return self.echo(words, "warning", **options)

    def err(self, words, **options):
        return self.echo(words, "error", **options)

    def md5(self, words=""):
        if type(words) != bytes: # md5的输入必须为bytes类型
            words = str(words).encode()
        return hashlib.md5(words).hexdigest();

#--Image Process--------------------------------------------------
    def imageToColor(self, url, scale=200, mode='rgb'):
        '将url指向的图片提纯为一个颜色'
        from PIL import Image
        import colorsys
        if url:
            response = urllib.request.urlopen(url)
            img_buffer = io.BytesIO(response.read())
            img = Image.open(img_buffer)
            img = img.convert('RGBA')
            img.thumbnail((scale,scale))
            statistics = { 'r':0,'g':0,'b':0,'coef':0}
            for count, (r, g, b, a) in img.getcolors(img.size[0] * img.size[1]):
                hsv = colorsys.rgb_to_hsv(r/255,g/255,b/255)
                saturation = hsv[1]*255
                coefficient = (saturation * count * a) + 0.01 #避免出现 0
                statistics['r'] += coefficient * r
                statistics['g'] += coefficient * g
                statistics['b'] += coefficient * b
                statistics['coef'] += coefficient
                color = (
                    int(statistics['r']/statistics['coef']),
                    int(statistics['g']/statistics['coef']),
                    int(statistics['b']/statistics['coef'])
                )
            if mode.lower() == 'rgb':
                return color
            elif mode.lower() == 'hex':
                return "#%0.2X%0.2X%0.2X" % color
            else:
                return color
        else:
            return False;

#--System Fucntions-----------------------------------------------
    def clearScreen(self):
        if "win" in sys.platform:
            os.system('cls')
        elif "linux" in sys.platform:
            os.system('clear')
        else:
            self.err("No clearScreen for " + sys.platform)

    @lockStdout
    def pressToContinue(self, msg="\nPress Enter to Continue...\n"):
        #PY2# raw_input(msg)
        input(msg)

    def byeBye(self, msg="See you later"): #BWC
        self.bye(msg)

    def bye(self, msg=''):
        exit(msg)

    @printStartAndEnd('Run Command')
    def runCmd(self, cmd):
        'run command and show if success or failed'
        self.echo(cmd, "command");
        result = os.system(cmd);
        self.checkResult(result);

    def readCmd(self, cmd):
        args = shlex.split(cmd);
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        (proc_stdout, proc_stderr) = proc.communicate(input=None) # input = proc_stdin
        return proc_stdout.decode(); # stdout & stderr is in bytes format

#--Get Information------------------------------------------------
    @lockStdout
    def getInput(self, question='', prompt='> '):
        if '' != question:
            print(question)
        #PY2# return raw_input(prompt_).strip()
        return str(input(prompt)).strip()

    def getChoice(self, choices_):
        assemble_print = ""
        for index,item in enumerate(choices_):
            assemble_print +='\n' if index else ''
            assemble_print += "| " + " {}) ".format(str(index+1)) + str(item)
        user_choice = self.getInput(assemble_print);
        if user_choice in choices_:
            return user_choice;
        elif user_choice.isdigit():
            numerical_choice = int(user_choice);
            if numerical_choice > len(choices_):
                self.err("Invalid Choice").bye()
            return choices_[numerical_choice-1]
        else:
            self.err("Please enter a valid choice");
            return self.getChoice(choices_);

    def ajax(self, url, param={}, method='get'):
        param = urllib.parse.urlencode(param)
        if method.lower() == 'get':
            req = urllib.request.Request(url + '?' + param)
        elif method.lower() == 'post':
            param = param.encode('utf-8')
            req = urllib.request.Request(url, data=param)
        else:
            raise Exception( "Method '{method}' is invalid. (GET/POST)".format(method=method) )
        rsp = urllib.request.urlopen(req)
        if rsp:
            rsp_json = rsp.read().decode('utf-8')
            rsp_dict = json.loads(rsp_json)
            return rsp_dict
        return None

#--Pre-checks---------------------------------------------------
    @printStartAndEnd("Platform Check")
    def needPlatform(self, expect_platform):
        self.info("Need: " + expect_platform)
        self.info("Current: " + sys.platform)
        if not expect_platform in sys.platform:
            self.byeBye("Platform Check Failed");

    @printStartAndEnd("User Check")
    def needUser(self, expect_user):
        self.info("Need: " + expect_user);
        self.info("Current: " + self.getUser());
        if self.getUser() != expect_user:
            self.byeBye("User Check Failed");

#--Debug---------------------------------------------------------
    def TRACE(self, input_, trace_type='INFO'):
        trace_content = ''.join(input_)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        current_function = sys._getframe().f_back
        current_function_name = current_function.f_code.co_name
        current_line = current_function.f_code.co_firstlineno
        current_filename = current_function.f_code.co_filename
        trace_header = "\n<" + trace_type \
                + ' FILE="' + current_filename + '"' \
                + ' LINE="' + str(current_line) + '"' \
                + ' TIME="' + current_time + '"' \
                + ' FUNC="' + current_function_name + '()">\n'
        with open(self.trace_file,'a') as trace:
            trace.write(trace_header + trace_content + "\n</" + trace_type + ">\n")

    @async
    def update(self):
        ktk_url = "https://raw.githubusercontent.com/kyan001/KyanToolKit_Unix/master/KyanToolKit_Py.py"
        version_old = self.version
        try:
            ktk_req = urllib.request.urlopen(ktk_url)
            ktk_codes = ktk_req.read()
            ktk_codes_md5 = self.md5(ktk_codes);
            with open("KyanToolKit_Py.py", "rb") as ktk_file:
                ktk_file_md5 = self.md5(ktk_file.read());
            if ktk_codes_md5 != ktk_file_md5:
                with open("KyanToolKit_Py.py", "wb") as ktk_file:
                    ktk_file.write(ktk_codes);
                self.asyncPrint("\n\n[KyanToolKit_Py.py] Updated \n(From Version: {version})\n\n".format(version=version_old))
            else:
                self.asyncPrint("\n\n[KyanToolKit_Py.py] No Need Update \n(Version: {version})\n\n".format(version=version_old))
            return True
        except Exception as e:
            self.asyncPrint("\n\n[KyanToolKit_Py.py] Update Failed ({err})\n\n".format(err=str(e)))
            self.asyncPrint("\n")
            return False

#--Internal Uses-------------------------------------------------
    def checkResult(self, result):
        if 0 == result:
            self.echo("Done", "result")
        else:
            self.echo("Failed", "result")

    def getUser(self):
        return getpass.getuser();

    def asyncPrint(self, words):
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
