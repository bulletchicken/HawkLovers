// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#define BUTTON_PIN 4

Adafruit_MPU6050 mpu;

void setup(void) {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens


  // Try to initialize!
  if (!mpu.begin()) {
    while (1) {
      delay(10);
    }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:

    break;
  case MPU6050_RANGE_4_G:
    break;
  case MPU6050_RANGE_8_G:
    break;
  case MPU6050_RANGE_16_G:
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    break;
  case MPU6050_RANGE_500_DEG:
    break;
  case MPU6050_RANGE_1000_DEG:
    break;
  case MPU6050_RANGE_2000_DEG:
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    break;
  case MPU6050_BAND_184_HZ:
    break;
  case MPU6050_BAND_94_HZ:
    break;
  case MPU6050_BAND_44_HZ:
    break;
  case MPU6050_BAND_21_HZ:
    break;
  case MPU6050_BAND_10_HZ:
    break;
  case MPU6050_BAND_5_HZ:
    break;
  }
  delay(100);
}

void loop() {

  /* Get new sensor events with the readings */

  /*
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  

  int fallspeed = a.acceleration.x + a.acceleration.y + a.acceleration.z + 9; //adjustment factor
  Serial.print(fallspeed);
  Serial.println(" m/s^2");
  */
  Serial.println(digitalRead(BUTTON_PIN));

  delay(100);
}