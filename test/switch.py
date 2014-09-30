from lib.gpio_common import GPIO_Common
from lib.switch import SwitchController, Action
from lib.settings import tick_delay
from time import sleep
import subprocess


#
# YOU MUST Initialize GPIO in BCM mode
#
GPIO_Common.init()

#
# YOU SHOULD refer to the switches by name instead of GPIO number
#
class Switch:
  A = 4
  B = 22
  C = 27
  D = 17

#
# YOU CAN declare the callback function explicily
#
def callback_switch_C_held_short(event, delta):
  print("Button C was held for a short duration")

def callback_switch_D_released(event, delta):
  print("Button D was released")

def callback_switch_B_released(event, delta):
  print("Button B was released after %s ms" % delta)  
#
# YOU MUST Initialize a SwitchController object
# YOU CAN Initialize default actions by passing a dictionary to the constructor like this
#
switch_controller = SwitchController({ 
  # YOU CAN assign an anonymous function as a callback for a specific event
  Switch.A : {
    Action.switch_all : lambda event, delta: print("[A] button triggered an event"),
    Action.switch_pressed : lambda event, delta: print("[A] button was pressed"),
    Action.switch_held_short : lambda event, delta: print("[A] button was held for a short time"),
    Action.switch_held_long : lambda event, delta: print("[A] button was held for a long time"),
    Action.switch_released : lambda event, delta: print("[A] button was released after %s ms!" % delta)
  },

  Switch.B : {
    Action.switch_held_short : lambda event, delta: print("HELD SHORT C")
  },

  # YOU MUST assign a callback to an event on a button after declaring it
  Switch.C : {
    Action.switch_pressed : callback_switch_C_held_short
  },

  Switch.D : {
    Action.switch_released : callback_switch_D_released
  }
  # YOU CAN assign a GPIO BCM number for every pin
  # Switch.E : None
})

# YOU CAN override your previous definitions
switch_controller.add_callback(Switch.A, Action.switch_held_short, lambda event, delta: print("omg! Held GPIO switch #22 for a little while"))

# YOU CAN define new callbacks
switch_controller.add_callback(Switch.B, Action.switch_released, callback_switch_B_released)

while True:
    switch_controller.tick()
    sleep(tick_delay)
    
