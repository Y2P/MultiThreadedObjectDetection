import serial
def SendSerial(message):
    try:
        ser = serial.Serial('/dev/ttyACM0',9600)
        ser.write(str(message))
    except:
        print('GGWP olduk = send')
def ReadSerial():
    try:
        ser = serial.Serial('/dev/ttyACM0',9600)
        message = ser.readline()
        return message
    except:
        print('GGWP olduk = read')
        
def ComLoop(SentMessage1,SentMessage2):
        ser = serial.Serial('/dev/ttyACM0',9600)

	while True:
		print("Message waiting")
		#mess = ReadSerial()
                message = ser.readline()
		print("Message is read",message)
        #		SendSerial(SentMessage1)
             
