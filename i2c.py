# 远程控制-作为主控设备
#
# 该脚本将您的OpenMV Cam配置为使用RPC库远程控制另一个OpenMV Cam。
# 该脚本可由任何实现pyb模块的Micropython板运行，以远程控制OpenMV Cam。
#
# 这个脚本与 "popular_features_as_the_remote_device.py" 配对。

import json, rpc, struct

# 上面的RPC库安装在您的OpenMV Cam上，并提供多种类，以允许您的OpenMV Cam控制CAN，I2C，SPI，UART或WIFI。

##############################################################
# 选择你想要控制的OpenMV摄像头的接口。
##############################################################

# 取消注释以下行以设置您的OpenMV Cam以控制CAN。
#
# * message_id - 用于CAN信息在can总线（11位）上进行数据传输。
# * bit_rate - CAN 比特率。
# * sampling_point - Tseg1/Tseg2 ratio. 一般为 75%. (50.0, 62.5, 75.0, 87.5, etc.)
#
# 注意:主从设备的message id和比特率必须匹配。将主设备的高电平引脚连接到从设备的高电平引脚，
# 将主设备的低电平引脚连接到从设备的低电平引脚。CAN总线必须接120欧姆的终端电阻。
#
# interface = rpc.rpc_can_master(message_id=0x7FF, bit_rate=250000, sampling_point=75)

# 取消注释以下行以设置您的OpenMV Cam以控制I2C。
#
# * slave_addr - I2C地址。
# * rate - I2C总线时钟频率。
#
# 注意：主地址和从地址必须匹配。将主scl连接到从scl，将主sda连接到从sda。
# 您必须使用外部上拉电阻。最后，两个设备必须共地。
#
# interface = rpc.rpc_i2c_master(slave_addr=0x12, rate=100000)


# 取消注释以下行以设置您的OpenMV Cam以控制SPI。
#
# * cs_pin - 从片选引脚。
# * freq - SPI总线时钟频率。
# * clk_polarity - 空闲时钟电平(0或1)。
# * clk_phase — 在时钟的第一个(0)或第二个边沿(1)上采样数据。
#
# 注意：主机和从机设置必须匹配。将CS，SCLK，MOSI，MISO连接到CS，SCLK，MOSI，MISO。
# 最后，两个设备必须共地。
#
# interface = rpc.rpc_spi_master(cs_pin="P3", freq=10000000, clk_polarity=1, clk_phase=0)

# 取消注释以下行以设置您的OpenMV Cam以控制UART。
#
# * baudrate - 串行波特率。
#
# 注意：主和从波特率必须匹配。将主TX连接到从TX，将主TX连接到从TX。
# 最后，两个设备必须共地。
#
interface = rpc.rpc_uart_master(baudrate=115200)

##############################################################
# 回调处理程序
##############################################################

def exe_face_detection():
    result = interface.call("face_detection")
    if result is not None and len(result):
        print("Largest Face Detected [x=%d, y=%d, w=%d, h=%d]" % struct.unpack("<HHHH", result))

def exe_person_detection():
    result = interface.call("person_detection")
    if result is not None:
        print(bytes(result).decode())

def exe_qrcode_detection():
    result = interface.call("qrcode_detection")
    if result is not None and len(result):
        print(bytes(result).decode())

def exe_all_qrcode_detection():
    result = interface.call("all_qrcode_detection")
    if result is not None and len(result):
        print("QR Codes Detected:")
        for obj in json.loads(result):
            print(obj)

def exe_apriltag_detection():
    result = interface.call("apriltag_detection")
    if result is not None and len(result):
        print("Largest Tag Detected [cx=%d, cy=%d, id=%d, rot=%d]" % struct.unpack("<HHHH",result))

def exe_all_apriltag_detection():
    result = interface.call("all_apriltag_detection")
    if result is not None and len(result):
        print("Tags Detected:")
        for obj in json.loads(result):
            print(obj)

def exe_datamatrix_detection():
    result = interface.call("datamatrix_detection")
    if result is not None and len(result):
        print(bytes(result).decode())

def exe_all_datamatrix_detection():
    result = interface.call("all_datamatrix_detection")
    if result is not None and len(result):
        print("Data Matrices Detected:")
        for obj in json.loads(result):
            print(obj)

def exe_barcode_detection():
    result = interface.call("barcode_detection")
    if result is not None and len(result):
        print(bytes(result).decode())

def exe_all_barcode_detection():
    result = interface.call("all_barcode_detection")
    if result is not None and len(result):
        print("Bar Codes Detected:")
        for obj in json.loads(result):
            print(obj)

def exe_color_detection():
    thresholds = (30, 100, 15, 127, 15, 127) # 通用红色阈值
    # thresholds = (30, 100, -64, -8, -32, 32) # 通用绿色阈值
    # thresholds = (0, 30, 0, 64, -128, 0) # 通用蓝色阈值
    result = interface.call("color_detection", struct.pack("<bbbbbb", *thresholds))
    if result is not None and len(result):
        print("Largest Color Detected [cx=%d, cy=%d]" % struct.unpack("<HH", result))

number = 0
def exe_jpeg_snapshot():
    global number
    result = interface.call("jpeg_snapshot")
    if result is not None:
        name = "snapshot-%05d.jpg" % number
        print("Writing jpeg %s..." % name)
        with open(name, "wb") as snap:
            snap.write(result)
            number += 1

# 循环执行远程功能。请在下面选择并取消注释一项远程功能。
# 如果相机每次执行都需要更改相机模式，则一次执行多个操作可能会运行缓慢。

while(True):
    exe_face_detection() # 脸应该在2英尺以外。
    # exe_person_detection()
    # exe_qrcode_detection() # 将QRCode二维码放在2英尺远的地方。
    # exe_all_qrcode_detection() # 将QRCode二维码放在2英尺远的地方。
    # exe_apriltag_detection()
    # exe_all_apriltag_detection()
    # exe_datamatrix_detection() # 将Datamatrix矩形码放置在大约2英尺之外。
    # exe_all_datamatrix_detection() # 将Datamatrix矩形码放置在大约2英尺之外。
    # exe_barcode_detection() # 将条形码放在2英尺远的地方。
    # exe_all_barcode_detection() # 将条形码放在2英尺远的地方。
    # exe_color_detection()
    # exe_jpeg_snapshot()
