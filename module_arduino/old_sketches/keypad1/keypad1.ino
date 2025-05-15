  #include <Keypad.h>


// Keypad
const byte ROWS = 4; //four rows
const byte COLS = 4; //three columns
char keys[ROWS][COLS] = {
  {'1','2','3','+'},
  {'4','5','6','-'},
  {'7','8','9','*'},
  {'A','0','B','/'}
};
byte rowPins[ROWS] = {39, 41, 43, 45}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {37, 35, 33, 31}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

// Display
#define char_1 2
#define char_2 3
#define char_3 4
#define char_4 5

// Variables

// Display
int input_number;
int ones = 0;
int tens = 0;
int hundreds = 0;
int thousands = 0;
int numberHexArray[10] = {0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F};

// Calculations
char intake[9];
byte index = 0;
int num1;
int num2;
char char1[4];
char op;
char char2[4];
byte i;
bool solved = false;

void setup(){
  Serial.begin(9600);
  DDRA=0xFF;
  pinMode(char_1, OUTPUT);
  pinMode(char_2, OUTPUT);
  pinMode(char_3, OUTPUT);
  pinMode(char_4, OUTPUT);
}

void loop(){
  
  
  if (!solved) {
    char key = keypad.getKey();

    if (index < 9) {
      if (key != NO_KEY){
        Serial.println(key);
        intake[index] = key;
        index++;
    
        Serial.println(index);
        Serial.println(intake);
        Serial.println();
      }
    }
  
  
    if (index >= 9) {


      // Casting to numbers and characters
      for (i = 0; i < 4; i++) {
          char1[i] = intake[i];
      }
    
      op = intake[4];
    
    
      for (i = 5; i < 9; i++) {
          char2[i - 5] = intake[i];
      }
    
    
      num1 = atoi(char1);
      num2 = atoi(char2);

      Serial.println(num1);
      Serial.println(num2);
      
    // Doing the calculation
      if (op == '*') {
        input_number = num1 * num2;
      }
      
      else if (op == '/') {
        input_number = num1 / num2;
      }
      
      else if (op == '+') {
        input_number = num1 + num2;
      }
      
      else if (op == '-') {
        input_number = num1 - num2;
      }

      solved = true;

      Serial.println(input_number);     
    }
  }

// Display
  if (solved) {

    int input_array[4];
    for (i = 0; i < 4; i++) {
      input_array[i] = (int(input_number/pow(10, i))) % 10;
    }
/*  
    ones = (input_number%10);
    tens = ((input_number/10)%10);
    hundreds = ((input_number/100)%10);
    thousands = (input_number/1000);

*/
    for (i = 0; i < 4; i++) {    
      PORTA = numberHexArray[input_array[i]];
      digitalWrite(char_1, LOW);
      delay(5);
      digitalWrite(char_1, HIGH);
    }
/*    
    PORTA = numberHexArray[hundreds];
    digitalWrite(char_2, LOW);
    delay(5);
    digitalWrite(char_2, HIGH);
    
    PORTA = numberHexArray[tens];
    digitalWrite(char_3, LOW);
    delay(5);
    digitalWrite(char_3, HIGH);
    
    PORTA = numberHexArray[ones];
    digitalWrite(char_4, LOW);
    delay(5);
    digitalWrite(char_4, HIGH);
    */
  }
}
