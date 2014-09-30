from lib.gpio_common import GPIO_Common
from lib.display import DisplayController
from lib.settings import tick_delay, display_delay
from time import sleep

#
# YOU MUST Initialize GPIO in BCM mode
#
GPIO_Common.init()

#
# YOU CAN define a function to be called by the controller every time it wants to refresh the display
#
def display_routine(display_controller):
    display_controller.scroll(DisplayController.LCD_LINE_1, "This is not a test", 1)
    display_controller.scroll(DisplayController.LCD_LINE_2, "This is reality", 2)

#
# YOU MUST Initialize a DisplayController object.
# This one is initialized to run routine every n ms
#
display_controller = DisplayController(display_routine, display_delay)


# YOU MUST call the tick method in the program's main loop
while True:
    display_controller.tick()
    sleep(tick_delay)
    
