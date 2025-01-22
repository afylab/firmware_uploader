import serial
import time
import os
import subprocess
import serial.tools.list_ports

def find_giga_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.description is not None and port.manufacturer is not None and "Giga" in port.description and "Arduino" in port.manufacturer:
            return port.device
    return None

def trigger_dfu_mode(port):
    try:
        with serial.Serial(port, 1200, timeout=1) as ser:
            ser.close()
            print(f"Triggered DFU mode on {port}.")
        time.sleep(2)
    except Exception as e:
        print(f"Error triggering DFU mode: {e}")

def upload_firmwareM4(firmware_name):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        firmware_path = os.path.join(script_dir, 'firmware', firmware_name)
        subprocess.run([
            "dfu-util",
            "-a", "0",
            "-s", "0x08100000:leave",
            "-D", firmware_path
        ], check=True)
        print(f"M{firmware_name[9]} firmware uploaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error uploading firmware: {e}")

def upload_firmwareM7(firmware_name):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        firmware_path = os.path.join(script_dir, 'firmware', firmware_name)
        subprocess.run([
            "dfu-util",
            "-a", "0",
            "-s", "0x08040000:leave",
            "-D", firmware_path
        ], check=True)
        print(f"M{firmware_name[9]} firmware uploaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error uploading firmware: {e}")

def nop_test():
    try:
        with serial.Serial(port, 115200, timeout=2) as ser:
            print()
            print(f"Testing NOP on {ser.port}...")
            
            ser.write("NOP\r\n".encode())
            
            response = ser.readline().decode().strip()
            
            if response == "NOP":
                print("NOP test passed: Correct response received.")
            else:
                print(f"NOP test failed: Expected 'nop', but received '{response}'")
                return
            
            
            ser.write("*IDN?\r\n".encode())
            id = ser.readline().decode().strip()
            
            ser.write("SERIAL_NUMBER\r\n".encode())
            serial_number = ser.readline().decode().strip()
            
            print()
            print(f"ID: {id}, Serial Number: {serial_number}")
            print(f"Firmware successfully uploaded.")
            
    except Exception as e:
        print(f"Error during NOP test: {e}")

if __name__ == "__main__":
    port = find_giga_port()
    if port:
        print()
        print(f"Found Arduino GIGA on {port}")
        print("Uploading M7 firmware...")
        trigger_dfu_mode(port)
        time.sleep(0.5)
        upload_firmwareM7('firmwareM7.bin')
        
        print()
        print("Waiting for M7 firmware to boot...")
        time.sleep(2)
        print("Uploading M4 firmware...")
        trigger_dfu_mode(port)
        time.sleep(0.5)
        upload_firmwareM4('firmwareM4.bin')
        print()
        print("Waiting for M4 firmware to boot...")
        time.sleep(2)
        
        nop_test()
    else:
        print("Arduino GIGA not found. Make sure it is connected.")
