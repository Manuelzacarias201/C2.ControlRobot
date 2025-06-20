import tkinter as tk
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pins = [27, 22, 18, 20]  
GPIO.setup(motor_pins, GPIO.OUT)

TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4


def adelante():
    GPIO.output(27, True)
    GPIO.output(22, False)
    GPIO.output(18, False)
    GPIO.output(20, True)

def atras():
    GPIO.output(27, False)
    GPIO.output(22, True)
    GPIO.output(18, True)
    GPIO.output(20, False)

def izquierda():
    GPIO.output(27, True)
    GPIO.output(22, False)
    GPIO.output(18, True)
    GPIO.output(20, False)

def derecha():
    GPIO.output(27, False)
    GPIO.output(22, True)
    GPIO.output(18, False)
    GPIO.output(20, True)

def stop():
    for pin in motor_pins:
        GPIO.output(pin, False)

def salir():
    stop()
    GPIO.cleanup()
    root.quit()


def leer_dht11():
    while True:
        humedad, temperatura = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humedad is not None and temperatura is not None:
            label_temp.config(text=f"Temperatura: {temperatura:.1f}°C")
            label_hum.config(text=f"Humedad: {humedad:.1f}%")
        else:
            label_temp.config(text="Temperatura: Error")
            label_hum.config(text="Humedad: Error")
        time.sleep(1)

def leer_ultrasonico():
    while True:
        GPIO.output(TRIG, False)
        time.sleep(0.05)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            start = time.time()
        while GPIO.input(ECHO) == 1:
            end = time.time()

        duracion = end - start
        distancia = duracion * 17150
        distancia = round(distancia, 2)
        label_dist.config(text=f"Distancia: {distancia} cm")
        time.sleep(1)


root = tk.Tk()
root.title("Control de Robot")
root.geometry("400x400")

label_temp = tk.Label(root, text="Temperatura: ", font=("Arial", 12))
label_temp.pack(pady=5)

label_hum = tk.Label(root, text="Humedad: ", font=("Arial", 12))
label_hum.pack(pady=5)

label_dist = tk.Label(root, text="Distancia: ", font=("Arial", 12))
label_dist.pack(pady=5)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Adelante", width=10, command=adelante).grid(row=0, column=1)
tk.Button(frame_botones, text="Izquierda", width=10, command=izquierda).grid(row=1, column=0)
tk.Button(frame_botones, text="Stop", width=10, command=stop).grid(row=1, column=1)
tk.Button(frame_botones, text="Derecha", width=10, command=derecha).grid(row=1, column=2)
tk.Button(frame_botones, text="Atrás", width=10, command=atras).grid(row=2, column=1)

tk.Button(root, text="Salir", width=10, command=salir).pack(pady=10)

threading.Thread(target=leer_dht11, daemon=True).start()
threading.Thread(target=leer_ultrasonico, daemon=True).start()

root.mainloop()