import time
import board
import neopixel
import paho.mqtt.client as mqtt
import os

pixel_pin = board.D18
num_pixels = 12
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

##Initialization Code to be used in the class below


pixels.fill((0,0,0))
pixels.show()

MQTT_SERVER = "192.168.0.100"
MQTT_PATH = "test_channel"

def Receiver():
    # The callback for when the client receives a CONNACK response from the serv$
    def __init__(self):

        f = open("/boot/id.txt",'r')
        self.id=int(f.readline())

        try:
            f = open("/boot/my_loc.txt",'r')
            my_str=f.readline()
            temp = re.findall(r'\d+', test_string) 
            my_str = list(map(int, temp)) 
            self.my_x = my_str[0]
            self.my_y = my_str[1]
            f.close()
        except:
            print("My Location is Currently Unknown, sending a REQ to ControlPy")
            self.x = None
            self.y = None


        # more callbacks, etc
        self.client = mqtt.Client(client_id = self.id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.connect(MQTT_SERVER, 1883, 60)
        
        if self.my_x == None or self.my_y == None:
            self.client.publish("CONTROL", "get_loc")
            #Sends a publish request to get my location soon.

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()

        self.commands_dict = {
        #'my_coords':
        'rainbow':rainbow_rand,
        'increment':pong_simulation,
        }

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_PATH)

    def on_publish(self, client, userdata, result):
        print("Published Data")

    def rainbow_rand(self):
        for iter_id in range(200):
            pixels.fill(((role_id + iter_id % 2)*255, (role_id + iter_id + 2 % 7)*42,
            (role_id + 5 + iter_id % 9)*28))
            pixels.show()
            time.sleep(0.5)

    def increment_simulation(self):
        num_tail_length = 5
        for iter_id in range(200):
            if id < iter_id + num_tail_length and id > iter_id - num_tail_length:
                pixels.fill((255,255,255))
                pixels.show()
                time.sleep(0.5)
            else:
                pixels.fill((0,0,140))
                pixels.show()
                time.sleep(0.5)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        print(msg.payload)
        if msg.payload == "R":
            pixels.fill((255,0,0))
            pixels.show()
        elif msg.payload == "G":
            pixels.fill((0,255,0))
            pixels.show()
        elif msg.payload == "B":
            pixels.fill((0,0,255))
            pixels.show()
        elif msg.payload == "W":
            pixels.fill((255,255,255))
            pixels.show()
        elif msg.payload == "C":
            pixels.fill((0,0,0))
            pixels.show()
        elif msg.payload == "cmd1":
            print(id*5)
            time.sleep(0.5*id)
            pixels.fill((255,255,255))
            pixels.show()
            time.sleep(0.5)
            pixels.fill((0,0,0))
            pixels.show()
        else:
            if msg.payload in commands_dict:
                func_to_call = commands_dict[msg.payload]
            elif str.find("my_coord:" , msg.payload):
                #Checks if the received message matches my role id
                #If it does, then add my coords
                temp = re.findall(r'\d+', test_string) 
                num_list = list(map(int, temp)) 
                if num_list[0] == id:
                    self.my_x = num_list[1]
                    self.my_y = num_list[2]
                    f = open("/boot/my_loc.txt",'w')
                    f.write("x: " + str(self.my_x) + " y: " + str(self.my_y))
                    f.close()
            elif str.find("shell:", msg.payload):
                #Reads a shell command and sends a PUB with shell output
                shell_command = msg.payload[6:]
                stream = os.popen(shell_command)
                self.client.publish("CONTROL",stream.read())
            elif str.find("set_color_to_id:", msg.payload):
                temp = re.findall(r'\d+', test_string) 
                num_list = list(map(int, temp))
                if num_list == id:
                    r = num_list[1]
                    g = num_list[2]
                    b = num_list[3]
                    pixels.fill((r,g,b))
                    pixels.show()