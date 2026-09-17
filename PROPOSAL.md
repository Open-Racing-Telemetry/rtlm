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
