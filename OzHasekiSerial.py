import serial
def SendSerial(message):
    try:
        ser = serial.Serial('/dev/ttyACM1',9600)
        ser.write(str(message))
    except:
        print('GGWP olduk')
        
