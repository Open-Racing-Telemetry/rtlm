# RTLM Design Proposal

## Rationale

Hobby electric racing teams, including Electrathon® teams, need useful vehicle data during a race and a reliable record afterward. Asking the driver to read voltages, currents, and temperatures from a small display adds distraction and gives the pit crew only occasional updates.

RTLM ("Racing Telemetry") is a proposed open-source system for collecting vehicle measurements, recording them onboard, and transmitting selected live data to a pit-side computer. The aim is to make telemetry affordable, repairable, and adaptable to different vehicles. Teams should be able to install only the sensors they need without redesigning the main electronics.

This document describes the intended system and design requirements. The onboard PCB is under development; the features and performance targets below are not claims of completed validation.

## System Architecture

The system has two primary physical units and a host application:

| Element | Responsibilities |
|---|---|
| Onboard Box | Acquire and timestamp sensor readings, apply calibration, record data to microSD, and send selected telemetry over LoRa. |
| Receiver | Receive LoRa packets and forward them to a computer through USB-C. |
| Host application | Display live measurements and connection status, flag stale or invalid readings, and support review/export of recorded data. |

Local acquisition and logging must continue when the radio link is unavailable. The live stream will use a selected subset of measurements and update rates that fit the radio airtime budget; it need not reproduce every locally recorded sample.

The initial prototype will support one vehicle and one receiver. Multi-vehicle coordination, remote configuration, and additional sensor nodes can follow after the basic acquisition, logging, and radio path is proven. Telemetry is observational and must not be required for propulsion, braking, or other vehicle control.

## Measurement Scope and Modularity

The intended measurement targets are:

| Measurement | Intended approach |
|---|---|
| Wheel speeds | Pulse inputs with configurable pulses per revolution and wheel circumference. |
| Motor, controller, battery, and brake temperatures | Suitable probes and conditioning selected for each location and temperature range. |
| Battery voltage, current, power, and energy | Appropriately rated measurement circuits; compute power and accumulated energy from calibrated, timestamped voltage/current readings. |
| Steering angle and pedal/throttle position | Calibrated position sensors connected through suitable analog inputs or expansion nodes. |

These are system-level targets, not a requirement to populate every sensor. The current onboard layout provides four pulse, four temperature, and four general analog connector positions, together with CAN expansion and a dedicated pack-voltage measurement region.

Each channel needs a documented signal type, electrical range, supply allowance, units, calibration, and sampling rate. A disconnected or out-of-range sensor must be reported as invalid rather than displayed as a plausible zero.

## Data and Firmware Guidelines

- Separate acquisition, storage, and radio work with bounded buffers so an SD write or transmission cannot stall time-sensitive sampling. Record buffer overruns and dropped samples.
- Store timestamps, channel identity, units, calibration/configuration information, and firmware/log-format versions with each recording.
- Include packet sequence information, sample age, and status flags in the radio protocol so the receiver can distinguish new readings from missing or stale data.
- Define startup, card-missing, storage-full, radio-loss, and power-interruption behavior. Existing recordings should remain recoverable after an interrupted session.
- Make channel configuration explicit. Support unused channels without requiring dummy sensors or firmware source changes.

Sampling rates, live update rates, permissible latency, and recording duration remain design inputs. Select them per measurement and verify the resulting storage, CPU, and radio budgets before committing to performance claims.

## Electrical and Mechanical Guidelines

The Onboard Box uses a regulated 5 V input; this is separate from traction-pack sensing. Document the external supply requirements and prevent USB power from back-feeding the vehicle supply. Calculate steady-state and peak demand for the MCU, radio, SD card, and enabled sensors, including operation from USB alone.

Keep `+3.3V`, `5V_SYS`, `5V_PULSE`, and `5V_CAN` distinct. Size switches, traces, vias, connector contacts, and plane necks for the expected load and voltage drop. Sensor-bank faults should be detectable, and their effect on other channels sharing the bank must be documented.

External inputs need protection and conditioning appropriate to their harness and signal type. Keep I2C and SPI local to the electronics; use CAN for remote expansion where appropriate. Publish connector pinouts with cavity numbers and viewing orientation, and clearly distinguish power, pack-sense, pulse, temperature, analog, and CAN ports.

Preserve the isolation boundary around pack-side circuitry on every copper layer. Establish the maximum fully charged pack voltage and required insulation spacing before releasing that region. Logger ground and power planes must remain outside the isolated pack-side region.

Use secure mounting, strain relief, and accessible programming/test connections. Enclosure, connector access, antenna placement, and SD retention should be checked before placement is frozen. Probe selection and mounting are part of the measurement design: battery surface temperature, for example, does not establish every cell's internal temperature.

## PCB Stackup and Layout

The intended board is six layers, nominally 1.6 mm thick, using JLCPCB's JLC06161H-3313 stackup with 1 oz outer copper and 0.5 oz inner copper. Confirm the stack and finished thickness with the manufacturer before ordering.

| Layer | Purpose |
|---|---|
| F.Cu | Signals, primarily horizontal |
| In1.Cu | GND reference plane within the logger domain |
| In2.Cu | +3.3V plane within the logger domain |
| In3.Cu | Separate 5V_SYS, 5V_PULSE, and 5V_CAN zones |
| In4.Cu | GND reference plane within the logger domain |
| B.Cu | Signals, primarily vertical |

The intended dielectric thicknesses, top to bottom, are **0.0994 / 0.55 / 0.1088 / 0.55 / 0.0994 mm**. Do not alter these merely to make KiCad's displayed total equal exactly 1.600 mm.

Layout guidelines:

- Reserve In1–In4 for planes. Enforce this with KiCad disallow-track rules and independently disable these layers in Freerouting. Through-vias remain allowed.
- Keep the preferred F.Cu/B.Cu routing directions for ordinary signals. Prioritize short decoupling paths, crystal loops, RF geometry, differential pairs, and switching-current loops over those preferences.
- Preserve a continuous ground reference beneath sensitive signals. Avoid crossing reference-plane gaps and provide nearby ground stitching when signals change between outer layers.
- Place decoupling capacitors close to their supply pins with short ground returns. Give source rails, exposed pads, and capacitor returns deliberate plane connections; a nearby pour alone does not establish connectivity.
- Use 0.20 mm as the ordinary signal-width default and 0.60/0.30 mm diameter/drill for ordinary through-vias. The current 0.15 mm minimum is for constrained routing. Power geometry requires a current/drop calculation.
- Calculate USB differential and SD single-ended geometry for the confirmed stackup. Apply constraints on both sides of series resistors, and derive any length/skew limits from interface timing requirements. RF matching interconnects must follow the selected reference design.
- Route and review sensitive circuits before general autorouting. Refill planes after changes and inspect clearances, disconnected islands, thermal connections, and narrow supply paths.
