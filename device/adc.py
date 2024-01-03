import smbus
import time
import sys

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40

def analogRead(chn):
    try:
        value = bus.read_byte_data(address, cmd+chn)
        print value
        return value
    except:
        return("error")

    

def analogWrite(value):
    try:
        bus.write_byte_data(address, cmd, value)
    except:
        return("error")
def loop():
    counter =0
    while True:
        counter = counter+1
        value = analogRead(0)
        volatge = value/255.0*3.3
        sys.stdout.write(u"\u001b[1000D"+str(counter)+" voltage "+str(value)+" Voltaeg: "+str(volatge)+".")
        sys.stdout.flush()
        time.sleep(0.01)

def destroy():
    bus.close()

if __name__ == '__main__':
    print('program is starting...')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
