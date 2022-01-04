def implement():
    from umqtt.simple import MQTTClient
    import machine,network
    import WiFi_connect
    import gc

    ssid ='wifi_extender_2GHz'
    password = 'niranjan1'

    WiFi_connect.do_connect(ssid,password)

    led = machine.Pin(5, machine.Pin.OUT)
    ma_speed = machine.Pin(14,machine.Pin.OUT)
    ma_speed.value(200)
    ma_t1 = machine.Pin(12,machine.Pin.OUT) 
    ma_t2 = machine.Pin(13,machine.Pin.OUT)

    topic = b'test'
    client_id = b'nodemcu'

    def sub_cb(topic, msg):
        global message
        message = msg.decode("utf-8")
    
    client = MQTTClient(client_id, '64.227.178.47',1883,user = '41SmartSecureRoom', password = '41SmartSecureRoom')
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic)
 
    if network.WLAN(network.STA_IF).isconnected:
        try:
            while True:

                client.wait_msg() 
                if message == 'PowerON':
                    led.value(1)
                    ma_t1.value(1)
                    ma_t2.value(0)
                    gc.collect()
                    
                else: 
                    led.value(0)
                    ma_t1.value(0)
                    ma_t2.value(0)
                    gc.collect()

        
        except KeyboardInterrupt:pass
    else: print("Not Connected")
