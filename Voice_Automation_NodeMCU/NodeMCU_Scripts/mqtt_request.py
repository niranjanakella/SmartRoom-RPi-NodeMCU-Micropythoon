def MQTT_request():
    from umqttsimple import MQTTClient
    import urequests as requests

    url = 'http://134.1'
    res = requests.get(url = url)
    
    return res.json()
    