from lib.gpio_common import GPIO_Common
from lib.switch import SwitchController, Action
from lib.settings import tick_delay
from time import sleep
import subprocess


# This callback can be used


subprocess.call("pwd", shell=True)

GPIO_Common.init()
switch_controller = SwitchController({ 
  4 : {
    Action.switch_pressed : lambda event, delta: print("eheh")
  },
  17 : None,
  22 : None,
  27 : None
})

switch_controller.add_callback(22, Action.switch_held_short, lambda event, delta: print("omg! Held GPIO switch #22 for a little while"))
switch_controller.add_callback(27, Action.switch_released, lambda event, delta : print("LOL released switch 27 after %s ms!" % delta))

while True:
    switch_controller.tick()
    sleep(tick_delay)
    
