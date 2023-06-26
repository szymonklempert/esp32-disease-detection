import os
import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QGroupBox, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QPushButton, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt, QTimer
import random

# Inicjalizacja danych
temperature_data = []
humidity_data = []
pressure_data = []

# Inicjalizacja wykresów
app = QApplication([])
window = QMainWindow()
central_widget = QWidget()
layout = QHBoxLayout(central_widget)
window.setCentralWidget(central_widget)

# Utworzenie panelu bocznego z danymi użytkownika
side_panel_user_data = QGroupBox("User Data")
side_panel_user_data_layout = QVBoxLayout()
side_panel_user_data.setLayout(side_panel_user_data_layout)

# Utworzenie pól wprowadzania danych użytkownika
age_label = QLabel("Age:")
age_input = QLineEdit()
height_label = QLabel("Height:")
height_input = QLineEdit()
weight_label = QLabel("Weight:")
weight_input = QLineEdit()
coffee_label = QLabel("Coffee today:")
coffee_checkbox = QCheckBox()
feeling_ok_label = QLabel("Feeling okay today:")
feeling_ok_checkbox = QCheckBox()
sex_label = QLabel("Sex:")
male_radio = QRadioButton("Male")
female_radio = QRadioButton("Female")
sex_button_group = QButtonGroup()
sex_button_group.addButton(male_radio)
sex_button_group.addButton(female_radio)

# Utworzenie przycisku "Save"
save_button = QPushButton("Save")

# Dodanie elementów do panelu z danymi użytkownika
side_panel_user_data_layout.addWidget(age_label)
side_panel_user_data_layout.addWidget(age_input)
side_panel_user_data_layout.addWidget(height_label)
side_panel_user_data_layout.addWidget(height_input)
side_panel_user_data_layout.addWidget(weight_label)
side_panel_user_data_layout.addWidget(weight_input)
side_panel_user_data_layout.addWidget(coffee_label)
side_panel_user_data_layout.addWidget(coffee_checkbox)
side_panel_user_data_layout.addWidget(feeling_ok_label)
side_panel_user_data_layout.addWidget(feeling_ok_checkbox)
side_panel_user_data_layout.addWidget(sex_label)
side_panel_user_data_layout.addWidget(male_radio)
side_panel_user_data_layout.addWidget(female_radio)
side_panel_user_data_layout.addWidget(save_button)

# Utworzenie wykresu temperatury
graphWidget_temp = pg.PlotWidget()
graphWidget_temp.setLabel("left", "Temperature")
graphWidget_temp.setLabel("bottom", "Time")

# Utworzenie panelu bocznego z wykresem temperatury
side_panel_charts = QGroupBox("Charts")
side_panel_charts_layout = QVBoxLayout()
side_panel_charts_layout.addWidget(graphWidget_temp)
side_panel_charts.setLayout(side_panel_charts_layout)

# Utworzenie panelu bocznego z alertami
side_panel_alerts = QGroupBox("Alerts")
side_panel_alerts_layout = QVBoxLayout()
side_panel_alerts.setLayout(side_panel_alerts_layout)

# Utworzenie etykiet z komunikatami o alertach
alert_temperature_label = QLabel("")
alert_humidity_label = QLabel("")
alert_pressure_label = QLabel("")
side_panel_alerts_layout.addWidget(alert_temperature_label)
side_panel_alerts_layout.addWidget(alert_humidity_label)
side_panel_alerts_layout.addWidget(alert_pressure_label)

# Dodanie paneli do głównego layoutu
layout.addWidget(side_panel_user_data)
layout.addWidget(side_panel_charts)
layout.addWidget(side_panel_alerts)

# Funkcja wywoływana przy aktualizacji wykresu i alertów
def update_chart():
    # Odczyt danych z urządzenia (emulacja)
    temperature = random.uniform(20, 30)
    humidity = random.uniform(50, 70)
    pressure = random.uniform(1000, 1100)
    
    # fake_data
    data = f"Temp: {temperature}, Humidity: {humidity}, Pressure: {pressure}"

    # Przetwarzanie odczytanych danych
    if data:
        temperature, humidity, pressure = parse_data(data)

        # Dodawanie danych do list
        temperature_data.append(temperature)
        humidity_data.append(humidity)
        pressure_data.append(pressure)

        # Aktualizacja danych na wykresie temperatury
        curve_temp.setData(range(len(temperature_data)), temperature_data)

        # Sprawdzanie alertów
        check_alerts(temperature, humidity, pressure)

# Parsowanie danych
def parse_data(data):
    # Przykładowe parsowanie danych
    # Zakładamy, że dane mają format "Temp: X C, Humidity: Y %, Pressure: Z hPa"
    parts = data.split(',')
    temperature = float(parts[0].split(':')[1].strip())
    humidity = float(parts[1].split(':')[1].strip())
    pressure = float(parts[2].split(':')[1].strip())
    return temperature, humidity, pressure

# Sprawdzanie alertów
def check_alerts(temperature, humidity, pressure):
    if temperature > 25:
        alert_temperature_label.setText("Temperature too high")
        alert_temperature_label.setStyleSheet("color: red")
    else:
        alert_temperature_label.setText("")
        alert_temperature_label.setStyleSheet("")

    if humidity > 60:
        alert_humidity_label.setText("Humidity too high")
        alert_humidity_label.setStyleSheet("color: red")
    else:
        alert_humidity_label.setText("")
        alert_humidity_label.setStyleSheet("")

    if pressure > 1050:
        alert_pressure_label.setText("Pressure too high")
        alert_pressure_label.setStyleSheet("color: red")
    else:
        alert_pressure_label.setText("")
        alert_pressure_label.setStyleSheet("")

# Funkcja obsługująca zapis danych użytkownika
def save_user_data():
    age = age_input.text()
    height = height_input.text()
    weight = weight_input.text()
    coffee_today = coffee_checkbox.isChecked()
    feeling_ok_today = feeling_ok_checkbox.isChecked()
    sex = "Male" if male_radio.isChecked() else "Female"

    # Tutaj możesz zapisać dane do zmiennych w programie lub wykonać inną operację
    # np. zapis do pliku, przekazanie do bazy danych itp.
    # W tym przykładzie, dane są wyświetlane w konsoli.
    print("User Data:")
    print(f"Age: {age}")
    print(f"Height: {height}")
    print(f"Weight: {weight}")
    print(f"Coffee today: {coffee_today}")
    print(f"Feeling okay today: {feeling_ok_today}")
    print(f"Sex: {sex}")
    print("---")

# Podłączenie funkcji obsługującej zapis danych do przycisku "Save"
save_button.clicked.connect(save_user_data)

# Timer do aktualizacji wykresu co sekundę
timer = QTimer()
timer.timeout.connect(update_chart)
timer.start(1000)

# Wyświetlenie aplikacji
window.show()
app.exec()