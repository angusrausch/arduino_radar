# Radar

Wanted a cool UI for Arduino radar

### Arduino setup
- Arduino Pinout
    - These can be altered but not recomended
    - Connect vcc on servo and ultrasonic sensor
    - Connect gnd on servo and ultrasonic sensor
    - Connect the signal pin on the servo to pin 8 on Arduino
    - Connect the trig pin on the ultrasonic sensor to pin 9 on Arduino
    - Connect the echo pin on the ultrasonic sensor to pin 10 on Arduino
    - Connect Arduino to computer using a USB B cable
- Setup IDE
    - Open `radar.ino` in Arduino IDE
    - Configure the Arduino board to match your board
    - Configure com port to match com port Arduino is connected to
- Upload to Arduino
    - Upload the file to the arduino
    - Once uploaded the arduino should immediately begin moveing the servo
    - Open Serial Monitor and set Baudrate to 9600 and check output is `[int],[int]` this is `heading,distance` and is read by the python application
- Close Arduino Ide

### Python Setup
<small>All commands using `python3` should be done as `py` on a Windows machine</small>
- Setup virtual enviroment
    - Create virtual enviroment
        ```bash
        python3 -m venv venv
        ```
    - Activate virtual enviroment
        - Unix
            ```bash
            source venv/bin/activate
            ```
        - Windows
            ```bash
            venv/scripts/activate
            ```
        - You should now see `(venv)` prepended to terminal line
    - Install required pip packages
        ```bash
        pip3 install -r requirements.txt
        ```
- Start application
    - Simulated data
        - Can run with simulated data using `-s [rate]` argument. Note that the rate value is inverse to frequency and linear
        - Example simulated run
            ```bash
            python3 main.py -s 100
            ```
    - Using an Arduino
        - Ensure Arduino is pluged in and power led is on
        - Find com port 
            - Mac
                
                Run 
                ```bash
                ls /dev/tty.usbmodem*
                ```
                or 
                ```bash
                /dev/tty.usbserial*
                ```
                Find the output which best matches the Arduino id and copy that string
            - Linux 

                Run 
                ```bash
                ls /dev/ttyUSB*
                ```
                or 
                ```bash
                ls /dev/ttyACM*
                ```
                Find the output which best matches the Arduino id and copy that string

            - Windows
                - Open device manager
                - Expand `Ports (COM & LPT)`
                - Copy the `COM*` string (i.e `COM3`)
        - Starting App
            - Ensure Arduino IDE Serial Monitor is closed
            - To start app run 
            ```bash
            python3 main.py -c [comport string] -r
            ```
            - Arguments
                - The `-r` string is generally required since most Arduino servo have heading values in the opposite direction to the UI
                - If you have altered the Baudrate of the Arduino serial output use the `-b [baudrate]` argument to use the correct baudrate. Default 9600
            - If you recieve an error about required hardware ensure the Arduino is connected and the correct comport is selected
            