import socket
import time
import sys
import KyanToolKit_Py
ktk = KyanToolKit_Py.KyanToolKit_Py("trace.tra")
ktk.update()

# init variables
print(ktk.banner('Select Server Ip'))
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
servers = [
    '127.0.0.1',
    '173.230.148.199',
]
servers.append(hostip)
server_ip = ktk.getChoice(servers)

trgt_ip = server_ip
trgt_port = 21516
ktk.info('My Hostname: ' + hostname)
ktk.info('My IP: ' + hostip)
ktk.info('Server IP: ' + trgt_ip)
ktk.info('Server Port: ' + str(trgt_port))

# create socket
ktk.info('Creating Socket ...')
my_sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ktk.info('Socket Created')

# connect to server
ktk.info('Connecting Server ...')
srvr = (trgt_ip, trgt_port)
my_sckt.connect(srvr)
time.sleep(1)
ktk.info('Connection Established')

def printChats(chats):
    ktk.clearScreen()
    print(ktk.banner("Welcome to ChatRobo"))
    for cht in chats:
        print(cht)
    print("")
# main
msg = 'Hi'
chats = [""]

while True:
    if msg=='':
        msg='Um...'
    # send msg
    bytes_sent = my_sckt.send(msg.encode(encoding="utf-8"))
    chats.append("Me: " + msg)
    if bytes_sent != len(msg):
        ktk.err("Message Length is not correct.")
        ktk.err('Bytes sent: ' + str(bytes_sent))
        ktk.err('My Message: ' + str(len(msg)))
    # get reply
    srvr_rply = my_sckt.recv(1024).decode('utf-8')
    chats.append("Server: " + srvr_rply)
    chats.append("")
    # Clear and Print Chats
    printChats(chats)
    if msg == 'bye':
        break
    # ask for msg
    msg = ktk.getInput("What do you want to say: ('bye' to quit)")
my_sckt.close()
