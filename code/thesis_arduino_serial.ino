const int muxS0 = D8;
const int muxS1 = D9;
const int muxS2 = D10; // Pinned to GND
const int muxSig = D4; 

// Rows for the pressure matrix
const int rows[] = {D0, D1, D2, D3}; 
const int rowCount = 4;
const int colCount = 4; // 4x4 matriisi

void setup() {
  Serial.begin(115200);

  pinMode(muxS0, OUTPUT);
  pinMode(muxS1, OUTPUT);
  pinMode(muxS2, OUTPUT);
  
  digitalWrite(muxS2, LOW); 

  for (int i = 0; i < rowCount; i++) {
    pinMode(rows[i], OUTPUT);
    digitalWrite(rows[i], LOW); 
  }
}

void loop() {
  for (int i = 0; i < rowCount; i++) {
    digitalWrite(rows[i], HIGH);

    for (int j = 0; j < colCount; j++) {
      setMuxChannel(j);
      
      // ADVISOR NOTE: Increased delay to let voltage stabilize
      delayMicroseconds(100); 

      analogRead(muxSig); 
      
      // Actual read
      int val = analogRead(muxSig); 

      Serial.print(val);
      Serial.print("\t");
    }
    
    digitalWrite(rows[i], LOW);
    
    // move to a new line after every row is finished
    Serial.println(); 
  }
  
  // draw a line between each full 4x4 scan
  Serial.println("----"); 
  delay(500);
}

void setMuxChannel(int channel) {
  digitalWrite(muxS0, bitRead(channel, 0));
  digitalWrite(muxS1, bitRead(channel, 1));
}
