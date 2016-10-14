import socket
import time

import consoleiotools as cit
import KyanToolKit
ktk = KyanToolKit.KyanToolKit("trace.tra")

# init variables
cit.ask('Select Server Ip')
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
servers = [
    '127.0.0.1',
    '173.230.148.199',
]
servers.append(hostip)
server_ip = cit.get_choice(servers)

trgt_ip = server_ip
trgt_port = 21516
cit.info('My Hostname: ' + hostname)
cit.info('My IP: ' + hostip)
cit.info('Server IP: ' + trgt_ip)
cit.info('Server Port: ' + str(trgt_port))

# create socket
cit.info('Creating Socket ...')
my_sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cit.info('Socket Created')

# connect to server
cit.info('Connecting Server ...')
srvr = (trgt_ip, trgt_port)
my_sckt.connect(srvr)
cit.info('Connection Established')
time.sleep(1)


def printChats(chats):
    ktk.clearScreen()
    cit.ask("Welcome to ChatRobo")
    for cht in chats:
        print(cht)
    print("")
# main
msg = 'Hi'
chats = [""]

while True:
    if msg == '':
        msg = 'Um...'
    # send msg
    bytes_sent = my_sckt.send(msg.encode(encoding="utf-8"))
    chats.append("Me: " + msg)
    if bytes_sent != len(msg):
        cit.err("Message Length is not correct.")
        cit.err('Bytes sent: ' + str(bytes_sent))
        cit.err('My Message: ' + str(len(msg)))
    # get reply
    srvr_rply = my_sckt.recv(1024).decode('utf-8')
    chats.append("Server: " + srvr_rply)
    chats.append("")
    # Clear and Print Chats
    printChats(chats)
    if msg == 'bye':
        break
    # ask for msg
    msg = cit.get_input("What do you want to say: ('bye' to quit)")
my_sckt.close()
