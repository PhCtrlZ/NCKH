int led1 = 2; // Chân cho LED 1
int led2 = 3; // Chân cho LED 2
int led3 = 4; // Chân cho LED 3

void setup() {
  Serial.begin(9600); // Khởi động Serial với tốc độ 9600
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Đọc lệnh từ Serial

    if (command == "LED1_ON") {
      digitalWrite(led1, HIGH);
    } else if (command == "LED1_OFF") {
      digitalWrite(led1, LOW);
    } else if (command == "LED2_ON") {
      digitalWrite(led2, HIGH);
    } else if (command == "LED2_OFF") {
      digitalWrite(led2, LOW);
    } else if (command == "LED3_ON") {
      digitalWrite(led3, HIGH);
    } else if (command == "LED3_OFF") {
      digitalWrite(led3, LOW);
    }
  }
}
