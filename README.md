# Firmware Installation Guide

## 1. Make sure you have `dfu-util` installed

- **Linux (Debian)**: `sudo apt install dfu-util`
- **MacOS**: `brew install dfu-util`
- **Windows**:
  - Download the `dfu-util` to your local system, e.g., under `D:\dfu-util`.
  - Rename it to `dfu-util.exe`.
  - Append the path of the `dfu-util.exe` to the system environment variable PATH.

## 2. Run `pip install -r requirements.txt`

## 3. Plug in Arduino Giga

## 4. Run `python3 upload_firmware.py {target}`

### {target} can be one of:
- new_hardware
- old_hardware
- new_shield_old_dac_adc

## 5. Feel free to contact `markzakharyan@ucsb.edu` via email or Slack if something isn't working
