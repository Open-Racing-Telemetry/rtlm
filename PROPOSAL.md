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

## Power Budget and Operating Modes

The initial external-power design targets are **1.25 A on +3.3 V**, **50 mA per sensor across eight 5 V outputs (400 mA combined)**, and **250 mA total for CAN expansion**. These are provisional selection allowances; sensor startup current, SD-card write peaks and simultaneous radio activity must be verified. Including the onboard CAN transceiver and conversion losses, the planning case requires approximately **1.81 A from the shared 5 V supply** at 4.5 V and 85% buck efficiency. Qualify the external power path for **2 A normal operation**, with separate startup and protection margins.

The current sensor/expansion switches are each limited to approximately 200 mA, and the external-input eFuse to approximately 1.5 A. Their settings must be revised to support these targets while respecting the power mux's 2.5 A continuous rating. Size source traces, plane necks, thermal connections and via banks for voltage drop and heating; the buck's 3 A rating and the POWER class's 0.50 mm width do not establish system capacity.

**USB power is intended for programming and service only.** Sensor and CAN-expansion supplies must default off; radio transmission, SD writes and LED loads must remain disabled in USB-only service mode. USB still powers the shared 3.3 V circuitry, so verify whole-board startup, enumeration and flashing current rather than budgeting only the ESP. First programming must work without application firmware.

The battery circuit has a **60 A fuse upstream of the branch**. Provide branch protection coordinated with the branch wiring, maximum battery voltage and fault current; the main fuse does not establish protection for the smaller telemetry or sense wiring.
