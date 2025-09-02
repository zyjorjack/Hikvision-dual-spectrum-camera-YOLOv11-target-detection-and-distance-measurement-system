import hksdk.hk_dll
import hksdk.hk_class
from ctypes import *
import struct
# from numba import njit

# 设备信息
m_strDeviceInfo = None

SERIALNO_LEN = 48  # 序列号长度
NAME_LEN = 32  # 用户名长度py
point_bytes = (c_byte * 4)()

#用户登录信息

m_strDeviceInfo = None

#测温信息

m_strJpegWithAppenData = None

# 初始化


def init():
    return hksdk.hk_dll.NET_DVR_Init()

# 登录


def login(ip, port, username, password):
    # 注册
    m_strDeviceInfo = hksdk.hk_class.NET_DVR_DEVICEINFO_V30()
    m_strDeviceInfo.sSerialNumber = (c_ubyte * SERIALNO_LEN)()
    m_strDeviceInfo.byRes1 = (c_ubyte * 24)()

    user_id = hksdk.hk_dll.NET_DVR_Login_V30(bytes(ip), port, bytes(username), bytes(password), byref(m_strDeviceInfo))

    # 打开SDK写日志的功能
    hksdk.hk_dll.NET_DVR_SetLogToFile(3, b'./sdklog', False)

    return user_id

# 退出登录


def logout(user_id):
    hksdk.hk_dll.NET_DVR_Logout_V30(user_id)

# 释放sdk


def cleanup():
    hksdk.hk_dll.NET_DVR_Cleanup()

'''
    全屏抓拍图片获取最高温度和最低温度
    user_id 登录成功后返回的用户id
'''

def get_max_min(user_id):

    ret, m_strJpegWithAppenData = get_temperature0(user_id)
    max_temperature = -50
    min_temperature = 120

    byValue = m_strJpegWithAppenData.pP2PDataBuff.contents.byValue

    if ret:
        for x in range(m_strJpegWithAppenData.dwJpegPicWidth):
            for y in range(m_strJpegWithAppenData.dwJpegPicHeight):

                temperature = struct.unpack('<f', struct.pack('4b', *get_bytes(byValue , (m_strJpegWithAppenData.dwJpegPicWidth * y + x) * 4, 4)))[0]

                max_temperature = temperature if temperature > max_temperature else max_temperature
                min_temperature = temperature if temperature < min_temperature else min_temperature

        return True, max_temperature, min_temperature

    return False, max_temperature, min_temperature

'''
    获取给定点列表最高温度，
    points 矩形区域内的起始点坐标 例如[(0,0), (10,10)]
    source_width 热成像图像的宽度
    source_height 热成像图像的高度
    user_id 登录成功后返回的用户id
'''

def get_temperature_max(points, source_width, source_height, user_id):

    ret, m_strJpegWithAppenData = get_temperature0(user_id)

    if(len(points) < 2):
        return False, -2

    if ret:
        x1, y1 = point2point(points[0][0], points[0][1], source_width, source_height,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)

        x2, y2 = point2point(points[1][0], points[1][1], source_width, source_height,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)

        if x1 > x2 or y1 > y2:
            return False, -3

        byValue = m_strJpegWithAppenData.pP2PDataBuff.contents.byValue

        max_temperature = -50.0
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                # 160 * 120
                temperature = struct.unpack('<f', struct.pack('4b', *get_bytes(byValue,  (m_strJpegWithAppenData.dwJpegPicWidth * y + x) * 4, 4)))[0]
                max_temperature = temperature if temperature > max_temperature else max_temperature

        return True, max_temperature

    return False, -1

# 获取某点的温度


def get_temperature(x, y, source_width, source_height, user_id, channel_no):

    ret, m_strJpegWithAppenData = get_temperature0(user_id, channel_no)

    if ret:
        x, y = point2point(x, y, source_width, source_height, m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)
        byValue = m_strJpegWithAppenData.pP2PDataBuff.contents.byValue

        return True, struct.unpack('<f', struct.pack('4b', *get_bytes(byValue, (m_strJpegWithAppenData.dwJpegPicWidth * y + x) * 4, 4)))[0]

    return False, 0.0

# 截取指定下标的和长度的返回数据


def get_bytes(src_bytes, offset, length):
    global point_bytes

    for i in range(length):
        point_bytes[i] = src_bytes[offset + i]

    return point_bytes


# 获取温度

def get_temperature0(user_id, channel_no = 2):
    bRet = False
    global m_strJpegWithAppenData

    if m_strJpegWithAppenData is None:
        m_strJpegWithAppenData = hksdk.hk_class.NET_DVR_JPEGPICTURE_WITH_APPENDDATA()
        m_strJpegWithAppenData.byRes = (c_byte * 255)()
        m_strJpegWithAppenData.dwChannel = 1
        m_strJpegWithAppenData.pJpegPicBuff = pointer(
            hksdk.hk_class.BYTE_ARRAY((c_byte * 2097152)()))
        m_strJpegWithAppenData.pP2PDataBuff = pointer(
            hksdk.hk_class.BYTE_ARRAY((c_byte * 2097152)()))
        m_strJpegWithAppenData.dwSize = sizeof(m_strJpegWithAppenData)

    bRet = hksdk.hk_dll.NET_DVR_CaptureJPEGPicture_WithAppendData(user_id, channel_no, byref(m_strJpegWithAppenData))

    if bRet:
        # 测温数据
        print(m_strJpegWithAppenData.dwP2PDataLen)
        if m_strJpegWithAppenData.dwP2PDataLen > 0:
            return True, m_strJpegWithAppenData

    return False, None

# 抓拍图片和热成像图像坐标转换
# @njit

def point2point(x, y, source_width, source_height, target_width, target_height):
    x = x * target_width / source_width
    y = y * target_height / source_height

    x = x if x <= target_width else target_width
    x = 0 if x < 0 else x

    y = y if y <= target_height else target_height
    y = 0 if y < 0 else y

    return int(x), int(y)

# 热成像坐标和可见光图像坐标转换
# @njit
#(注意下面ratio、width、height、参数为测试的参数，具体修改为摄像头实际数值)

def point_point_2(x, y, source_width, source_height):
    #热成像图像和抓拍图片比例
    ratio = 3.0
    #热成像图像和可见光图像的位置差值单位像素
    width = 100
    height = 50

    x = x * ratio - width
    y = y * ratio - height

    x = x if x <= source_width else source_width
    x = 0 if x < 0 else x

    y = y if y <= source_height else source_height
    y = 0 if y < 0 else y

    return int(x), int(y)

#抓拍图片
# user_id 登录用户id
# lChannel 渠道号
# dir 文件保存路径
def captureJPEGPicture(user_id, lChannel, dir):
    jpegpara= hksdk.hk_class.NET_DVR_JPEGPARA()
    jpegpara.wPicSize = 0xff
    jpegpara.wPicQuality = 2

    p = c_char_p()
    s = byref(c_ulong())

    # return hk_dll.NET_DVR_CaptureJPEGPicture(user_id, lChannel, byref(jpegpara), p, 2048, s)
    return hksdk.hk_dll.NET_DVR_CaptureJPEGPicture(user_id, lChannel, byref(jpegpara), dir)

def get_last_error():
    return hksdk.hk_dll.NET_DVR_GetLastError()