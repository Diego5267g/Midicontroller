import machine
from machine import UART
from machine import Pin, SoftI2C
from HC1SR04 import HCSR04
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=400000)  
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
sensor_der = HCSR04(trigger_pin=19, echo_pin=18, echo_timeout_us=25000)
sensor_izq = HCSR04(trigger_pin=25, echo_pin=26, echo_timeout_us=25000)

uart = machine.UART(0, baudrate=115200)


def limitarD(distancia_der):
    if (distancia_der >= 30):
        distancia_der  == 30
    return distancia_der

def limitarI(distancia_izq):
    if (distancia_izq >= 30):
        distancia_izq = 30
    return distancia_izq

def conversion(distancia_izq):
    rango = limitarI(distancia_izq)
    valor_midi = int((rango/30)*127)
    return valor_midi

def conversionIzq(distancia_izq):
    rango = conversion(distancia_izq)
    note_off = 0x80
    note_on = 0xC0
    velocidad = 100
    if rango:
        return bytes([note_on, rango, velocidad])
    else:
        return bytes([note_off, 0, 0])

def conversionDer(distancia_der):
    rango = limitarD(distancia_der)
    note_off = 0x80
    note_on = 0x90
    velocidad = 50
    if rango < 4:
        return bytes([note_on, 60, velocidad])
    elif rango < 6:
        return bytes([note_on, 61, velocidad])
    elif rango < 8:
        return bytes([note_on, 62, velocidad])
    elif rango < 10:
        return bytes([note_on, 63, velocidad])
    elif rango < 12:
        return bytes([note_on, 64, velocidad])
    elif rango < 14:
        return bytes([note_on, 65, velocidad])
    elif rango < 16:
        return bytes([note_on, 66, velocidad])
    elif rango < 18:
        return bytes([note_on, 67, velocidad])
    elif rango < 20:
        return bytes([note_on, 68, velocidad])
    elif rango < 22:
        return bytes([note_on, 69, velocidad])
    elif rango < 24:
        return bytes([note_on, 70, velocidad])
    elif rango < 26:
        return bytes([note_on, 71, velocidad])
    elif rango < 30:
        return bytes([note_off, 0, 0])
    else:
        return bytes([note_off, 0, 0])

def pantallaDer(distancia_der):
    rango = limitarD(distancia_der)

    if rango < 4:
        return 'Nota: C'
    elif rango < 6:
        return 'Nota: C#'
    elif rango < 8:
        return 'Nota: D'
    elif rango < 10:
        return 'Nota: D#'
    elif rango < 12:
        return 'Nota: E'
    elif rango < 14:
        return 'Nota: F'
    elif rango < 16:
        return 'Nota: F#'
    elif rango < 18:
        return 'Nota: G'
    elif rango < 20:
        return 'Nota: G#'
    elif rango < 22:
        return 'Nota: A'
    elif rango < 24:
        return 'Nota: A#'
    elif rango < 28:
        return 'Nota: B'
    elif rango < 30:
        return 'Nota:'
    else:
        return ''

def enviar_nota():
    distancia_der = sensor_der.distance_cm()
    distancia_izq = sensor_izq.distance_cm()
    mensaje_der = conversionDer(distancia_der)
    mensaje_izq = conversionIzq(distancia_izq)
    uart.write(mensaje_der)
    uart.write(mensaje_izq)
    
while True:
    dis = str(pantallaDer(sensor_der.distance_cm()))
    lcd.putstr(dis)
    enviar_nota()
    sleep(0.1)
    lcd.clear()
    