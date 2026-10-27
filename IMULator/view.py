from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QSlider, QLabel)

class SensorView(QWidget):
    user_interaction = Signal(str, str, float)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de IMUs")
        self.resize(400, 300)

        main_layout = QVBoxLayout(self)
        self.labels = {}

        main_layout.addWidget(self._create_sensor_group("sensor1", "Sensor 1 (Hombro)"))
        main_layout.addWidget(self._create_sensor_group("sensor2", "Sensor 2 (Codo/Antebrazo)"))

    def _create_sensor_group(self, sensor_id: str, title: str) -> QGroupBox:
        group = QGroupBox(title)
        layout = QVBoxLayout()

        layout.addLayout(self._create_slider_row(sensor_id, "roll", "Roll", -180, 180))
        layout.addLayout(self._create_slider_row(sensor_id, "pitch", "Pitch", -90, 90))

        group.setLayout(layout)
        return group

    def _create_slider_row(self, sensor_id: str, axis: str, label_text: str, min_val: int, max_val: int) -> QHBoxLayout:
        layout = QHBoxLayout()
        
        name_label = QLabel(f"{label_text}:")
        name_label.setFixedWidth(40)

        val_label = QLabel("0°")
        val_label.setFixedWidth(40)
        val_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.labels[f"{sensor_id}{axis}"] = val_label

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(0)

        slider.valueChanged.connect(
            lambda val, s=sensor_id, a=axis: self.user_interaction.emit(s, a, float(val))
        )

        layout.addWidget(name_label)
        layout.addWidget(slider)
        layout.addWidget(val_label)
        return layout

    @Slot(dict)
    def update_ui(self, state:dict):
        for sensor_id, axes in state.items():
            for axis, value in axes.items():
                label_key = f"{sensor_id}{axis}"
                if label_key in self.labels:
                    self.labels[label_key].setText(f"{int(value)}°")
