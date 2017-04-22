import serial
import SetTrackBar as ST

def SendSerial(message):
    try:
        ser = serial.Serial('/dev/ttyUSB0',9600)
        ser.write(str(message))
    except:
        print('GGWP olduk')
def ReadSerial():
    try:
        ser = serial.Serial('/dev/ttyUSB0',9600)
        message = ser.readline()
        return message
    except:
        print('GGWP olduk')
        
def ComLoop(SentMessage1,SentMessage2):
    ser = serial.Serial('/dev/ttyACM0',9600)
    while true:
        print("Message waiting")
        mess = ser.readline()
        print("Message is read",mess)
        ser.write(str(ST.distance2Line))
