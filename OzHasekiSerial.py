import serial
def SendSerial(message):
    try:
        ser = serial.Serial('/dev/ttyACM1',9600)
        ser.write(str(message))
    except:
        print('GGWP olduk')
def ReadSerial():
    try:
        ser = serial.Serial('/dev/ttyACM1',9600)
        message = ser.readline()
        return message
    except:
        print('GGWP olduk')
        
def ComLoop(SentMessage):
	while True:
		print("Message waiting")
		mess = ReadSerial()
		print("Message is read",mess)
		