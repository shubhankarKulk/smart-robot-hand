#include <Servo.h>
#define input_size 30
#define servos 5
#define pulpin 9
#define dirpin 10
#define enapin 11

long loops = 0;

Servo myservo[servos];

int servo_pins[servos] = {2, 3, 4, 5, 6, 7, 8};
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

void loop() {


  if (Serial.available())
  {

    byte Size = Serial.readBytes(input, input_size);
    input[Size] = 0;
    char* command = strtok(input, ",");
    int i = 0;
    while (command != NULL)
    {
      Serial.println(command);
      if (motor_en)
      {
        char buffer[30];
        sprintf(buffer, "Servo %d in position: %d", i, atoi(command));
        myservo[i].write(atoi(command));     // move servo
        Serial.println(buffer);
        delay(15);
        i += 1;
      }
      if (i == 8) && (motor_en)
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
