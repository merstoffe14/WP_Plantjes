#include <ESP8266WiFi.h>

const char* ssid = ".";
const char* password = "Vochtplek123!";

int ledPin = 1;
WiFiServer server(80);


void setup() {
  Serial.begin(9600);
  delay(10);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Verbinden met het wifi netwerk
  Serial.println();
  Serial.println();
  Serial.println("Aan het verbinden met: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  //De server starten
  server.begin();
  Serial.println("Server started");

  // Print the IP adress
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}

void loop() {
  //Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  //Wait untiel the client sends some data
  Serial.println("new client");
  while (!client.available()) {
    delay(1);
  }

  //read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  //match the request

  int value = LOW;
  if (request.indexOf("/LED=ON") != -1) {
    digitalWrite(ledPin, HIGH);
    value = HIGH;
  }

  if (request.indexOf("/LED=OFF") != -1) {
    digitalWrite(ledPin, LOW);
    value = LOW;
  }

  // Return the response

  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println("");
  client.println("<!DOCTYPE HTML>");
  client.println("<HTML>");

  client.println("Led is now: ");

  if (value == HIGH) {
    client.print("On");

  }
  else {
    client.print("Off");
  }

  client.println("<br><br>");
  client.println("<a href=\"/LED=ON\"\"><button>On </button></a>");
  client.println("<a href=\"/LED=OFF\"\"><button>Off </button></a><br />");
  client.println("</html>");

  delay(1);
  client.println("Client disconnected");
  client.println("");
}
