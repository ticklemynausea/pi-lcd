
# Based on HD44780 LCD Test Script for the Raspberry Pi
# Author : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk
# Date   : 26/07/2012

 
import RPi.GPIO as GPIO
from lib.util_common import timestamp_ms
import time
 
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

class DisplayController(object):
 
  # Define GPIO to LCD mapping
  LCD_RS = 7
  LCD_E  = 8
  LCD_D4 = 25
  LCD_D5 = 24
  LCD_D6 = 23
  LCD_D7 = 18
   
  # Define some device constants
  LCD_WIDTH = 16    # Maximum characters per line
  LCD_CHR = True
  LCD_CMD = False
   
  LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
  LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 
   
  # Timing constants
  E_PULSE = 0.00005
  E_DELAY = 0.00005


  def __init__(self, callback, wait_time):
  

    self.callback = callback
    self.wait_time = wait_time
    self.waiting_since = timestamp_ms()

    self.animation_status = {
      DisplayController.LCD_LINE_1 : [0, 0],
      DisplayController.LCD_LINE_2 : [0, 0]
     }
    
    GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
    GPIO.setup(DisplayController.LCD_E, GPIO.OUT)  # E
    GPIO.setup(DisplayController.LCD_RS, GPIO.OUT) # RS
    GPIO.setup(DisplayController.LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(DisplayController.LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(DisplayController.LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(DisplayController.LCD_D7, GPIO.OUT) # DB7

    # Initialise display
    self.lcd_init()

  def set_callback(self, callback):
    self.callback = callback
    
  def set_wait_time(self, wait_time):
    self.wait_time = wait_time

  # Send some test
  def text(self, line, text):

    assert(line in [DisplayController.LCD_LINE_1, DisplayController.LCD_LINE_2])

    self.lcd_byte(line, DisplayController.LCD_CMD)

    self.lcd_string(text)

  # scroll line on the screen
  def scroll(self, line, text, increment = 1):

    assert(line in [DisplayController.LCD_LINE_1, DisplayController.LCD_LINE_2])


    text = " " * 16 + text

    self.lcd_byte(line, DisplayController.LCD_CMD)
    
    i = self.animation_status[line][0]
    
    text_slice = text[i : i + 16]

    self.lcd_string(text_slice)

    i = i + increment
    if i >= len(text):
      i = 0
    
    self.animation_status[line][0] = i
    

  # blink
  def blink(line, text):

    if (line == 1):
      self.lcd_byte(DisplayController.LCD_LINE_1, DisplayController.LCD_CMD)
      i = 2

    elif (line == 2):
      self.lcd_byte(DisplayController.LCD_LINE_2, DisplayController.LCD_CMD)
      i = 3
   
    if (self.counter[i] % 2 > 0):
      text = " " * 16;

    self.lcd_string(text)

    self.counter[i] = self.counter[i] + 1
    
  def tick(self):
    now = timestamp_ms()
    if (now - self.waiting_since >= self.wait_time):
      self.callback(self)
      self.waiting_since = now

  def lcd_init(self):
    # Initialise display
    self.lcd_byte(0x33,DisplayController.LCD_CMD)
    self.lcd_byte(0x32,DisplayController.LCD_CMD)
    self.lcd_byte(0x28,DisplayController.LCD_CMD)
    self.lcd_byte(0x0C,DisplayController.LCD_CMD)
    self.lcd_byte(0x06,DisplayController.LCD_CMD)
    self.lcd_byte(0x01,DisplayController.LCD_CMD)
   
  def lcd_string(self, message):
    # Send string to display
   
    message = message.ljust(DisplayController.LCD_WIDTH," ")  
   
    for i in range(DisplayController.LCD_WIDTH):
      self.lcd_byte(ord(message[i]),DisplayController.LCD_CHR)
   
  def lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
   
    GPIO.output(DisplayController.LCD_RS, mode) # RS
   
    # High bits
    GPIO.output(DisplayController.LCD_D4, False)
    GPIO.output(DisplayController.LCD_D5, False)
    GPIO.output(DisplayController.LCD_D6, False)
    GPIO.output(DisplayController.LCD_D7, False)
    if bits&0x10==0x10:
      GPIO.output(DisplayController.LCD_D4, True)
    if bits&0x20==0x20:
      GPIO.output(DisplayController.LCD_D5, True)
    if bits&0x40==0x40:
      GPIO.output(DisplayController.LCD_D6, True)
    if bits&0x80==0x80:
      GPIO.output(DisplayController.LCD_D7, True)
   
    # Toggle 'Enable' pin
    time.sleep(DisplayController.E_DELAY)
    GPIO.output(DisplayController.LCD_E, True)
    time.sleep(DisplayController.E_PULSE)
    GPIO.output(DisplayController.LCD_E, False)
    time.sleep(DisplayController.E_DELAY)      
   
    # Low bits
    GPIO.output(DisplayController.LCD_D4, False)
    GPIO.output(DisplayController.LCD_D5, False)
    GPIO.output(DisplayController.LCD_D6, False)
    GPIO.output(DisplayController.LCD_D7, False)
    if bits&0x01==0x01:
      GPIO.output(DisplayController.LCD_D4, True)
    if bits&0x02==0x02:
      GPIO.output(DisplayController.LCD_D5, True)
    if bits&0x04==0x04:
      GPIO.output(DisplayController.LCD_D6, True)
    if bits&0x08==0x08:
      GPIO.output(DisplayController.LCD_D7, True)
   
    # Toggle 'Enable' pin
    time.sleep(DisplayController.E_DELAY)
    GPIO.output(DisplayController.LCD_E, True)
    time.sleep(DisplayController.E_PULSE)
    GPIO.output(DisplayController.LCD_E, False)
    time.sleep(DisplayController.E_DELAY)   

  def lcd_cleanup(self):
    GPIO.cleanup()
