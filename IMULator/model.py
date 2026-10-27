from PySide6.QtCore import QObject, Signal

class SensorModel(QObject):
    data_updated = Signal(dict)

    def __init__(self):
        super().__init__()
        self._state = {
            "sensor1": {"roll": 0.0, "pitch": 0.0},
            "sensor2": {"roll": 0.0, "pitch": 0.0}
        }

    def set_value(self, sensor_id: str, axis: str, value: float):
        if self._state[sensor_id][axis] != value:
            self._state[sensor_id][axis] = value
            self.data_updated.emit(self._state)

    def get_state(self) -> dict:
        return self._state