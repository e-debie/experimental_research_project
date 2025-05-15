#include <Keypad.h>



// Keypad
const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
char keys[ROWS][COLS] = {
  {'1', '2'},
  {'4', '5'},
  {'7', '8'},
  {'^', '0'}
};
byte rowPins[ROWS] = {39, 41, 43, 45}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {37, 35}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

// Display
#define char_1 2

// Variables

// Display
long input_number;
int input_array[8];
String overflow_error = "ErrU.";
String underflow_error = "ErrO.";
String divzero_error = "ErrD0";
String error = "Error";
bool is_error = false;
char temp[10];

// Calculations
char intake[9];
byte index = 0;
float num1;
float num2;
float result;
char char1[8];
char op;
char char2[8];
long i;
bool solved = false;


void reverse() {
  for (int i = 0, j = 7; i < 4; i++, j--) {
    int temp = input_array[i];
    input_array[i] = input_array[j];
    input_array[j] = temp;
  }
}


void setup() {
  Serial.begin(9600);
  for (i = 0; i < 8; i++) {
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
          result = num1 / num2;
          break;

        case '+':
          result = num1 + num2;
          break;

        case '-':
          result = num1 - num2;
          break;

        case '^':
          result = pow(num1, num2);
          break;

        case 'R':
          result = pow(num2, (1 / num1));
          break;

        default:
          // memcpy(input_array, error, sizeof(input_array));
          // is_error = true;
          break;
      }


      input_number = abs(round(result));
      solved = true;

      Serial.println(input_number);

      // Preparing the display
      if (!is_error) {
        long Temp = input_number   ;
        for (byte i = 0; i < 8; i++) {
          input_array[7 - i] = Temp % 10 ;
          Temp /= 10 ;
          Serial.print(input_array[i - 7]);
        }

        if (result < 0) {
          input_array[0] = 19;
        }
      }


      //  Throwing Exceptions
      // if (input_number > 99999999) {
      //   memcpy(input_array, overflow_error, sizeof(input_array));
      //   is_error = true;
      // }
      // else if (input_number < -9999999) {
      //   memcpy(input_array, underflow_error, sizeof(input_array));
      //   is_error = true;
      // }

      // else if (num2 == 0) {
      //   if (op = '/') {
      //     memcpy(input_array, divzero_error, sizeof(input_array));
      //     is_error = true;
      //   }
      // }
    }
  }




  // Display
  if (solved) {
    for (i = 0; i < 8; i++) {
    }
  }
}
