import serial
import detect_and_play as dap
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
		print("Message waiting")
		mess = ReadSerial()
		print("Message is read",dap.distance2Line)
		SendSerial(SentMessage1)