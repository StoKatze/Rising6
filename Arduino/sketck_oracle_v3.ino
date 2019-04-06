#include <Keypad.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <WiFi101.h>
#include <MQTT.h>

const char ssid[] = "InnovationLab24";
const char pass[] = "welcome1";

WiFiClient net;
MQTTClient client;

LiquidCrystal_I2C lcd(0x27, 16, 2);

int a = 0; // variabile per il publish
String gName = ""; // variabile globale per il payload del publish

const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'D', 'C', 'B', 'A'},
  {'#', '9', '6', '3'},
  {'0', '8', '5', '2'},
  {'*', '7', '4', '1'}
};

int portarossa = A3;
int portaverde = A2;
int portablu = A1;

byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {6, 7, 8, 9};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void colore (unsigned char rosso, unsigned char verde, unsigned char blu) {
  analogWrite(portarossa, rosso);
  analogWrite(portablu, blu);
  analogWrite(portaverde, verde);
}

unsigned long lastMillis = 0;

void connect() {
  Serial.print("checking wifi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.print("\nconnecting...");
  while (!client.connect("arduino", "try", "try")) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("\nconnected!");
}

void stampa() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  - Welcome! - ");
  lcd.setCursor(0, 1);
  lcd.print(" Enter the code");
}

void setup() {
  Serial.begin(9600);
  
  WiFi.begin(ssid, pass);

  // Note: Local domain names (e.g. "Computer.local" on OSX) are not supported by Arduino.
  // You need to set the IP address directly.
  client.begin("192.168.1.198", net); //192.168.99.12
  client.onMessage(messageReceived);
  
  connect();
  
  pinMode(portarossa, OUTPUT);
  pinMode(portaverde, OUTPUT);
  pinMode(portablu, OUTPUT);

  colore(255, 0, 0);
  lcd.init(); // inizializza il display
  lcd.backlight(); //accende la retroilluminazione

  stampa();
  
  delay(3000);
}

String ctrlLen; // variabile per il controllo della lunghezza per la stampa del messaggio su display
String insertPin; // stringa che contiene il codice inseri

int f = 0; // variabile di controllo
int x = 0; // variabile di controllo lunghezza

void messageReceived(String &topic, String &payload) {
  Serial.println("incoming: " + topic + " - " + payload);
  client.unsubscribe("answer");
  gName = payload;
}

void loop() {
  client.loop();

  if (!client.connected()) {
    connect();
  }
  
  colore(255, 0, 0);

  char key = keypad.getKey();

  if (key != NO_KEY && x < 6) {

    if (f == 0) {
      lcd.clear();
      f = 1;
    }

    //Serial.print(key);

    lcd.setCursor(0, 0);
    lcd.print("Password:");
    lcd.setCursor(x, 1);
    lcd.print("*");

    insertPin += key;
    x++;
    a++;
  }

  if(a == 5) { // inviato il messaggio
    client.publish("code", insertPin);
    insertPin = "";
    client.subscribe("answer");
    a = 7;
    lcd.clear();
  }
  
  if(a == 7) { // ricevimento del messaggio e stampa sul display
    lcd.setCursor(0, 0);
    lcd.print("Recognition...");
    if(gName.length() > 0) {
      if(gName.equals("Err")) { // stampa errore sul display
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(" - Wrong code - ");
        Serial.println(" - Wrong code - ");
        for (int s = 0; s < 6; s++) {
          colore(0, 0, 0);
          delay(150);
          colore(255, 0, 0);
          delay(150);
        }
        delay(800);
        lcd.clear();
        stampa();
        x = 0;
        f = 0;
        a = 0;
        gName = "";
      } else {
        // Il pin viene aggiunto con la parola 'Welcome'
        ctrlLen = "Welcome " + gName;
        Serial.println(" - " + ctrlLen + " -");
      
        // Se tutta la stringa è maggiore di 16 caratteri allora verrà stampata in due righe diverse
        if (ctrlLen.length() > 16) {
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("Welcome");

          lcd.setCursor(0, 1);
          lcd.print(gName);
        } else {
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("Welcome " + gName);
        }
      
        colore(255, 235, 59);
        delay(1000);
        colore(0, 255, 0);
      
        delay(1000);
        lcd.clear();
      
        stampa();
        x = 0;
        f = 0;
        a = 0;
        gName = "";
      }
    }
  }
}