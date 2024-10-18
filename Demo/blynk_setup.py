import BlynkLib

class BlynkSetup:
    def __init__(self, auth_token, server='blynk.cloud', port=80):
        self.blynk = BlynkLib.Blynk(auth_token, server=server, port=port)

    def register_handler(self, pin, handler):
        self.blynk.on(pin, handler)

    def run(self):
        self.blynk.run()

    def virtual_write(self, pin, value):
        self.blynk.virtual_write(pin, value)

    def set_property(self, pin, property_name, value):
        self.blynk.set_property(pin, property_name, value)