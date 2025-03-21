#!/usr/bin/env python3
########################################################################
# Filename    : ADC.py
# Description : Use ADC module to read the voltage value of potentiometer.
# Author      : www.freenove.com
# modification: 2020/03/06
########################################################################
import RPi.GPIO as GPIO
import time
from ADCDevice import ADS7830, ADCDevice

ledPin = 11
adc = ADCDevice()  # Define an ADCDevice class object


def setup():
    global adc
    # if(adc.detectI2C(0x48)): # Detect the pcf8591.
    #     adc = PCF8591()
    if adc.detectI2C(0x4B):  # Detect the ads7830
        adc = ADS7830()
    else:
        print(
            "No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n"
        )
        exit(-1)
    global p
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    p = GPIO.PWM(ledPin, 1000)
    p.start(0)


def loop():
    while True:
        value = adc.analogRead(0)  # read the ADC value of channel 0
        p.ChangeDutyCycle(value * 100 / 255)  # Mapping to PWM duty cycle
        voltage = value / 255.0 * 3.3  # calculate the voltage value
        print("ADC Value : %d, Voltage : %.2f" % (value, voltage))
        time.sleep(0.03)


def destroy():
    p.stop()  # stop PWM
    GPIO.cleanup()
    adc.close()


if __name__ == "__main__":  # Program entrance
    print("Program is starting ... ")
    try:
        setup()
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
