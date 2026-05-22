from machine import Pin,reset,Timer
from time import sleep
import socket
import network
#Pins setup
addr=('MICROCONTROLER 1 IP(local)',2000) 
LED1=Pin(2,Pin.OUT)
Gled=Pin(15,Pin.OUT)
Button=Pin(21,Pin.IN,Pin.PULL_UP)
#variables
Gon=False
Alarm=False
Alarm_init=False
ERR=False
#WIFI
wifi=network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('SSID','PASSWORD')
a=0
while a<20 and not wifi.isconnected():
    a+=1
    LED1.value(not LED1.value())
    sleep(1)
if a==20:
    reset()
print(wifi.ifconfig()[0])
LED1.off()
#SOCKET INIT
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.settimeout(15)
try:#connecting to microcontroler 2
    client.connect(addr)
except:
    LED1.on()#unsuccesfull
    sleep(2)
    LED1.off()
    reset()
client.settimeout(5)
Gled.on()#successfull
sleep(5)
Gled.off()
#FUNCTIONS
def Gblink(t):
    Gled.value(not Gled.value())
def BUTTPRESS(a):
    global Alarm_init
    Alarm_init=True
def TEST(t):#connection test
    global Gon,Alarm,ERR
    if not Alarm:
        client.send('TEST'.encode('utf-8'))
        try:
            msg=client.recv(1024)
            msg=msg.decode('utf-8')
        except:
            msg='Err'
        if msg=='OK':
            Gon=True
            ERR=False
        elif msg=='Err':
            ERR=True
            LED1.on()
#IRQ+TIMER INIT
Button.irq(trigger=Pin.IRQ_FALLING,handler=BUTTPRESS)
TestTim=Timer(0)
TestTim.init(mode=Timer.PERIODIC, period=300000, callback=TEST)
GledBlink=Timer(1)
#MAINLOOP
while True:
    if Gon:
        Gon=False
        Gled.on()
        sleep(0.5)
        Gled.off()
    if Alarm_init and not ERR:
        print('ALARM')
        Alarm_init=False
        Alarm=True
        client.send('ALARM'.encode('utf-8'))
        GledBlink.init(mode=Timer.PERIODIC, period=500, callback=Gblink)
    else:
        try:
            msg2=client.recv(1024)
            msg2=msg2.decode('utf-8')
        except:
            msg2='Err'
        if msg2=='COMING':
            Alarm=False
            GledBlink.deinit()
            Gled.off()