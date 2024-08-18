import BlynkLib
import time

BLYNK_AUTH = 'XMU3TqkPXkZuubyYdndoIP1qgHhY4u1i'

blynk = BlynkLib.Blynk(BLYNK_AUTH, server='blynk.cloud', port=80)

def v0_write_handler(value):
    print(f"V0 value: {value}")
    blynk.virtual_write(1, value[0])

blynk.on("V0", v0_write_handler)


def blynk_connected():
    print("Connected to Blynk Server")

blynk.on("connected", blynk_connected)


def my_timer_event():
    uptime = int(time.time()) - start_time
    blynk.virtual_write(2, uptime)

blynk.run()

start_time = time.time()

while True:
    my_timer_event()
    blynk.run()
    time.sleep(1)