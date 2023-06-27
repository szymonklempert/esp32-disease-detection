import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QCheckBox,
    QButtonGroup,
    QProgressBar,
)
from PyQt6.QtCore import QTimer
import random
import serial

ESP_PORT = "COM3"
ESP_FREQUENCY = 1
ser = serial.Serial(ESP_PORT, 115200)
from app.client import get_stress_level

# Inicjalizacja danych
temperature_data = []
eda_data = []

data_dict = {
    "user_data": {},
    "temp":      [],
    "eda":       []
}

COLLECTION_TIME = 20

# Inicjalizacja wykresów
app = QApplication([])
window = QMainWindow()
central_widget = QWidget()
layout = QHBoxLayout(central_widget)
window.setCentralWidget(central_widget)

# Utworzenie panelu bocznego
side_panel = QGroupBox("Stress level:")
side_panel_layout = QVBoxLayout()
layout.addWidget(side_panel)
side_panel.setLayout(side_panel_layout)

# size_policy = side_panel.sizePolicy()
# size_policy.setHorizontalPolicy(QSizePolicy.Policy.Minimum)
# size_policy.setVerticalPolicy(QSizePolicy.Policy.Minimum)
# side_panel.setSizePolicy(size_policy)
side_panel.setMinimumWidth(150)

# Utworzenie etykiety z komunikatem o alercie
# Utworzenie etykiet z komunikatami o alertach
stress_level_label = QLabel("")
side_panel_layout.addWidget(stress_level_label)

# Utworzenie panelu bocznego z danymi użytkownika
side_panel_user_data = QGroupBox("User Data")
side_panel_user_data_layout = QVBoxLayout()
layout.addWidget(side_panel_user_data)
side_panel_user_data.setLayout(side_panel_user_data_layout)
side_panel_user_data.setMinimumWidth(150)

progress_bar = QProgressBar()
progress_bar.setVisible(False)
progress_label = QLabel("Collecting data...")

# Utworzenie pól wprowadzania danych użytkownika
age_label = QLabel("Age:")
age_input = QLineEdit()
height_label = QLabel("Height:")
height_input = QLineEdit()
weight_label = QLabel("Weight:")
weight_input = QLineEdit()
coffee_label = QLabel("Coffee today:")
coffee_checkbox = QCheckBox()
sport_label = QLabel("Sport today:")
sport_checkbox = QCheckBox()
feeling_ill_label = QLabel("Feeling ill today:")
feeling_ill_checkbox = QCheckBox()
sex_label = QLabel("Sex:")
male_radio = QRadioButton("Male")
female_radio = QRadioButton("Female")
sex_button_group = QButtonGroup()
sex_button_group.addButton(male_radio)
sex_button_group.addButton(female_radio)
smoker_label = QLabel("Are you a smoker?")
smoker_checkbox = QCheckBox()

# Utworzenie przycisku "Save"
bottom_layout = QHBoxLayout()
save_button = QPushButton("Save")

bottom_layout.addWidget(save_button)
bottom_layout.addWidget(progress_label)
bottom_layout.addWidget(progress_bar)

# Dodanie elementów do panelu z danymi użytkownika
side_panel_user_data_layout.addWidget(age_label)
side_panel_user_data_layout.addWidget(age_input)
side_panel_user_data_layout.addWidget(height_label)
side_panel_user_data_layout.addWidget(height_input)
side_panel_user_data_layout.addWidget(weight_label)
side_panel_user_data_layout.addWidget(weight_input)
side_panel_user_data_layout.addWidget(coffee_label)
side_panel_user_data_layout.addWidget(coffee_checkbox)
side_panel_user_data_layout.addWidget(sport_label)
side_panel_user_data_layout.addWidget(sport_checkbox)
side_panel_user_data_layout.addWidget(feeling_ill_label)
side_panel_user_data_layout.addWidget(feeling_ill_checkbox)
side_panel_user_data_layout.addWidget(sex_label)
side_panel_user_data_layout.addWidget(male_radio)
side_panel_user_data_layout.addWidget(female_radio)
side_panel_user_data_layout.addWidget(smoker_label)
side_panel_user_data_layout.addWidget(smoker_checkbox)
side_panel_user_data_layout.addWidget(save_button)

# Utworzenie wykresu temperatury
graphWidget_temp = pg.PlotWidget()
graphWidget_temp.setYRange(30, 45)
layout.addWidget(graphWidget_temp)

# Utworzenie wykresu wilgotności
graphWidget_eda = pg.PlotWidget()
layout.addWidget(graphWidget_eda)

# Ustawienie etykiet osi
graphWidget_temp.setLabel("left", "Temperature")
graphWidget_temp.setLabel("bottom", "Time")
graphWidget_eda.setLabel("left", "Electrodermal activity")
graphWidget_eda.setLabel("bottom", "Time")

# Utworzenie krzywych na wykresach
curve_temp = graphWidget_temp.plot(
    [], [], pen=pg.mkPen("r", width=2), name="Temperature"
)
curve_eda = graphWidget_eda.plot(
    [], [], pen=pg.mkPen("g", width=2), name="Electrodermal activity"
)


