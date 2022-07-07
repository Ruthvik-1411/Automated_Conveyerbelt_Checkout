/* Scanner entry
 *  The setup contains a motor attached to a conveyer belt, a 4x4 numpad
 *  and two leds red, green which are mutually opposite and operated using a single pin.
 *  The motor moves until it received any data from python script and stops when specific data is received.
 *  When received, it reads input from numpad and sends it back to script. 
 *  
 *  written 1 jul 2022
 *  by Ruthvik Kotapati
 */

#include <Keypad.h>               //Library to use numpad
const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {         //Characters on 4x4 numpad
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'.','0','#','D'}
};

byte rowPins[ROWS] = {2, 3, 4, 5}; //R1,R2,R3,R4
byte colPins[COLS] = {6, 7, 8, 9}; //C1,C2,C3,C4

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

/*Pin declaration of motor of belt, led and 
 * variables to store serial data and price entered through numpad.
 */

const int m1 = 10;
const int m2 = 11;
const int leds = 12;
char data = "";
String price = "";

void setup(){
  Serial.begin(9600);
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(leds, OUTPUT);
  delay(200);
}
/* Motor keeps moving in forward direction 
 *  until serial message from python script is received, then
 *  read the data and if it is the byte 'r' then
 *  stop the motor by blinking the lights and 
 *  call the function price_entry() before starting again and
 *  if the message received is not 'r' then keep moving forward
 *  repeat this indefinetly
 */
void loop(){
  forward();
  while(Serial.available() > 0){
    data = Serial.read();
    if(data == 'r'){
      rest();
      analogWrite(m1, 255);
      delay(2000);
    }
    forward();
  }
}
/* Two leds controlled using single pin
 *  so if pin goes high red led is on and green is off and
 *  if pin is low green led is on and red is off
 */
void proc(){
  digitalWrite(leds, HIGH);
  delay(100);
  digitalWrite(leds, LOW);
  delay(100);
}
void forward(){
  analogWrite(m1, 220);
  analogWrite(m2, 0);
  digitalWrite(leds, LOW);
}
void rest(){
  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
  proc();
  proc();
  price_entry();
}

/* When the motor is stopped then start reading the pins
 *  from numpad and read each character entered and
 *  if any key is entered then blink the lights and
 *  add the key to string and if the key is '#' the break out of loop
 * and show the string added until now i.e 
 * if 3589# is entered one by one then after entering # loop breaks and prints 3589.
 * The .print is read and decoded by python only. 
 */
void price_entry(){
  while(true){
    char key = keypad.getKey();
    if(key){
      proc();
      if(key == '#'){
        break;
      }
      price+= key;
    }
  }
  Serial.print(price);
  price = "";
}
