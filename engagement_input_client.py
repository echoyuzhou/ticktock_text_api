import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        clientsocket.connect(('localhost', 13011))
    except:
        print 'try'
    else:
        break

print 'connection established'
while True:
    clientsocket.recv(64)
    engagement = raw_input('What is the engagement state of the user of this turn?, score 1-5.  ')
    clientsocket.send(engagement)