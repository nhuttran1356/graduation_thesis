#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const byte RX = 12;  // GPIO D6
const byte TX = 14;  // GPIO D5
SoftwareSerial mySerial = SoftwareSerial(RX, TX);

String URL = "http://192.168.29.37/clean_machine/connection.php";
const char* ssid = "SanBanh_BacSaiGon2";
const char* password = "123456789";

float temperature_post = 0;
float water1_post = 0;
float water2_post = 0;

float waterLevel1;
float waterLevel2;
float temperature;

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  connectWiFi();
}

void loop() {
  if (mySerial.available() > 0) {
    String receivedData = mySerial.readStringUntil('\n');

    int firstCommaIndex = receivedData.indexOf(',');

    if (firstCommaIndex != -1) {
      String water1String = receivedData.substring(0, firstCommaIndex);
      String remainingData = receivedData.substring(firstCommaIndex + 1);

      int secondCommaIndex = remainingData.indexOf(',');
      if (secondCommaIndex != -1) {
        String water2String = remainingData.substring(0, secondCommaIndex);
        String temperatureString = remainingData.substring(secondCommaIndex + 1);

         waterLevel1 = water1String.toFloat();
         waterLevel2 = water2String.toFloat();
         temperature = temperatureString.toFloat();

      }
    }
  }

  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // Load_DHT11_Data();
  Load_Data();
  String postData = "temperature=" + String(temperature_post) + "&water1=" + String(water1_post) + "&water2=" + String(water2_post);

  HTTPClient http;
  WiFiClient client;
  http.begin(client, URL);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int httpCode = http.POST(postData);
  String payload = http.getString();

  Serial.print("URL : ");
  Serial.println(URL);
  Serial.print("Data: ");
  Serial.println(postData);
  Serial.print("httpCode: ");
  Serial.println(httpCode);
  Serial.print("payload : ");
  Serial.println(payload);
  Serial.println("--------------------------------------------------");
  delay(5000);
}

void Load_Data() {
  //-----------------------------------------------------------

  temperature_post = temperature;
  water1_post = waterLevel1;
  water2_post = waterLevel2;
  //-----------------------------------------------------------
  // Check if any reads failed.
  if (isnan(temperature_post) || isnan(water1_post) || isnan(water2_post)) {
    Serial.println("Failed to read from sensor!");
    temperature_post = 0;
    water1_post = 0;
    water2_post = 0;
  }
  //-----------------------------------------------------------

  Serial.printf("Temperature: %.2f\n", temperature);
  Serial.printf("Water1: %.2f\n", water1_post);
  Serial.printf("Water2: %.2f\n", water2_post);
}

void connectWiFi() {
  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("connected to : ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}