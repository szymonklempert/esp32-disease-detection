import serial
import time

ESP_PORT = "COM3"
ESP_FREQUENCY = 1


def collect_data(n_seconds: int) -> list:
    """

    :int n_seconds: numer of seconds to collect data
    """
    data = []
    ser = serial.Serial(ESP_PORT, 115200)
    # compute how many times we need to read data
    n_readings = n_seconds * ESP_FREQUENCY
    counter = 0

    while counter < n_readings:
        print(ser.in_waiting)
        if ser.in_waiting > 0:
            received_data = ser.readline()
            print("Received data:", received_data)
            received_data = received_data.decode("utf-8")
            print("Received data:", received_data)
            received_data = received_data[5:8]
            print("Received data:", received_data)
            data.append(received_data)
            counter += 1
        time.sleep(1)
    return data

collect_data(10)