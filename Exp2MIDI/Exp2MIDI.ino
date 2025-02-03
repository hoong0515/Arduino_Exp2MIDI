#include <MIDIUSB.h>

const int expressionPin = A0;  // Expression 페달 신호 입력 핀
int minValue = 0;           // 최소값
int maxValue = 1023;              // 최대값
int currentValue = 0;
int cc_number = 11;
char command = "R";
bool invertPolarity = false;   // 극성 반전 여부

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();

    if (command == "C") {
      cc_number = 11;
      command = "R";
    }

    if (command == "D") {
      cc_number = 1;
      command = "R";
    }

    if (command == "E") {
      cc_number = 11;
      minValue = 0;
      maxValue = 1023;
      currentValue = 0;
      invertPolarity = false;
      command = "R";
    }

    if (command == 'S') {  // 캘리브레이션 시작
      minValue = 0;
      maxValue = 1023;
      // Serial.println("Calibration started. Send 'N' for next step.");
    }

    if (command == 'N') {  // 다음 단계로 이동
      minValue = analogRead(expressionPin);
      // Serial.println("Step completed. Send 'N' for next step or 'F' to finish.");
    }

    if (command == 'F') {  // 캘리브레이션 완료
      maxValue = analogRead(expressionPin);
      // Serial.println("Calibration finished.");
      // Serial.print("Min: ");
      // Serial.println(minValue);
      // Serial.print("Max: ");
      // Serial.println(maxValue);

      // 극성 반전 확인
      if (minValue > maxValue) {
        invertPolarity = true;
        // Serial.println("Polarity inverted.");
      } else {
        invertPolarity = false;
        // Serial.println("Polarity normal.");
      }
      command = "R";
    }
  }

  // MIDI 신호 전송 (정상 동작)
  int sensorValue = analogRead(expressionPin);
  if (invertPolarity) {
    if (sensorValue < maxValue) {
      sensorValue = maxValue;
    } else if (sensorValue > minValue) {
      sensorValue = minValue;
    }
  } else {
    if (sensorValue < minValue) {
      sensorValue = minValue;
    } else if (sensorValue > maxValue) {
      sensorValue = maxValue;
    }
  }
  int mappedValue = map(sensorValue, minValue, maxValue, 0, 127);
  if (mappedValue != currentValue) {
    // Serial.print(sensorValue);
    //Serial.print(" ");
    // Serial.println(mappedValue);
    midiEventPacket_t event = {0x0B, 0xB0, 11, mappedValue};
    MidiUSB.sendMIDI(event);
    MidiUSB.flush();
    currentValue = mappedValue;
  }

  delay(10);
}