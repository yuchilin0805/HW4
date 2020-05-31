import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np
# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your ip
host = "localhost"
topic = "Mbed"
t = [] 
X = []
Y = []
Z = []
samplecount=0
# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    global samplecount,X,Y,Z,t
    a=str(msg.payload,encoding = "utf-8")
    result= float(a[1:])
    if 'g' in a:
        print("g")
        mqttc.disconnect()
    elif 's' in a:
        samplecount=result
    elif 'x' in a:
        X.append(result)
    elif 'y' in a:
        Y.append(result)
    elif 'z' in a:
        Z.append(result)
    elif 't' in a:
        t.append(result)

    print(result)
    
    

    
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

# Loop forever, receiving messages
mqttc.loop_forever()

tilt=[]
for i in range(0,int(samplecount)):
    if Z[i]<= 0.5:
        tilt.append(1)
    else :
        tilt.append(0)
fig, ax = plt.subplots(2, 1)
ax[0].plot(t,X,color="blue", linewidth=1.0, linestyle="-",label="x")
ax[0].plot(t,Y,color="red", linewidth=1.0, linestyle="-",label="y")
ax[0].plot(t,Z,color="green", linewidth=1.0, linestyle="-",label="z")
ax[0].legend( loc='lower left', borderaxespad=0.)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Acc Vector')
ax[1].stem(t,tilt) # plotting the spectrum

ax[1].set_xlabel('Time')
ax[1].set_ylabel('Tiilt')
plt.show()