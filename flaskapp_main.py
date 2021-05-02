# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import paho.mqtt.client as mqtt_client
import time



SmartRoom_State = 'PowerOFF'
SmartRoom_json= {'SmartRoom_State':SmartRoom_State}
app = Flask(__name__)

@app.route('/')
def hello_world():
    broker = '134.209.153.73'
    port = 1883
    topic = "test"
    # generate client ID with pub prefix randomly
    client_id = 'localhost'
    username = 'root'
    password = 'Smart32Room'


    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


    def publish(client,message):
        msg_count = 0

        time.sleep(1)
        result = client.publish(topic, message)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1



    mqtt_client = connect_mqtt()
    publish(mqtt_client,'Yo Bros This is Awesome')

    return 'Hello from Flask!'

@app.route('/ifttt', methods=['POST','GET'])
def handler():
    global SmartRoom_json
    SmartRoom_State = request.get_data()
    SmartRoom_json['SmartRoom_State']=SmartRoom_State
    print('Smart Room state is : {}'.format(SmartRoom_State))
    return ''

@app.route('/SmartRoom')
def SmartRoom():
    return SmartRoom_json