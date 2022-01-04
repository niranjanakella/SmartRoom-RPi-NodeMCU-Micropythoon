def do_connect(ssid,password):
    import network
    ssid = ssid
    password = password
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid,password)
        while not sta_if.isconnected():
            pass
    # print('network config:', sta_if.ifconfig())
