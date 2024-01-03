import serial,time
from serial import Serial
try:
    try:
        phone = serial.Serial("/dev/ttyUSB0", 9600, timeout=5)
    except:
        phone = serial.Serial("/dev/ttyUSB3", 9600, timeout=5)
except:
    phone = serial.Serial("/dev/ttyUSB3", 9600, timeout=5)

def write(strz):
    phone.write(strz.encode()+b'\r')

def read():
    results=[]
    while True:
        z = phone.readline().decode()
        print(z)
        if len(z)==0:
            break
        else:
            if (z == " "):
                pass
            else:
                results.append(z.replace('\r','').replace('\n',''))

    resultz = []
    for i in results:
        if len(i)!=0:
            resultz.append(i)
    return resultz

def send_msg(msg, target):
    write('ATZ')
    time.sleep(0.5)
    write('AT+CMGF=1')
    time.sleep(0.5)
    write('AT+CMGS=' + target)
    time.sleep(0.5)
    write(msg)
    time.sleep(0.5)
    write(chr(26))
    return(read())

def GetAllSMS():
    write('AT+CMGL="REC UNREAD"')
    return(read())

def test():
    write("at+creg?")
    return(read())

if __name__ =="__main__":
#    print(test())
#    print(GetAllSMS())
    send_msg("test",'"+19253991595"') 

