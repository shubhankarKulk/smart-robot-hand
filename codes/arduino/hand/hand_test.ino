#include<Servo.h>
#define s1 6
#define s2 8
#define s3 7
#define s4 5

//5 / last
//6 / first
//7// third
//8 / second

Servo myservo;
Servo myservo1;
Servo myservo2;
Servo myservo3;

void setup() {
  myservo.attach(s1);
  myservo1.attach(s2);
  myservo2.attach(s3);
  myservo3.attach(s4);

  myservo.write(0);
  myservo1.write(0);
  myservo2.write(0);
  myservo3.write(0);
}

void loop() {
  delay(1000);
  myservo.write(180);
  delay(1000);
  myservo1.write(180);
  delay(1000);
  myservo2.write(180);
  delay(1000);
  myservo3.write(180);
  delay(1000);

//  delay(1000);
//  myservo.write(0);
//  delay(1000);
//  myservo1.write(0);
//  delay(1000);
//  myservo2.write(0);
//  delay(1000);
//  myservo3.write(0);
//  delay(1000);
}
