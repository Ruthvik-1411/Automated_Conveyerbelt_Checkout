/* 
 *  Scanner 
 *  Runs a motor attached to a conveyer belt and it moves forward. If a text is recieved from python script then it stops and 
 *  rings a buzzer and continues and moves forward again.
 *  written 6 jul 2022
 *  by Ruthvik Kotapati
 */

const int m1 = 10;              //pins of motor and buzzer and variable declaration to store serial data
const int m2 = 11;
const int buzz = 13;
char data = "";

void setup(){
  Serial.begin(9600);
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(buzz, OUTPUT);
  delay(200);
}

/*
 * The motor attached to the belt keeps moving forward until a serial data is recieved.
 * when data is recieved it is read and if it is the byte 'r' the ring the buzzer and stop.
 * Continue moving forward if data is not 'r' or no data is recieved
 */
void loop(){
  forward();
  while(Serial.available() > 0){
    data = Serial.read();
    //Serial.println(data);
    if(data == 'r'){
      proc();
      rest();
      delay(1000);
    }
    forward();
  }
}
void proc(){
  analogWrite(buzz, 175);
  delay(100);
  digitalWrite(buzz, LOW);
}
void forward(){
  analogWrite(m1, 200);
  analogWrite(m2, 0);
}
void rest(){
  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
}
