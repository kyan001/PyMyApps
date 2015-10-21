import socket
import random
import KyanToolKit_Py
ktk = KyanToolKit_Py.KyanToolKit_Py("trace.tra")
ktk.update()

# init server socket
ver='1.2'
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
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
rply_dict = {'version':[ver]}
rply_dict["?"] = [
    "Yes, the answer you will find out soon!",
    "Well...I don't know the answer.",
    "You are so right.",
    "I don't want to answer this.",
    ]
rply_dict['hi'] = [
    "Hello",
    "Hi",
    "What's up",
    "Nice to meet you",
    "Yo hommie",
    ]
rply_dict['bye'] = [
	'Bye bye',
	"It's time to say good bye, bro.",
	"Nice talking to you.",
	]
rply_dict["default"] = [
    "Haha, that's funny.",
    "Oh, really?",
    "tell me more, please.",
    "Wow, fantastic!",
    "Pardon? The signal is not perfect.",
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
    if "yes" == input("\nstop server? (yes/no): "):
        break
    else:
    	ktk.info('Server is running ...')
srvr_sckt.close()
