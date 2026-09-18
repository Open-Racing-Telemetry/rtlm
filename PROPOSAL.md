# RTLM Design Proposal

## Rationale
The nexus of our problem is data visibility in a high stakes racing environment. Hobby electric racing vehicles, including but not limited to Electrathon® vehicles, lack a reliable method of transmitting vital information about their status. Often, the driver is responsible for reading out voltages and current from a small onboard display, increasing their already high cognitive load and forcing them to divert their attention from the task at hand. To us, this is unnaceptable. RTLM (loosely meaning "Racing Telemetry") will provide an affordable, modular, and easy to install hobby racing telemetry system that provides realtime updates regarding performance of critical onboard systems. Our modular design will allow the end-user to select which sensors are neccessary for their vehicle, preventing unneccesary expenditures and maximizing compatibility.

## Overview
The telemetry system shall be split between two primary physical componenets:
- Transmitter (henceforth reffered to as "The Onboard Box")
- Reciever (henceforth reffered to as "The Reciever")

The transmitter will be mounted on the vehicle and is responsible for both data logging and transmission over LoRa to the reciever.
The reciever simply recieves the transmitted telemetry over LoRa and communicates it to a host computer over usb-c.

Our primary measurement targets we intend to specifically support are as following:
- Acceleration and angular velocity
- Wheel speed(s)
- Motor temperature(s)
- Controller temperature(s)
- Battery temperature(s)
- Brake temperature(s)
- Battery voltage/current/energy
- Steering angle
- Pedal/throttle position(s)

Please note that our intent to support these targets will in no way impose them upon the user.

## Part selection

*DigiKey USD prices, quantity 1; excludes shipping and tax.*

Processor: [ESP32-S3FN8](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-S3FN8/15822446) $4.17000

LoRa radio: [SX1262IMLTRT](https://www.digikey.com/en/products/detail/semtech-corporation/SX1262IMLTRT/8564369) $9.04000

IMU: [BMI088](https://www.digikey.com/en/products/detail/bosch-sensortec/BMI088/8634942) $5.92000 — out of stock

Analog sensor ADC: [MCP3208-CI/SL](https://www.digikey.com/en/products/detail/microchip-technology/MCP3208-CI-SL/305929) $2.78000

Battery monitor: [INA228AIDGSR](https://www.digikey.com/en/products/detail/texas-instruments/INA228AIDGSR/13691042) $4.68000; external shunt required

CAN transceiver: [TCAN1042HGVDRQ1](https://www.digikey.com/en/products/detail/texas-instruments/TCAN1042HGVDRQ1/5967664) $2.23000

3.3 V regulator: [TPS62130RGTR](https://www.digikey.com/en/products/detail/texas-instruments/TPS62130RGTR/4833914) $1.99000

Sensor connector, PCB side: [Micro-Fit 3.0 0430450400](https://www.digikey.com/en/products/detail/molex/0430450400/252527) $1.45000 each