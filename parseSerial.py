import serial
import serial.serialutil

class parser:
    def __init__(self, comport="/dev/tty.usbmodem101", baudrate=9600, reverse = False):
        try:
            self.ser = serial.Serial(port=comport, baudrate=baudrate, timeout=0.1)
        except serial.serialutil.SerialException:
            print("Com port does not have necessary hardware connected")
            exit()
        self.reverse = reverse

    def read_serial(self):
        try:
            data = self.ser.readline().decode().strip()
        except serial.serialutil.SerialException:
            print("Radar hardware disconnected")
            exit()
        try:
            split_data = data.split(",")
            if len(split_data) != 2: raise IndexError()
            heading = int(split_data[0]) - 90
            if self.reverse:
                heading *= -1
            seen_object = int(split_data[1])
            if seen_object > 400: seen_object = None
            return heading, seen_object
        except IndexError:
            return 90, None # Serial connection not finalised

if __name__ == "__main__":
    app = parser()
    while True:
        heading, seen_object = app.read_serial()
        print(f"Heading: {heading}, Distance: {seen_object}")
