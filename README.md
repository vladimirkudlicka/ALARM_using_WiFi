# ALARM_using_WiFi
This is a code for a simple alarm system that uses 2 microcontrolers and they comunicate over local WiFi network.
# Alarm trigger (microcontroler 1):
This microcontroler is the client. Turn it on after the microcontroler 2 (server) is ready for connection.
This microcontrolers is connected to a button and an LED.(button is connected to ground and to the pin of the microcontroler, LED is connected to ground and also to the pin of the microcontroler using a resistor)
The onboard LED is used to signalise connecting to WiFi.
Then after the mictrocontroler establishes a connection with the alarm the green LED is turned on for 5s.
The system checks if the connection is still alive and if it is it blinks the green LED for 0,5s each 5 mins. (The connection check runs each 5 mins)
If the connection is lost the onboard LED will remain turned on.
When the button is pressed the LED starts blinking and it sends a message to the alarm (second microcontroler) using socket server.
# Alarm (microcontroler 2):
This microcontroler is the server.
This microcontroler is connected to an active buzzer using a PNP trasistor, there is a resistor between the pin and the base with value 2.7k ohms 
(if you want to use an NPN just swich the commands Buzzer.on() and Buzzer.off())
And also to an LED trough a resistor (300 ohms is enough).
And additionally to a button connected to the microcontroler pin and the ground.
If the alarm is triggered this microcontroler will switch the buzzer on and off each 1s.
You can turn off the alarm using the button on the microcontroler 2. The green LED on microcontroler 1 also stops blinking.
While the LED is blinking the system is connecting to WiFi.
If it is turned on permanently it is waiting for the microcontroler 1 connection.
If it is turned off it is working and ready.
If the connection check is succeful the LED will blink once shortly. (connection still alive)
If there is no connection check in 500s microcontroler 2 will restart. (The connection is lost)
# communication protocol
Socket type: TCP
Alarm triggering: Microcontroler 1 sends the message 'ALARM' Action: Microcontroler 1- Green LED starts blinking Microcontroler2 - buzzer starts making sound
Turning the alarm off: Microcontroler 2 sends the message 'COMING' Action: Microcontroler 1- Green LED stops blinking Microcontroler2 - buzzer stops making sound
Connection check: Microcrocontroler 1 sends the message 'TEST' if microcontroler 2 responds with 'OK' within 5s the LED blink is performed on both microcontrolers if the microcontroler 2 does not get the mesage 'TEST' for longer than 500s it restarts. If microcontroler 1 does not get the message 'OK' The onboard LED is turned on.
