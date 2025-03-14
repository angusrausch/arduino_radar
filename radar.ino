#include <Servo.h>

Servo myservo;
int direction = 1;
int heading = 90;

const int trigPin = 9;
const int echoPin = 10;

void setup() {
  myservo.attach(8);
  delay(500);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  Serial.begin(9600);
}

void moveServo() {
  if (heading >= 180 || heading <= 0) direction *= -1;
  heading += direction;
  myservo.write(heading);
}

int checkUltrasonic() {
  digitalWrite(trigPin, LOW);  
	delayMicroseconds(2);  
	digitalWrite(trigPin, HIGH);  
	delayMicroseconds(10);  
	digitalWrite(trigPin, LOW);
  // unsigned long startTime = micros(); Debuggin
  int duration = pulseIn(echoPin, HIGH, 2000); 
  // unsigned long endTime = micros(); Debugging
  // unsigned long timeDiff = endTime - startTime;  
  // Serial.println(timeDiff);
  if (duration == 0) return 999;
  return (duration*.0343)/2;
}

void loop() {
  moveServo();
  int distance = checkUltrasonic();

  String output = String(heading) + "," + String(distance);
  Serial.println(output);

  delay(20);
}