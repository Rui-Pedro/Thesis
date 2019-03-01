import serial
import socket
import serial.tools.list_ports

host = '127.0.0.1'
port = 8080               # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
"""
data = s.recv(1024)
s.close()
print('Received', repr(data))
"""

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print p

ser = serial.Serial(
    port='/dev/pts/26',\
    baudrate=9600,\

    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1

while True:
    
    line=ser.readline()
    if line!='' or line!='\n':
        print(line)
        s.sendall(line)
    count = count+1

ser.close()




