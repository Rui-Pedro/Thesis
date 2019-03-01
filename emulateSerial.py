import serial
import time

port = serial.Serial("/dev/pts/25", baudrate=115200, timeout=3.0)

while True:
    filepath = 'tou.txt'  
    with open(filepath) as fp:  
        line = fp.readline()
        cnt = 1
        while line:
            print(line)
            time.sleep(2)
            line = fp.readline()
            port.write(line)
        
