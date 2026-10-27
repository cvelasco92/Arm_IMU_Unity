using System;
using System.Globalization;
using System.Net;
using System.Net.Sockets;
using System.Numerics;
using System.Text;
using System.Threading;
using Unity.VisualScripting;
using UnityEngine;

// Estructuras de parseo del JSON de Python
[Serializable]
public class SensorData
{
    public float roll;
    public float pitch;
}

[Serializable]
public class StateData
{
    public SensorData sensor1;
    public SensorData sensor2;
}
public class IMUDenavitHartenberg : MonoBehaviour
{
    [Header("Eslabones del Brazo Izquierdo (Modelo 3D)")]
    public Transform hombroTransform;
    public Transform codoTransform;

    [Header("Configuración de Red")]
    public int udpPort = 5005;

    // Red y concurrencia
    private UdpClient udpClient;
    private Thread receiveThread;
    private bool isListening = false;

    // Almacenamiento seguro entre hilos
    private readonly object stateLock = new object();
    private StateData currentState = new StateData();

    void Start()
    {
        // Activar la ejecución en segundo plano.
        
        Application.runInBackground = true;
        // Inicializar estado en 0
        currentState.sensor1 = new SensorData();
        currentState.sensor2 = new SensorData();

        // Iniciar el hilo secundario para no bloquear el framerate de Unity
        isListening = true;
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
        Debug.Log($"[UDP] Escuchando en el puerto {udpPort}...");
    }

    private void ReceiveData()
    {
        udpClient = new UdpClient(udpPort);
        IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);

        while(isListening)
        {
            try
            {
                byte[] data = udpClient.Receive(ref anyIP);
                string textData = Encoding.UTF8.GetString(data);

                // Separar la cadena por comas
                string[] parts = textData.Split(',');

                if(parts.Length == 3)
                {
                    // Parsear los valores
                    int sensorId = int.Parse(parts[0]);
                    float roll = float.Parse(parts[1], CultureInfo.InvariantCulture);
                    float pitch = float.Parse(parts[2], CultureInfo.InvariantCulture);

                    // Bloquear el hilo temporalmente para actualizar el estado de lforma segura
                    lock (stateLock)
                    {
                        if (sensorId == 1) // Datos del Hombro
                        {
                            currentState.sensor1.roll = roll;
                            currentState.sensor1.pitch = pitch;
                        }
                        else if (sensorId == 2) // Datos del Codo
                        {
                            currentState.sensor2.roll = roll;
                            currentState.sensor2.pitch = pitch;
                        }
                    }
                }
            }
            catch (Exception e)
            {
                if (isListening) Debug.LogWarning($"[UDP] Error de recepción: {e.Message}");
            }
        }
    }

    void Update()
    {
        // Extraer los datos seguros para usarlos en el hilo principal
        StateData frameState;
        lock (stateLock)
        {
            frameState = currentState;
        }
        // Hombro (Sensor 1)
        // theta_1 (Abducción o aleteo), theta_2 (Flexión o balanceo)
        float theta1_abd = frameState.sensor1.roll;
        float theta2_flex = frameState.sensor1.pitch;

        // Rig estándar: Z adelante, X tranversal
        hombroTransform.localEulerAngles = new UnityEngine.Vector3(theta2_flex, 0f, theta1_abd);

        // Codo (Sensor 2)
        // theta_3 (Flexión/Extensión). Codo como bisagra, solo rota un eje.
        float theta3_codoFlex = frameState.sensor2.pitch;

        // El codo solo afecta el eje que corresponde a la flexión transversal (X local)
        codoTransform.localEulerAngles = new UnityEngine.Vector3(theta3_codoFlex, 0f, 0f);
    }

    void OnApplicationQuit()
    {
        // Cerrar el socket y el hilo al terminar el programa
        isListening = false;
        if (udpClient != null) udpClient.Close();
        if (receiveThread != null) receiveThread.Abort();
    }
}
