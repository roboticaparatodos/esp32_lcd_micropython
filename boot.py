import time

from machine import SPI
from libraries.ST7735 import TFT
from tools import show_spi_info, create_display, demo_start, show_image


### User Defined Pins ####
CS = 18
RES= 17   # (TX)
DC = 16   # (RX)

### Show assigned SCK (SCL) and MOSI (SDA) pins ###
show_spi_info()

### Initialize LCD Screen ###
lcd = create_display(DC, RES, CS)

### Begin script ###
lcd.rotation(2)                         # Rotate 180 degrees screen display
demo_start(lcd)                         # Show some text information
time.sleep_ms(5000)                     # Wait 5 seconds
lcd.fill(TFT.BLACK)                     # Clear screen (all in black color)
show_image(lcd, 'images/pinball.bmp')   # Show pinball image