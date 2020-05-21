import serial
import time
import matplotlib.pyplot as plt
import numpy as np

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600,timeout=3)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x164\r\n".encode())
char = s.read(3)
print("Set MY 0x164.")
print(char.decode())

s.write("ATDL 0x264\r\n".encode())
char = s.read(3)
print("Set DL 0x264.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(4)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")

t=np.arange(0,20,1)
num=np.arange(0,20,1)
xbeenum=[]
count=0

while True:
    # send RPC to remote
    s.write("/query/run\r".encode())
    line=s.read(2)
   # print("read:")
    print(line.decode())
    xbeenum.append(line)
    count=count+1
    time.sleep(1)
    if count==21 :
        break

print("stop")
print(xbeenum)
print(xbeenum[1])
for i  in range(0,19):
    num[i]=xbeenum[i+1]
    print(num[i])
num[19]=2
plt.plot(t,num)
plt.show()

s.close()