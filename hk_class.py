# coding=utf-8
from ctypes import *

#宏定义
SERIALNO_LEN = 48  # 序列号长度
NAME_LEN = 32  # 用户名长度py
VCA_MAX_POLYGON_POINT_NUM = 10 #检测区域最多支持10个点的多边形

NET_DVR_GET_REALTIME_THERMOMETRY = 3629 # 实时温度检测
NET_DVR_GET_MANUALTHERM_INFO = 6706 # 手动测温实时获取

class NET_DVR_DEVICEINFO_V30(Structure):
    _fields_ = [('sSerialNumber', c_ubyte * SERIALNO_LEN), ('byAlarmInPortNum', c_byte), ('byAlarmOutPortNum', c_byte), ('byDiskNum', c_byte),
                ('byDVRType', c_byte), ('byChanNum', c_byte), ('byStartChan', c_byte), ('byAudioChanNum', c_byte), ('byIPChanNum', c_byte), ('byRes1', c_ubyte * 24)]

class NET_VCA_POINT(Structure):
    _fields_ = [('fX', c_float), ('fY', c_float)]

class NET_VCA_POLYGON(Structure):
    _fields_ = [('dwPointNum', c_ulong), ('struPos',NET_VCA_POINT * 10)] 

class NET_DVR_THERMOMETRY_PRESETINFO_PARAM(Structure):
    _fields_ = [('byEnabled', c_byte), ('byRuleID', c_short), ('wDistance', c_short), ('fEmissivity', c_float), ('byDistanceUnit', c_byte), ('byRes', c_ubyte * 2), ('byReflectiveEnabled', c_byte),
                ('fReflectiveTemperature', c_float), ('szRuleName', c_ubyte * NAME_LEN), ('byRes1', c_ubyte * 63), ('byRuleCalibType', c_byte), ('struPoint', NET_VCA_POINT), ('struRegion', NET_VCA_POLYGON)]

class NET_DVR_THERMOMETRY_PRESETINFO(Structure):
    _fields_ = [('dwSize', c_ulong), ('wPresetNo', c_short), ('byRes', c_ubyte * 2),
                ('struPresetInfo', NET_DVR_THERMOMETRY_PRESETINFO_PARAM * 40)]

class NET_DVR_THERMOMETRY_COND(Structure):
    _fields_ = [('dwSize', c_ulong), ('dwChannel', c_ulong),
                ('wPresetNo', c_short), ('byRes', c_ubyte * 62)]

class BYTE_ARRAY(Structure):
    _fields_ = [('byValue', c_byte * 2097152)]

class NET_DVR_STD_CONFIG(Structure):
    _fields_ = [('lpCondBuffer', POINTER(NET_DVR_THERMOMETRY_COND)), ('dwCondSize', c_ulong), ('lpInBuffer', POINTER(NET_DVR_THERMOMETRY_PRESETINFO)), ('dwInSize', c_ulong), ('lpOutBuffer', POINTER(NET_DVR_THERMOMETRY_PRESETINFO)), ('dwOutSize', c_ulong),
                ('lpStatusBuffer', POINTER(BYTE_ARRAY)), ('dwStatusSize', c_ulong), ('lpXmlBuffer', c_void_p), ('dwXmlSize', c_ulong), ('byDataType', c_bool), ('byRes', c_ubyte * 23)]

class NET_VCA_RECT(Structure):
    _fields_ = [('fX', c_char),('fY', c_char),('fWidth', c_char),('fHeight', c_char)]

class NET_DVR_JPEGPICTURE_WITH_APPENDDATA(Structure):
    _fields_ = [('dwSize', c_int32), ('dwChannel', c_int32), ('dwJpegPicLen', c_int32), ('pJpegPicBuff', POINTER(BYTE_ARRAY)), ('dwJpegPicWidth', c_int32),
                ('dwJpegPicHeight', c_int32), ('dwP2PDataLen', c_int32), ('pP2PDataBuff', POINTER(BYTE_ARRAY)), ('byIsFreezedata', c_byte), ('byRes', c_byte * 255)]

# JPEG图像信息结构体。

# struct{
#   WORD     wPicSize;
#   WORD     wPicQuality;
# }NET_DVR_JPEGPARA,*LPNET_DVR_JPEGPARA;

class NET_DVR_JPEGPARA(Structure):
    _fields_ = [('wPicSize', c_ulong),('wPicQuality', c_ulong)]

#点坐标参数结构体。

class NET_VCA_POINT(Structure):
    _fields_ =[('fX',c_float),('fY',c_float)]

#点测温实时信息结构体。

class NET_DVR_POINT_THERM_CFG(Structure):
    _fields_ = [('fTemperature', c_float),('struPoint', NET_VCA_POINT),('byRes', c_byte * 120)]

#多边形结构体。
class NET_VCA_POLYGON(Structure):
    _fields_ = [('dwPointNum',c_uint32), ('struPos', NET_VCA_POINT * VCA_MAX_POLYGON_POINT_NUM)]

#框/线测温实时信息结构体。

class NET_DVR_LINEPOLYGON_THERM_CFG(Structure):
    _fields_ = [('fMaxTemperature', c_float),('fMinTemperature', c_float), ('fAverageTemperature', c_float), ('fTemperatureDiff', c_float),('struRegion', NET_VCA_POLYGON), ('byRes', c_ubyte * 32)]

#区域框参数结构体。

class NET_VCA_RECT(Structure):
    _fields_ = [('fX', c_float), ('fY', c_float), ('fWidth', c_float), ('fHeight', c_float)]

# 实时温度信息结构体。
class NET_DVR_THERMOMETRY_UPLOAD(Structure):
     _fields_ =[('dwSize', c_uint32),('dwRelativeTime', c_uint32),('dwAbsTime', c_uint32),('szRuleName', c_char * NAME_LEN),('byRuleID', c_ubyte),('byRuleCalibType', c_ubyte),
                ('wPresetNo', c_uint16),('struPointThermCfg', NET_DVR_POINT_THERM_CFG),('struLinePolygonThermCfg', NET_DVR_LINEPOLYGON_THERM_CFG),('byThermometryUnit', c_ubyte),
                ('byDataType', c_ubyte),('byRes1', c_ubyte),('bySpecialPointThermType', c_ubyte),('fCenterPointTemperature', c_float),('fHighestPointTemperature', c_float),
                ('fLowestPointTemperature', c_float),('struHighestPoint', NET_VCA_POINT),('struLowestPoint', NET_VCA_POINT),('byIsFreezedata', c_ubyte),('byFaceSnapThermometryEnabled', c_ubyte),
                ('byRes2[2]', c_ubyte),('dwChan', c_uint32),('struFaceRect', NET_VCA_RECT),('dwTimestamp', c_uint32),('byRes[68]', c_ubyte)]
# DWORD|c_uint32 BYTE|c_ubyte WORD|c_int16

#实时温度检测条件参数结构体。

class NET_DVR_REALTIME_THERMOMETRY_COND(Structure):
    _fields_ = [('dwSize', c_int32),('dwChan', c_int32), ('byRuleID', c_ubyte), ('byMode', c_ubyte),('wInterval', c_short), ('fTemperatureDiff', c_float), ('byRes', c_ubyte * 56)]
