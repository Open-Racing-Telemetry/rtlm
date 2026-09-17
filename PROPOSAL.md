# RTLM Design Proposal

## Overview
The telemetry system shall be split between two primary physical componenets:
- Transmitter (henceforth reffered to as "The Onboard Box")
- Reciever (henceforth reffered to as "The Reciever")

The transmitter will be mounted on the vehicle and is responsible for both data logging and transmission over LoRa to the reciever.
The reciever simply recieves the transmitted telemetry over LoRa and communicates it to a host computer over usb-c.