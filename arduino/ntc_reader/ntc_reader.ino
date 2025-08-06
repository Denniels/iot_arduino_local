// ntc_reader.ino

const int analogPin = A0;     // Pin donde está conectado el divisor resistivo
const unsigned long interval = 1000; // Intervalo de muestreo en milisegundos

unsigned long previousMillis = 0;

void setup() {
  Serial.begin(9600);         // Inicializa la comunicación Serial
  while (!Serial) {
    ; // Espera a que el puerto Serial esté listo (necesario en algunos modelos)
  }
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    int adcValue = analogRead(analogPin);  // Lectura del ADC (0–1023)
    Serial.println(adcValue);              // Envío por Serial
  }
}