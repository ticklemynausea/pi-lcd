import RPi.GPIO as GPIO

class GPIO_Common(object):
  initialized = False
   
  @classmethod
  def init(self):
    if not self.initialized:
      print("GPIO Initialized")
      GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    else:
      print("GPIO Already Initialized!")