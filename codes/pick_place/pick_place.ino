#include <Servo.h>
#define input_size 30
#define servos 5
#define pulpin 9
#define dirpin 10
#define enapin 11

long loops = 0;
char serial;
Servo myservo[servos];

int servo_pins[servos] = {2, 3, 4, 5, 6, 7, 8, 12};
int default_pos[servos] = {0, 0, 0, 0, 0, 0, 0};

char input[input_size + 1];
bool motor_en = false;

void setup() {
  pinMode(pulpin, OUTPUT);
  pinMode(dirpin, OUTPUT);
  pinMode(enapin, OUTPUT);

  digitalWrite(pulpin, LOW);
  digitalWrite(enapin, LOW);
  digitalWrite(dirpin, HIGH);

  for (int i = 0; i < servos; i++)
  {
    myservo[i].attach(servo_pins[i]);
    myservo[i].write(default_pos[i]);
  }
  delay(15);
  Serial.begin(19200);
  Serial.println("init");

  digitalWrite(enapin, HIGH);
  delay(100);
  digitalWrite(enapin, LOW);
}

void grab()
{
  delay(1000);
  myservo[7].write(90);
  delay(1000);
  myservo[3].write(180);
  delay(500);
  myservo[4].write(180);
  delay(500);
  myservo[5].write(180);
  delay(500);
  myservo[6].write(180);
  delay(1000);
}

void leave()
{
  delay(1000);
  myservo[6].write(0);
  delay(500);
  myservo[4].write(0);
  delay(500);
  myservo[5].write(0);
  delay(500);
  myservo[3].write(0);
  delay(1000);
  myservo[7].write(90);
}

void place()
{
  if (Serial.available() > 0)
  {

    byte Size = Serial.readBytes(input, input_size);
    input[Size] = 0;
    char* command = strtok(input, ",");
    int i = 0;
    while (command != NULL)
    {
      Serial.println(command);
      if (i > 0) && (motor_en)
      {
        char buffer[30];
        sprintf(buffer, "Servo %d in position: %d", i, atoi(command));
        myservo[i].write(atoi(command));     // move servo
        Serial.println(buffer);
        delay(15);
        i += 1;
      }
      if (i == 0) && (motor_en)
      {
        angle = map(command, 0, 360, 0, 8001);
        while (loops < angle)
        {
          digitalWrite(dirpin, LOW);
          digitalWrite(pulpin, HIGH);
          digitalWrite(pulpin, LOW);
          loops++;
          delayMicroseconds(10);
        }
      }
      command = strtok(NULL, ",");
    }
  }
}

void loop() {
  if (Serial.available() > 0)
  {
    serial = Serial.read();
    Serial.println(serial, char);
    if (serial == 's')
    {
      place();
      delay(1000);
      grab();
      delay(1000);
      place();
      delay(1000);
      leave();
      delay(1000);
      place();
    }
  }
}
