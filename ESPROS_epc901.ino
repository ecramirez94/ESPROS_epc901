/*
 * ESPROS EPC901 Line Imager Control Firmware
 * An Arduino MEGA 2560 is used due to the limited dynamic memory
 * (~2KB) of a normal Arduino UNO (ATMega328P)
 * Carlos Ramirez - 9/13/22
 */

#include <Wire.h>

#define EPC901_ADDR 0b0010101

#define DATA_RDY 19
#define CLR_PIX  7
#define SHUTTER 8
#define READ 9
#define VIDEO_P A0

// States
uint8_t state = 0;
uint8_t return_state = 0;
#define idle 0
#define SINGLE 1
#define CONTINUOUS 2
#define EPC_CONFIG 3

// EPC901 Configuration Commands
uint8_t config_command = 0;
#define CHIP_REV_NO 0
#define EPC_RESET 1

volatile bool data_ready = false;
uint32_t prevMillis = 0;

uint16_t data[1027];

void setup() 
{
  pinMode(DATA_RDY, INPUT);
  pinMode(CLR_PIX, OUTPUT);
  pinMode(SHUTTER, OUTPUT);
  pinMode(VIDEO_P, INPUT);
  pinMode(READ, OUTPUT);

  digitalWrite(CLR_PIX, LOW);
  digitalWrite(SHUTTER, LOW);
  digitalWrite(READ, LOW);

  attachInterrupt(digitalPinToInterrupt(DATA_RDY), data_ready_ISR, RISING);

  analogReference(EXTERNAL);

  Wire.begin();

  Serial.begin(250000);
  Serial.println(F("BEGIN"));
}

void loop() 
{
  switch (state)
  {
    case SINGLE:
      epc901_read();
      state = idle;
    break;
    
    case CONTINUOUS:
      epc901_read();
    break;

    case EPC_CONFIG:
      switch (config_command)
      {
        case CHIP_REV_NO: 
          Wire.beginTransmission(EPC901_ADDR);
          Wire.write(byte(0x00));
          Wire.endTransmission();
          Wire.requestFrom(EPC901_ADDR, 1);
          if (Wire.available())
          {
            uint8_t no = Wire.read();
            Serial.print("R ");
            Serial.println(no, BIN);
          }
          Serial.println("HERE");
        break;

        case EPC_RESET:

        break;

        default:
          Serial.println(F("INVALID COMMAND"));
        break;
      }
      state = return_state;
    break;
    
    case idle:
    default:
      // If there's nothing to do, just print "WAIT" as a heartbeat signal
      if ((millis() - prevMillis) >= 1500) // Interval between prints in milliseconds
      {
        Serial.println(F("WAIT"));
        prevMillis = millis();
      }
    break;
  }
}

void serialEvent(void)
{
  String command = Serial.readStringUntil('\n'); // Read until newline char. '\n' is truncated.

  switch (command.charAt(0))
  {
    case '$':
      switch (command.charAt(1))
      {
        case '0':
          Serial.println(F("STOP READ"));
          state = idle;
        break;
        
        case '1':
          state = SINGLE;
        break;

        case '2':
          state = CONTINUOUS;
        break;
    
        default:
        break;
      }
    break;
    default:
      if (state != idle)
        return_state = state;
        
      if (command == "CHIP_REV_NO")
        config_command = CHIP_REV_NO;
      else if (command == "EPC_RESET")
        config_command = EPC_RESET;

      state = EPC_CONFIG;
    break;
  }
}

void data_ready_ISR(void)
{
  data_ready = true;
}

void epc901_read(void)
{
    clear_pix();
    capture_image();
    
    while(!data_ready){};
    data_ready = false;
    
    digitalWrite(READ, HIGH);
    delayMicroseconds(2);
    digitalWrite(READ, LOW);
    delayMicroseconds(100);
    for (uint16_t i = 0; i <= 1026; i++)
    {
      digitalWrite(READ, HIGH);
      //delayMicroseconds(1);
      data[i] = analogRead(VIDEO_P);
      digitalWrite(READ, LOW);
      //delayMicroseconds(1);
    }

    Serial.print("D ");
    
    for (uint16_t i = 3; i <= 1026; i++)
        Serial.print(data[i] + String(","));
    
    Serial.println('\n');

    delayMicroseconds(25000);
}

void clear_pix(void)
{
  digitalWrite(CLR_PIX, HIGH);
  delayMicroseconds(1);
  digitalWrite(CLR_PIX, LOW);
}

void capture_image(void)
{
  digitalWrite(SHUTTER, HIGH);
  delayMicroseconds(100);
  digitalWrite(SHUTTER, LOW);
}
