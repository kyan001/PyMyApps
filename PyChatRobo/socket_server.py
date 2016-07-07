import socket
import sys
import random

import KyanToolKit
ktk = KyanToolKit.KyanToolKit("trace.tra")

# init server socket
ver = '1.2'
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
if len(sys.argv) > 1:
    srvr_ip = sys.argv[1]
else:
    srvr_ip = hostip
srvr_port = 21516
ktk.info('Hostname: ' + hostname)
ktk.info('Server IP: ' + srvr_ip)
ktk.info('Server Port: ' + str(srvr_port))

# create socket
ktk.info('Starting Server ...')
srvr_sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
allowed_connection = 5
srvr_sckt.bind((srvr_ip, srvr_port))
srvr_sckt.listen(allowed_connection)
ktk.info('Allowed Connection: ' + str(allowed_connection))
ktk.info('Socket Created, Server is listening...')

# init reply dict
rply_dict = {'version': [ver]}

rply_dict['hi'] = [
    "Hello~",
    "Hi!",
    "What's up, bro?",
    "Nice to meet you.",
    "Yo homie.",
]
rply_dict['bye'] = [
    'Bye bye.',
    "It's time to say good bye.",
    "Nice talking to you.",
    'See you.',
    'See you later.',
]
rply_dict['how old'] = [
    "I'm 2 years old."
]
rply_dict['are you'] = [
    'Yes, I am.',
    "No, I'm not.",
]
rply_dict["?"] = [
    "The answer you will find out soon!",
    "Well...I don't know.",
    "Maybe you are right.",
    "Yes... I guess?",
    "I don't want to answer this.",
    "What question is that?",
]
rply_dict["default"] = [
    "Haha, that's funny.",
    "Oh, really?",
    "Tell me more, please.",
    "Wow, fantastic!",
    "Pardon? The signal is not perfect.",
    "I don't want to talk about this.",
]
# Get msg
while True:
    clnt_sckt, (clnt_ip, clnt_port) = srvr_sckt.accept()
    clnt_id = clnt_ip + ":" + str(clnt_port)
    ktk.warn("Client connected: " + clnt_id)
    while True:
        clnt_req = clnt_sckt.recv(1024).decode('utf-8')
        for kywrd in rply_dict:
            if kywrd.lower() in clnt_req.lower():
                rply = random.choice(rply_dict[kywrd.lower()])
                break
            else:
                rply = random.choice(rply_dict["default"])
        clnt_sckt.send(rply.encode(encoding="utf-8"))
        print("User: " + clnt_req)
        print("Me  : " + rply)
        print('')
        if "bye" == clnt_req:
            break
    clnt_sckt.close()
    ktk.warn("Client disconnected: " + clnt_id)
    print("")
    stopit = ktk.getInput("Stop the server? (yes/no)")
    if "yes" == stopit:
        break
    else:
        ktk.info('Server keeps running ...')
srvr_sckt.close()
