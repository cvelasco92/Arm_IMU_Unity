import json
import socket
from PySide6.QtCore import QObject, Slot
from model import SensorModel
from view import SensorView

class SensorController(QObject):

    def __init__(self, model: SensorModel, view: SensorView):
        super().__init__()
        self.model = model
        self.view = view
        # Configuración del cliente UDP
        self.udp_ip = "127.0.0.1"   # Localhost
        self.udp_port = 5005        # Puerto que Unity escucha

        # AF_INET = IPv4 | SOCK_DGRAM = Protocolo UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Conexión de señales y slots
        self.view.user_interaction.connect(self._handle_user_input)         # UI -> Modelo
        self.model.data_updated.connect(self.view.update_ui)                # Modelo -> UI
        self.model.data_updated.connect(self._broadcast_udp)    # Modelo -> Red (Unity)

    @Slot(str, str, float)
    def _handle_user_input(self, sensor_id: str, axis: str, value: float):
        # Se invoca el callback cuando el usuario mueve el slider
        self.model.set_value(sensor_id, axis, value)

    @Slot(dict)
    def _broadcast_udp(self, state: dict):
        # Extrae los valores del diccionario de estado y los envía a Unity
        # uno por uno en formato separado por comas: "SensorID,Roll,Pitch"
        try:
            for sensor_key, axes in state.items():
                # Extraer el número del sensor (de "sensor_1" se obtiene "1")
                sensor_id = ''.join(filter(str.isdigit, sensor_key))

                roll = axes["roll"]
                pitch = axes["pitch"]

                # Formatear la cadena limitando a 2 decimanes para optimizar el envío
                mensaje_unity = f"{sensor_id},{roll:.2f},{pitch:.2f}"

                # Codificar a bytes y enviar al IP/Puerto de Unity
                self.sock.sendto(mensaje_unity.encode('utf-8'), (self.udp_ip, self.udp_port))

                #print(f"[UDP Enviado] {mensaje_unity}")
        except Exception as e:
            print(f"Error al enviar paquete de datos UDP: {e}")