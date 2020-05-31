import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
# MQTT broker hosted on local machine
mqttc = paho.Client()


# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600,timeout=5)

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
x=[]
y=[]
z=[]
sampletime=[]
while True:
    s.write("/query/run\r".encode())
    line=s.read(2)
    print("read:")
    print(line.decode())
    xbeenum.append(line)
    count=count+1
    time.sleep(1)
    if count==21 :
        break
s.write("/getACCval/run\r".encode())
numcount=s.read(3).decode()
print(numcount)

for i in range(0,int(numcount)):
    line=s.read(6)
    print(line.decode())
    x.append(float(line.decode()))
for i in range(0,int(numcount)):
    line=s.read(6)
    print(line.decode())
    y.append(float(line.decode()))
for i in range(0,int(numcount)):
    line=s.read(6)
    print(line.decode())
    z.append(float(line.decode()))
for i in range(0,int(numcount)):
    line=s.read(6)
    print(line.decode())
    sampletime.append(float(line.decode()))

for i  in range(0,19):
    num[i]=xbeenum[i+1]
    #print(num[i])

num[19]=2
ax=plt.subplot(111)
ax.plot(t,num)
ax.set_xlabel('time')
ax.set_ylabel('number')
ax.set_title('collected data plot')
plt.show()
"""
ax1=plt.subplot(111)
ax1.plot(sampletime,x)
ax1.plot(sampletime,y)
ax1.plot(sampletime,z)
plt.show()
"""
# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

mesg = "s"+numcount
mqttc.publish(topic, mesg)

for i in range(0,int(numcount)):
    mesg = "x"+str(x[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
for i in range(0,int(numcount)):
    mesg = "y"+str(y[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
for i in range(0,int(numcount)):
    mesg = "z"+str(z[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
for i in range(0,int(numcount)):
    mesg = "t"+str(sampletime[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
mesg = "g26.12"
mqttc.publish(topic, mesg)
s.close()