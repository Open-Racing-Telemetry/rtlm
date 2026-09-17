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

### Supporting part list (incomplete)
## Part selection — supporting parts

*USD prices for quantity 1, excluding shipping/tax. These are schematic candidates; quantities and circuit values still need finalizing. † = listed out of stock.*

Analog input buffers: [TLV9004IPWR](https://www.digikey.com/en/products/detail/texas-instruments/TLV9004IPWR/9674912) $0.85000 each  up to 2

3.0 V ADC reference: [MCP1501T-30E/CHY](https://www.digikey.com/en/products/detail/microchip-technology/MCP1501T-30E-CHY/5844610) $0.76000  1

Wheel-pulse conditioning: [SN74LVC14APWR](https://www.digikey.com/en/products/detail/texas-instruments/SN74LVC14APWR/276492) $0.54000  1 †

Sensor-power switches: [TPS2553DBVR](https://www.digikey.com/en/products/detail/texas-instruments/TPS2553DBVR/2047900) $1.09000 each 3 proposed †

CAN protection: [PESD2CANFD24V-TR](https://www.digikey.com/en/products/detail/nexperia-usa-inc/PESD2CANFD24V-TR/11487035) $0.44000  1

USB/external-power selector: [TPS2116DRLR](https://www.digikey.com/en/products/detail/texas-instruments/TPS2116DRLR/15205127) $1.07000  1

Input electronic fuse: [TPS25940ARVCR](https://www.digikey.com/en/products/detail/texas-instruments/TPS25940ARVCR/6572447) $2.80000  1 candidate †

Reverse-polarity protection MOSFET: [DMP2035U-7](https://www.digikey.com/en/products/detail/diodes-incorporated/DMP2035U-7/2178761) $0.52000 1 candidate †

Input transient suppressor: [SMBJ5.0A](https://www.digikey.com/en/products/detail/littelfuse-inc/SMBJ5-0A/285951) $0.50000  1 candidate

Buck-regulator inductor, 2.2 µH: [XFL4020-222MEC](https://www.coilcraft.com/en-us/products/power/high-voltage-inductors/xfl/xfl4020/xfl4020-222/) $2.47000 1; Coilcraft direct price

*The input protection components need a coordinated circuit. In particular, a “5 V” TVS does not clamp at 5 V and cannot alone protect the power selector.*

ESP32 40 MHz crystal: [FA-128 40.0000MF10Z-K3](https://www.digikey.com/en/products/detail/epson/FA-128-40-0000MF10Z-K3/2514630) $1.11000 1

LoRa 32 MHz TCXO: [TG2520SMN 32.0000M-MCGNNM3](https://www.digikey.com/en/products/detail/epson/TG2520SMN-32-0000M-MCGNNM3/13151954) $3.61000 1 candidate †

PCB antenna connector: [U.FL-R-SMT-1(10)](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/U-FL-R-SMT-1-10/2504612) $1.67000 1

USB-C receptacle: [USB4105-GF-A](https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198510) $0.80000 1

USB data-line ESD protection: [TPD2EUSB30DRTR](https://www.digikey.com/en/products/detail/texas-instruments/TPD2EUSB30DRTR/2193486) $1.11000 1 †

microSD socket: [1040310811](https://www.digikey.com/en/products/detail/molex/1040310811/2370379) $2.21000 1

Four-pin sensor cable housing: [0430250400](https://www.digikey.com/en/products/detail/molex/0430250400/252497) $0.42000 each — one per populated sensor port

Six-pin CAN PCB connector: [0430450600](https://www.digikey.com/en/products/detail/molex/0430450600/252528) $2.04000 1

Six-pin CAN cable housing: [0430250600](https://www.digikey.com/en/products/detail/molex/0430250600/252498) $0.51000 1

Two-pin 5 V power PCB connector: [0430450200](https://www.digikey.com/en/products/detail/molex/0430450200/252526) $0.98000 1

Two-pin power cable housing: [0430250200](https://www.digikey.com/en/products/detail/molex/0430250200/252496) $0.36000 1

Female crimp contacts, 20–24 AWG: [0430300007](https://www.digikey.com/en/products/detail/molex/0430300007/252479) $0.20000 each one per populated cable position

Boot/reset buttons: [PTS810SJG250SMTR LFS](https://www.digikey.com/en/products/detail/c-k/PTS810SJG250SMTR-LFS/4176612) $0.65000 each  2

Green status LEDs: [APT1608SGC](https://www.digikey.com/en/products/detail/kingbright/APT1608SGC/1747519) $0.19000 each  2–3

100 nF decoupling capacitors: [CC0603KRX7R9BB104](https://www.digikey.com/en/products/detail/yageo/CC0603KRX7R9BB104/2103082) $0.14000 each  quantity TBD

1 µF capacitors: [CC0603KRX5R6BB105](https://www.digikey.com/en/products/detail/yageo/CC0603KRX5R6BB105/2833608) $0.19000 each  quantity TBD

22 µF low-voltage bulk capacitors: [GRM21BR61A226ME51L](https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR61A226ME51L/5027595) $0.19000 each  quantity TBD †

USB-C CC resistors, 5.1 kΩ: [RC0603FR-075K1L](https://www.digikey.com/en/products/detail/yageo/RC0603FR-075K1L/730215) $0.10000 each  2 †

General pull-up resistors, 10 kΩ: [RC0603FR-0710KL](https://www.digikey.com/en/products/detail/yageo/RC0603FR-0710KL/726880) $0.10000 each  quantity TBD

CAN termination resistor, 120 Ω: [RC0603FR-07120RL](https://www.digikey.com/en/products/detail/yageo/RC0603FR-07120RL/726920) $0.10000  1, jumper-selectable
