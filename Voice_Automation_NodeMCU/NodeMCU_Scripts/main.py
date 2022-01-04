# main.py

import machine, network
import WiFi_connect
import gc
import implementation
# import ubinascii
from umqtt.simple import MQTTClient

# gc.enable()

# WiFi_connect.do_connect('vivo-1906','yesh1234')
# ssid ='Niranjan IPhone 11'
# password = 'nopassword2'

# ssid ='wifi_extender_2GHz'
# password = 'niranjan1'

# WiFi_connect.do_connect(ssid,password)
# led = machine.Pin(5, machine.Pin.OUT)
# ma_speed = machine.Pin(14,machine.Pin.OUT)
# ma_speed.value(200)
# ma_t1 = machine.Pin(12,machine.Pin.OUT) 
# ma_t2 = machine.Pin(13,machine.Pin.OUT)



implementation.implement()
        

# topic = b'test'
# # client_id = ubinascii.hexlify(machine.unique_id())
# client_id = b'nodemcu'


# def sub_cb(topic, msg):
#         global message
#         message = msg.decode("utf-8")
        

# # print('Booting Automation')

# client = MQTTClient(client_id, '64.227.178.47',1883,user = '41SmartSecureRoom', password = '41SmartSecureRoom')
# client.set_callback(sub_cb)
# client.connect()
# client.subscribe(topic)


# # print('Client Connected to Mqtt Broker')
# if network.WLAN(network.STA_IF).isconnected:
        
#         try:
        
#                 while True:
#                         client.wait_msg()                
#                         # print(SmartRoom_State)

#                         if message == 'PowerON':
#                                 led.value(1)
#                                 ma_t1.value(1)
#                                 ma_t2.value(0)
#                                 gc.collect()
#                         else:
#                                 led.value(0)
#                                 ma_t1.value(0)
#                                 ma_t2.value(0)
#                                 gc.collect()
                


#                         # control=ifttt_request.Ifttt_Request()
#                         # if control['SmartRoom_State']=='PowerON':
#                         #         pin.value(1)
#                         #         ma_t1.value(1)
#                         #         ma_t2.value(0)

#                         # elif control['SmartRoom_State']=='PowerOFF':
#                         #         pin.value(0)
#                         #         ma_t1.value(0)
#                         #         ma_t2.value(0)

#                         # time.sleep(0.01) #Time in seconds
                        
#         except KeyboardInterrupt:
#                 pass
#         except OSError as oserror:
#                 print(oserror)

