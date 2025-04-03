import machine

from machine import SPI
from libraries.ST7735 import TFT, TFTColor
from libraries.sysfont import sysfont

### Show SCK and MOSI pin assignation ###
def show_spi_info(spi_port: int = 1):
    pinout = machine.SPI(spi_port)
    print(pinout)

### Init screen ###
def create_display(DC: int, RES: int, CS: int) -> TFT:
    spi = SPI(1, baudrate=20000000, polarity=0, phase=0, miso=None)
    lcd = TFT(spi, DC, RES, CS)
    lcd.initr()
    lcd.rgb(True)
    lcd.fill(TFT.BLACK)

    return lcd

### Show some text ###
def demo_start(lcd: TFT):
    lcd.fill(TFT.BLACK)
    v = 30
    lcd.text((10, v), "Hola a todos", TFT.RED, sysfont, 1.5, nowrap=True)
    v += sysfont["Height"]*2
    lcd.text((10, v), "Soy un Pinball", TFT.YELLOW, sysfont, 1.2, nowrap=True)
    v += sysfont["Height"]*2
    lcd.text((10, v), "Robotica para Todos", TFT.WHITE, sysfont, 1.0, nowrap=True)

### Render a bitmap image in screen ###
def show_image(lcd: TFT, file: str):
    f = open(file, 'rb')
    if f.read(2) == b'BM':  # header
        dummy = f.read(8) # file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1: # planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0: # compress method == uncompressed
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                w, h = width, height
                if w > 128: w = 128
                if h > 160: h = 160
                lcd._setwindowloc((0,0),(w - 1,h - 1))
                for row in range(h):
                    if flip:
                        pos = offset + (height - 1 - row) * rowsize
                    else:
                        pos = offset + row * rowsize
                    if f.tell() != pos:
                        dummy = f.seek(pos)
                    for col in range(w):
                        bgr = f.read(3)
                        lcd._pushcolor(TFTColor(bgr[2],bgr[1],bgr[0]))
