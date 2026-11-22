# RTLM Design Proposal

## Rationale

Hobby electric racing teams, including Electrathon® teams, need useful vehicle data during a race and a reliable record afterward. Asking the driver to read voltages, currents, and temperatures from a small display adds distraction and gives the pit crew only occasional updates.

RTLM ("Racing Telemetry") is a proposed open-source system for collecting vehicle measurements, recording them onboard, and transmitting selected live data to a pit-side computer. The aim is to make telemetry affordable, repairable, and adaptable to different vehicles. Teams should be able to install only the sensors they need without redesigning the main electronics.

This document describes the intended system and design requirements. The onboard PCB is under development; the features and performance targets below are not claims of completed validation.

Please note that our intent to support these targets will in no way impose them upon the user.

## Power Budget and Operating Modes

The provisional design allocation is **1.30 A peak on +3.3 V**, **50 mA per powered sensor across eight 5V_PULSE outputs (400 mA combined)**, and **250 mA total for CAN expansion**. The 3.3 V allowance includes ESP/flash (500 mA), SD (400 mA), LoRa/TCXO (150 mA), LEDs/driver (185 mA), isolated measurement (43 mA), and other circuits (22 mA). These are selection allowances, not guaranteed maxima for unspecified cards, sensors or firmware. Wi-Fi/BLE remain disabled because the ESP RF antenna/matching path is absent.

At 4.5 V on 5V_SYS and an assumed 85% buck efficiency, the simultaneous planning case draws **1.85 A** including 70 mA for the onboard CAN transceiver and 5 mA overhead; at 5 V it draws **1.73 A**. R11 is now **42.2 kΩ, 1%**, giving approximately 2.08 A nominal input current limit (about 1.90–2.27 A with tabulated device limits and resistor tolerance). R34 is **52.3 kΩ, 1%** (sensor limit 448–562 mA); R81 is **88.7 kΩ, 1%** (CAN expansion limit 262–342 mA). The 1.85 A case fits the estimated minimum thresholds, but input startup margin is only about 54 mA: inrush and simultaneous load steps still need qualification. The mux is rated 2.5 A continuous, so the buck's 3 A nameplate is not system capacity. Do not promise 2 A continuous input operation across all current-limit tolerance corners.

Qualify an external regulated source around **5.1 V ±1% at J2**, capable of at least 2 A, with transient control. This is a candidate source specification, pending measurement of the reverse-polarity FET, eFuse, mux, connector/cable and PCB drops. Maintain **at least 4.5 V at IC7 VCC**, whose CAN transceiver is on unswitched 5V_SYS. A generic 4.75 V source at J2 does not establish that margin. Source traces, 0.30 mm thermal spokes, 0.60/0.30 mm via banks and actual filled-plane paths were reviewed with copper-loss calculations; confirm copper/plating and test temperature rise before release. The 0.50 mm POWER default is not a thermal signoff.

**USB is intended for programming/service, but standalone USB cold-start is not yet qualified.** Sensor and CAN-expansion enables have hardware pull-downs and must remain off; radio transmission, SD writes and LEDs must remain disabled. USB also powers the isolated amplifier, LED-driver logic and other 3.3 V loads. A provisional service scenario is about 239 mA at a 4.5 V buck input, exceeding the conventional 100 mA USB pre-enumeration budget. A 500 mA source provides only about 580 mA at 3.3 V at that voltage/efficiency. Measure ROM/download startup and enumeration without application firmware; use external power while programming until qualification, or add documented hardware load gating/source-current detection. The two 5.1 kΩ CC resistors alone do not establish permission to draw 1.5 A or 3 A.

The battery-sense input is **96 V absolute maximum**. F1 is SCHURTER 3403.0266.23, 160 mA time-lag, 250 VDC; verify available fault current against its 1.5 kA DC breaking rating and total clearing energy against the conductors. The 60 A upstream fuse does not automatically protect the sense harness. F1 cannot protect faults upstream of its location. The divider draws only about 95.4 µA at 96 V; each 499 kΩ resistor dissipates 4.54 mW with 47.6 V across it. The AMC3330 input is 0.782 V and differential output about 1.565 V; configure ADS1115 differential AIN0–AIN1 with at least ±2.048 V full scale. Insulation, resistor MPN/voltage ratings and source fault conditions still require release review.



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
