import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
#GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
#GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def isHuman():
    if GPIO.input(GPIO_ECHO) == 1:
	    return True
    return False

if __name__ == '__main__':
    print("test")
    i = 0
    try:
        while True:
            if (isHuman()):
                i = i +1
            print("humans" + str(i))
            time.sleep(0.5)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup
