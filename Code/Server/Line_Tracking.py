import time
from Motor import *
import RPi.GPIO as GPIO
IR01 = 14
IR02 = 15
IR03 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR01,GPIO.IN)
GPIO.setup(IR02,GPIO.IN)
GPIO.setup(IR03,GPIO.IN)
class Line_Tracking:
    def run(self):
        stop_count = 0

        while True:
            self.LMR=0x00
            if GPIO.input(IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(IR03)==True:
                self.LMR=(self.LMR | 1)

            if self.LMR == 0:
                #When not input is detected stop after a certain number of step
                stop_count = stop_count + 1

                if(stop_count == 5000):
                    print("No input received after " + str(stop_count) + " -> Stop now!")
                    PWM.setMotorModel(0, 0, 0, 0)
            else:
                stop_count = 0

            if self.LMR==2:
                print("Line tracking command M -> Go straight " + str(self.LMR), flush=True)
                PWM.setMotorModel(800,800,800,800)
            elif self.LMR==4:
                print("Line tracking command L -> Small left " + str(self.LMR), flush=True)
                PWM.setMotorModel(-1500,-1500,2500,2500)
            elif self.LMR==6:
                print("Line tracking command M + L -> Left " + str(self.LMR), flush=True)
                PWM.setMotorModel(-2000,-2000,4000,4000)
            elif self.LMR==1:
                print("Line tracking command R -> Small right " + str(self.LMR), flush=True)
                PWM.setMotorModel(2500,2500,-1500,-1500)
            elif self.LMR==3:
                print("Line tracking command R + M -> Right " + str(self.LMR), flush=True)
                PWM.setMotorModel(4000,4000,-2000,-2000)
            elif self.LMR==7:
                print("Line tracking L + M + R -> Stop!!!!! " + str(self.LMR), flush=True)
                PWM.setMotorModel(0, 0, 0, 0)
                pass

infrared=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
