import RPi.GPIO as GPIO
import time
import sys
import os
import code
from lib.settings import held_short_duration, held_long_duration
from datetime import datetime


def timestamp_ms():
  import time as time_
  return int(round(time_.time() * 1000))
    
class Action(object):
  switch_all = "SWITCH_ALL"
  switch_released = "SWITCH_RELEASED"
  switch_pressed = "SWITCH_PRESSED"
  switch_held_short = "SWITCH_HELD_SHORT"
  switch_held_long = "SWITCH_HELD_LONG"

class Switch(object):
  def __init__(self, GPIO_num, callbacks): 
    #
    #code.interact(local=locals())
    print("Init switch on GPIO BCM #%s" % (GPIO_num))

    # default callbacks for switch object
    self.callbacks = {
      Action.switch_all : None, #self.print_status, 
      Action.switch_released : None, #self.print_status,
      Action.switch_pressed : None, #self.print_status,
      Action.switch_held_short : None, #self.print_status,
      Action.switch_held_long : None, #self.print_status
    }
    
    # Setup callbacks
    if callbacks is not None:
      self.callbacks  = { x : callbacks[x] if x in callbacks.keys() else y for x, y in self.callbacks.items()} 
    
    # Setup GPIO pin
    GPIO.setup(GPIO_num, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    
    # GPIO BCM number
    self.GPIO_num = GPIO_num
    
    # Switch states
    self.current_input = 0
    self.previous_input = self.current_input
    self.is_pressed = False
    self.is_pressed_short = False
    self.is_pressed_long = False
    self.timestamp_pressed = timestamp_ms()

        
  def print_status(self, event, delta = None):
    print("%s %s %s %s ms" % (self.GPIO_num, self.current_input, event, delta))
    
  def callback(self, event, delta = None):
    try:
      if self.callbacks[event] is not None:
        self.callbacks[event](event, delta)

    except KeyError:
      assert(false)
      
  def add_callback(self, event, callback = None):
    self.callbacks[event] = callback

  def tick(self):
    
    #
    self.current_input = GPIO.input(self.GPIO_num)

    # switch was pressed
    if (self.current_input and not self.previous_input):
      self.is_pressed = True
      self.timestamp_pressed = timestamp_ms()
      self.callback(Action.switch_pressed, 0)

    # how long the switch has been pressed (ms)
    self.pressed_delta = timestamp_ms() - self.timestamp_pressed

    if (self.is_pressed and not self.is_pressed_short and self.pressed_delta > 1000):  
      self.is_pressed_short = True     
      self.callback(Action.switch_held_short, self.pressed_delta)
      
    if (self.is_pressed and not self.is_pressed_long and self.pressed_delta > 5000):  
      self.is_pressed_long = True
      self.callback(Action.switch_held_long, self.pressed_delta)

    # switch was released    
    if (self.previous_input and not self.current_input):
      self.is_pressed = False
      self.is_pressed_long = False
      self.is_pressed_short = False
      self.timestamp_pressed = timestamp_ms()
      self.callback(Action.switch_released, self.pressed_delta)

    if (self.current_input != self.previous_input):
      self.previous_input = self.current_input

class SwitchController(object):

  def __init__(self, GPIO_config):
    self.GPIO_switches = {}
    
    for GPIO_num, callback in GPIO_config.items():
      self.GPIO_switches[GPIO_num] = Switch(GPIO_num, callback)

  def add_callback(self, GPIO_num, event, callback = None):
    self.GPIO_switches[GPIO_num].add_callback(event, callback)

  def routine(self):
    for GPIO_num, Switch in self.GPIO_switches.items():
      Switch.tick()

  def tick(self):
    try:
      self.routine()

    except KeyboardInterrupt:
      GPIO.cleanup()