# Funkcja wywoływana przy aktualizacji wykresów
def update_chart():
    curve_temp.setData(range(len(temperature_data)), temperature_data)
    curve_eda.setData(range(len(eda_data)), eda_data)


# Parsowanie danych
def parse_data(data):
    # Przykładowe parsowanie danych
    # Zakładamy, że dane mają format "Temp: X C, eda: Y %, Pressure: Z hPa"
    parts = data.split(",")
    temperature = float(parts[0].split(":")[1].strip())
    eda = float(parts[1].split(":")[1].strip())
    return temperature, eda


collection_time = 0
collection_timer = QTimer()


# Function to start data collection
def start_data_collection():
    # Clear existing data
    global collection_time
    global temperature_data
    global eda_data
    temperature_data = []
    eda_data = []
    collection_time = 0
    data_dict["temp"] = []
    data_dict["eda"] = []




    # Start collecting data for 10 seconds
    collection_timer.start(1000)  # Start the QTimer to trigger data collection every second

    # Disable the start button to prevent multiple starts
    save_button.setEnabled(False)
    print("Collecting data.", end="")

    # Show the progress bar
    progress_bar.setValue(0)
    progress_bar.setMaximum(COLLECTION_TIME)
    progress_bar.setWindowTitle("Collecting data... Remain still!")
    progress_bar.setFixedSize(500, 60)
    progress_bar.setVisible(True)


# Function to handle data collection
def collect_data():
    global collection_time


    # Odczyt danych z urządzenia (emulacja)
    temperature = 36.6 + random.uniform(-.1, 1)
    temperature_data.append(temperature)
    eda = 0

    while True:
        if ser.in_waiting > 0:
            received_data = ser.readline()
            # print("Received data original:", received_data)
            received_data = received_data.decode("utf-8")
            # print("Received data decoded:", received_data)
            received_data = received_data.split("b")[1].strip().replace('\'', '')
            # print("Received data:", received_data)
            if received_data == '' or received_data == ' ':
                continue
            try:
                eda = float(received_data)
            except ValueError:
                eda = 0
            print("Received data:", eda)
            # data.append(received_data)
            break

    # fake_data
    data = f"Temp: {temperature}, EDA: {eda}"
    eda_data.append(eda)

    # Przetwarzanie odczytanych danych
    if data:
        temperature, eda = parse_data(data)

        # Dodawanie danych do list
        data_dict["temp"].append(temperature)
        data_dict["eda"].append(eda)
    print(".", end="")
    # Increase collection time by 1 second
    collection_time += 1

    progress_bar.setValue(collection_time)

    # Stop collecting data after 10 seconds
    if collection_time >= COLLECTION_TIME:
        collection_timer.stop()  # Stop the QTimer
        save_button.setEnabled(True)  # Re-enable the start button
        progress_bar.setVisible(False)

        # Print collected data
        print("Collected Data:")
        print(data_dict)
        print("---")

        result = get_stress_level(data_dict)
        stress_level_label.setText(result)
        stress_level_label.setStyleSheet("color: red")


collection_timer.timeout.connect(collect_data)


# Funkcja obsługująca zapis danych użytkownika
def save_user_data():
    age = age_input.text()
    height = height_input.text()
    weight = weight_input.text()
    coffee_today = coffee_checkbox.isChecked()
    sport_today = sport_checkbox.isChecked()
    feeling_ill_today = feeling_ill_checkbox.isChecked()
    sex = male_radio.isChecked()
    smoker = smoker_checkbox.isChecked()

    # Tutaj możesz zapisać dane do zmiennych w programie lub wykonać inną operację
    # np. zapis do pliku, przekazanie do bazy danych itp.
    # W tym przykładzie, dane są wyświetlane w konsoli.
    data_dict["user_data"] = {
        "age":                   age,
        "height":                height,
        "weight":                weight,
        "coffee_today_YES":      coffee_today,
        "sport_today_YES":       sport_today,
        "feeling_ill_today_YES": feeling_ill_today,
        "gender":                sex,
        "smoker":                smoker
    }

    print("User Data:")
    print(f"Age: {age}")
    print(f"Height: {height}")
    print(f"Weight: {weight}")
    print(f"Coffee today: {coffee_today}")
    print(f"Sport today: {sport_today}")
    print(f"Feeling ill today: {feeling_ill_today}")
    print(f"Sex: {sex}")
    print(f"Smoker: {smoker}")
    print("---")


def reset():
    global collection_time
    collection_time = 0
    collection_timer.stop()  # Stop the QTimer
    save_button.setEnabled(True)  # Re-enable the start button
    progress_bar.setVisible(False)
    temperature_data.clear()
    eda_data.clear()
    data_dict.clear()
    stress_level_label.setText("")
    print("Reset")


# Podłączenie funkcji obsługującej zapis danych do przycisku "Save"
save_button.clicked.connect(save_user_data)
save_button.clicked.connect(start_data_collection)

# Timer do aktualizacji wykresów co sekundę
timer = QTimer()
timer.timeout.connect(update_chart)
timer.start(1000)

# Wyświetlenie aplikacji
window.show()
app.exec()
