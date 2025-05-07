#include <Keypad.h>


// Keypad
const byte ROWS = 4; //four rows
const byte COLS = 4; //three columns
char keys[ROWS][COLS] = {
  {'1', '2', '3', '+'},
  {'4', '5', '6', '-'},
  {'7', '8', '9', '*'},
  {'^', '0', 'R', '/'}
};
byte rowPins[ROWS] = {39, 41, 43, 45}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {37, 35, 33, 31}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

// Display
#define char_1 2

// Variables

// Display
long input_number;
int numberHexArray[16] = { 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x79, 0x50, 0xD0, 0xDC, 0x9C, 0x00 };
//                       { '0' , '1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , 'E' , 'r' , 'r.', 'o.', 'u.', ' '  };
int input_array[4];
int overflow_error[4] = { 13, 10, 11, 12 };
int underflow_error[4] = { 14, 10, 11, 12 };
int error[4] = { 10, 11, 12, 15 };
bool is_error = false;

// Calculations
char intake[9];
byte index = 0;
float num1;
float num2;
float result;
char char1[4];
char op;
char char2[4];
byte i;
bool solved = false;


void reverse() {
  for (int i = 0, j = 3; i < 2; i++, j--) {
    int temp = input_array[i];
    input_array[i] = input_array[j];
    input_array[j] = temp;
  }
}


void setup() {
  Serial.begin(9600);
  DDRA = 0xFF;

  for (i = 0; i < 4; i++) {
    pinMode(i + char_1, OUTPUT);
  }
}

void loop() {


  if (!solved) {
    char key = keypad.getKey();

    if (index < 9) {
      if (key != NO_KEY) {
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
      switch (op) {
        case '*':
          result = num1 * num2;
          break;

        case '/':
          result = round(num1 / num2);
          break;

        case '+':
          result = num1 + num2;
          break;

        case '-':
          result = num1 - num2;
          break;

        case '^':
          result = round(pow(num1, num2));
          break;

        case 'R':
          result = round(pow(num2, (1/num1)));
          break;

        default:
          memcpy(input_array, error, sizeof(input_array));
          is_error = true;
          break;
      }
      input_number = round(result);
      solved = true;
      
      Serial.println(input_number);

      // Preparing the display
      if (!is_error) {
        for (i = 0; i < 4; i++) {
          input_array[i] = (int(input_number / pow(10, i))) % 10;
        }
          reverse();
      }


      // Create an error
      if (input_number > 9999) {
        memcpy(input_array, overflow_error, sizeof(input_array));
        is_error = true;
      }
      if (input_number < 0) {
        memcpy(input_array, underflow_error, sizeof(input_array));
        is_error = true;
      }


    }
  }


  // Display
  if (solved) {
    for (i = 0; i < 4; i++) {
      PORTA = numberHexArray[input_array[i]];
      digitalWrite(i + char_1, LOW);
      delay(5);
      digitalWrite(i + char_1, HIGH);
    }
  }
}
