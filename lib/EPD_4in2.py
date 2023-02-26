from machine import Pin, SPI
import framebuf
import gc
import utime

from epd import EPD

EPD_4IN2_lut_vcom0 = [
    0x00, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x00, 0x0F, 0x0F, 0x00, 0x00, 0x01,
    0x00, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00,
]
EPD_4IN2_lut_ww = [
    0x50, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
    0xA0, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_4IN2_lut_bw = [
    0x50, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
    0xA0, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_4IN2_lut_wb = [
    0xA0, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
    0x50, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_4IN2_lut_bb = [
    0x20, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
    0x10, 0x08, 0x08, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]

# ******************************partial screen update LUT********************************* #
EPD_4IN2_Partial_lut_vcom1 =[
    0x00,0x19,0x01,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,
]

EPD_4IN2_Partial_lut_ww1 =[
    0x00,0x19,0x01,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]

EPD_4IN2_Partial_lut_bw1 =[
    0x80,0x19,0x01,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]

EPD_4IN2_Partial_lut_wb1 =[
    0x40,0x19,0x01,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]

EPD_4IN2_Partial_lut_bb1 =[
    0x00,0x19,0x01,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]

# ******************************gray********************************* #
# 0~3 gray
EPD_4IN2_4Gray_lut_vcom=[
    0x00,0x0A,0x00,0x00,0x00,0x01,
    0x60,0x14,0x14,0x00,0x00,0x01,
    0x00,0x14,0x00,0x00,0x00,0x01,
    0x00,0x13,0x0A,0x01,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00
]
# R21
EPD_4IN2_4Gray_lut_ww =[
    0x40,0x0A,0x00,0x00,0x00,0x01,
    0x90,0x14,0x14,0x00,0x00,0x01,
    0x10,0x14,0x0A,0x00,0x00,0x01,
    0xA0,0x13,0x01,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]
# R22H r
EPD_4IN2_4Gray_lut_bw =[
    0x40,0x0A,0x00,0x00,0x00,0x01,
    0x90,0x14,0x14,0x00,0x00,0x01,
    0x00,0x14,0x0A,0x00,0x00,0x01,
    0x99,0x0C,0x01,0x03,0x04,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]
# R23H w
EPD_4IN2_4Gray_lut_wb =[
    0x40,0x0A,0x00,0x00,0x00,0x01,
    0x90,0x14,0x14,0x00,0x00,0x01,
    0x00,0x14,0x0A,0x00,0x00,0x01,
    0x99,0x0B,0x04,0x04,0x01,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]
#  R24H b
EPD_4IN2_4Gray_lut_bb =[
    0x80,0x0A,0x00,0x00,0x00,0x01,
    0x90,0x14,0x14,0x00,0x00,0x01,
    0x20,0x14,0x0A,0x00,0x00,0x01,
    0x50,0x13,0x01,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]

class EPD_4in2(EPD):

    def __init__(self):

        super().__init__(400, 300)
        self.expected_block_count = 2

        self.lut_vcom0 = EPD_4IN2_lut_vcom0
        self.lut_ww = EPD_4IN2_lut_ww
        self.lut_bw = EPD_4IN2_lut_bw
        self.lut_wb = EPD_4IN2_lut_wb
        self.lut_bb = EPD_4IN2_lut_bb

        self.lut_Partial_vcom = EPD_4IN2_Partial_lut_vcom1
        self.lut_Partial_ww = EPD_4IN2_Partial_lut_ww1
        self.lut_Partial_bw = EPD_4IN2_Partial_lut_bw1
        self.lut_Partial_wb = EPD_4IN2_Partial_lut_wb1
        self.lut_Partial_bb = EPD_4IN2_Partial_lut_bb1

        self.lut_4Gray_vcom = EPD_4IN2_4Gray_lut_vcom
        self.lut_4Gray_ww = EPD_4IN2_4Gray_lut_ww
        self.lut_4Gray_bw = EPD_4IN2_4Gray_lut_bw
        self.lut_4Gray_wb = EPD_4IN2_4Gray_lut_wb
        self.lut_4Gray_bb = EPD_4IN2_4Gray_lut_bb


        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55
        # self.buffer_1Gray_DATA  = [0x00] * (self.height * self.width // 8)

        # self.buffer_1Gray = bytearray(self.height * self.width // 8)
        # self.buffer_4Gray = bytearray(self.height * self.width // 4)
        # self.image1Gray = framebuf.FrameBuffer(self.buffer_1Gray, self.width, self.height, framebuf.MONO_HLSB)
        # self.image4Gray = framebuf.FrameBuffer(self.buffer_4Gray, self.width, self.height, framebuf.GS2_HMSB)

    def ReadBusy(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 0):      #  LOW: idle, HIGH: busy
            self.send_command(0x71)
            self.delay_ms(100)
        print("e-Paper busy release")

    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.delay_ms(100)
        self.ReadBusy()

    # Hardware reset (little bit more complex than usual)
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)

    def EPD_4IN2_4Gray_lut(self):
        self.send_command(0x20)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_vcom[count])

        self.send_command(0x21)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_ww[count])

        self.send_command(0x22)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_bw[count])

        self.send_command(0x23)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_wb[count])

        self.send_command(0x24)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_bb[count])

        self.send_command(0x25)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_ww[count])

    def init(self, *args):
        # 4 gray init
        print('4 gray init...')
        self.send_command(0x01)  # POWER SETTING
        self.send_data (0x03)
        self.send_data (0x00)  # VGH=20V,VGL=-20V
        self.send_data (0x2b)  # VDH=15V
        self.send_data (0x2b)  # VDL=-15V
        self.send_data (0x13)

        print('booster')
        self.send_command(0x06)  # booster soft start
        self.send_data (0x17)  # A
        self.send_data (0x17)  # B
        self.send_data (0x17)  # C

        print('send_command 0x04')
        self.send_command(0x04)
        self.ReadBusy()

        print('Panel setting')
        self.send_command(0x00)  # panel setting
        self.send_data(0x3f)  # KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        print('PLL setting')
        self.send_command(0x30)  # PLL setting
        self.send_data (0x3c)  # 100hz

        print('Resolution setting')
        self.send_command(0x61)  # resolution setting
        self.send_data (0x01)  # 400
        self.send_data (0x90)
        self.send_data (0x01)  # 300
        self.send_data (0x2c)

        print('vcom_DC setting')
        self.send_command(0x82)  # vcom_DC setting
        self.send_data (0x12)

        print('vcom and data interval setting')
        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x97)
        print('init() finished')

    def clear(self):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1

        self.send_command(0x10)
        blanks = bytearray([0xff for e in range(0, wide)])
        for j in range(0, high):
            self.send_data_array(blanks)

        self.send_command(0x13)
        for j in range(0, high):
            self.send_data_array(blanks)

        self.send_command(0x12)
        self.delay_ms(10)
        self.TurnOnDisplay()

    # Here for reference, not actually used
    def display(self, data):
       self.send_command(0x10)
       for i in range(0, self.width * self.height // 8):
            temp3=0
            for j in range(0, 2):
                temp1 = data[i * 2 + j]
                for k in range(0, 2):
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):
                        temp3 |= 0x01   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x01
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x00
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2

                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1

                    temp1 >>= 2

            self.send_data(temp3)
       # new  data
       self.send_command(0x13)
       for i in range(0, self.width * self.height // 8):
            temp3=0
            for j in range(0, 2):
                temp1 = data[i * 2 + j]
                for k in range(0, 2):
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):
                        temp3 |= 0x01   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x01
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x00
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2

                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1

                    temp1 >>= 2
            self.send_data(temp3)
       self.EPD_4IN2_4Gray_lut()
       self.TurnOnDisplay()

    def displayMessage(self, *args):
        self.init()
        framebuf.FrameBuffer(self.buffer_4Gray, self.width, self.height, framebuf.GS2_HLSB)
        # Create a small framebuffer to display several lines of text.
        # This is a MONO_HLSB buffer (1 bit per pixel) for displaying white/black image (no gray1/gray2).

        textBufferHeight = 12 * (1 + len(args))
        textBufferWidth = self.width # Buffer extends entire width
        textBufferByteArray = bytearray(textBufferHeight * textBufferWidth // 8)
        image = framebuf.FrameBuffer(textBufferByteArray, textBufferWidth, textBufferHeight, framebuf.MONO_HLSB)
        image.fill(0xff)
        for h in range(0, len(args)):
            image.text(str(args[h]), 5, 12 * (1 + h), 0x00)

        blanks = bytearray([0xff for e in range(0, self.width // 8)])

        self.send_command(0x10)
        for j in range(0, textBufferHeight):
            self.send_data_array(textBufferByteArray[j * self.width // 8: (j + 1) * self.width // 8])
        for j in range(textBufferHeight, self.height):
            self.send_data_array(blanks)

        # You send the same image but with gray1/gray2 flipped (no pixels are gray)
        self.send_command(0x13)
        for j in range(0, textBufferHeight):
            self.send_data_array(textBufferByteArray[j * self.width // 8: (j + 1) * self.width // 8])
        for j in range(textBufferHeight, self.height):
            self.send_data_array(blanks)
        image = None
        textBufferByteArray = None
        gc.collect()
        self.EPD_4IN2_4Gray_lut()
        self.TurnOnDisplay()

    def sleep(self):
#         self.send_command(0X02)  # power off
#         self.ReadBusy()
        self.send_command(0X07)  # deep sleep
        self.send_data(0xA5)

    def process_data_block(self, data, block_number, send_response):
        if block_number == 0:
            self.init()
            self.send_command(0x10)
            self.send_data_array(data)
            send_response(200, 'OK')
            self.data_block_count = 1
        elif block_number == 1:
            if (block_number != self.data_block_count):
                send_response(409, 'Conflict - expected block number ' + str(self.data_block_count))
                self.data_block_count = 0
                return

            self.send_command(0x13)
            self.send_data_array(data)
            send_response(200, 'OK')
            self.EPD_4IN2_4Gray_lut()
            self.TurnOnDisplay()

            self.data_block_count = 0
            self.delay_ms(2000)
            self.sleep()