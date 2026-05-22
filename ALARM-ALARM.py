from machine import Pin,reset,Timer
from time import sleep,ticks_ms
import socket
import network
#Pins setup
LED1=Pin(16,Pin.OUT)
Button=Pin(13,Pin.IN,Pin.PULL_UP)
Buzzer=Pin(17,Pin.OUT)
Buzzer.on()
ALARM=False
AlarmOff=False
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
LED1.off()
ip=wifi.ifconfig()[0]
print(ip)
#IRQ
def ButtPress(a):
    global AlarmOff,ALARM
    if ALARM:
        AlarmOff=True
Button.irq(trigger=Pin.IRQ_FALLING,handler=ButtPress)
#timer
def Buzz(t):
    Buzzer.value(not Buzzer.value())
BuzzTim=Timer()
#Server
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,2000))
print('STARTING SERVER')
LED1.on()
server.listen()
lastTest=ticks_ms()
conn,addr=server.accept()
print('Connection established')
LED1.off()
conn.settimeout(0.5)
#Mainloop
while True:
    if (ticks_ms()-lastTest)>500000:#checks duration between last connection check and now
        break
    if AlarmOff:
        print('OFF')
        conn.send('COMING'.encode('utf-8'))
        ALARM=False
        AlarmOff=False
        BuzzTim.deinit()
        Buzzer.on()
    else:
        try:#recieving messages   
            msg=conn.recv(1024)
            msg=msg.decode('utf-8') 
        except:
            msg='Err'
        if msg=='ALARM':
            ALARM=True
            BuzzTim.init(mode=Timer.PERIODIC, callback=Buzz,period=500)
        elif msg=='TEST':
            conn.send('OK'.encode('utf-8'))
            lastTest=ticks_ms()
            LED1.on()
            sleep(1)
            LED1.off()
    sleep(1)
reset()