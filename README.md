# Simulador de IMUs y Visualización Cinemática (Workshop)

Este repositorio contiene la arquitectura cliente-servidor (UDP) diseñada para la captura, emulación y visualización en tiempo real de la cinemática de un brazo humano (modelo Denavit-Hartenberg de 2 GDL en hombro y 1 GDL en codo). 

El proyecto está dividido en dos módulos independientes:
1. **PythonEmulator:** Emulador con interfaz gráfica (PySide6) que actúa como Cliente UDP.
2. **UnityServer:** Entorno de visualización 3D en Unity 6 que actúa como Servidor UDP.

## 🛠️ Requisitos Previos
* **Python 3.12** o superior.
* **Unity 6** (o compatible).

## 🚀 Instrucciones de Ejecución

### 1. Preparar el Emulador (Python)
Abre tu terminal, navega a la carpeta del proyecto y ejecuta:

```bash
cd PythonEmulator
pip install -r requirements.txt
python main.py
```

Esto abrirá la interfaz de PySide6. Los *sliders* envían datagramas UDP automáticamente al puerto `5005` de tu red local en formato `ID,Roll,Pitch`.

### 2. Preparar el Entorno Visual (Unity)
1. Abre Unity Hub y añade el proyecto seleccionando la carpeta `ArmIMU_Workshop`.
2. Abre la escena principal que contiene el `NetworkManager` (IMUDenavitHartenberg.cs) y los modelos del brazo.
3. Presiona el botón de **Play**.
4. Ejecuta `main.py`. Al mover los *sliders* en la ventana de Python, verás la actualización cinemática en tiempo real en Unity.

## 📚 Citas y Agradecimientos Académicos

Este software es de código abierto (Licencia MIT) y su uso es libre para experimentación y desarrollo. Sin embargo, si utilizas este repositorio, código o arquitectura como parte de tu proyecto de grado, tesis de maestría/doctorado, o publicación científica, **es un requisito indispensable otorgar el crédito correspondiente**.

* **Cita en Bibliografía:** Debes incluir el enlace directo a este repositorio de GitHub en tu sección de referencias.
* **Agradecimientos:** Por favor, menciona explícitamente el uso de esta herramienta y a sus creadores en la sección de "Agradecimientos" (Acknowledgments) de tu documento. Al otorgar este crédito, contribuyes a dar visibilidad y apoyo a proyectos de investigación en ingeniería mecatrónica, computación biomédica y física biomédica.