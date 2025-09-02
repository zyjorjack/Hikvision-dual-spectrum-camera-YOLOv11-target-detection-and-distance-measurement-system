# coding=utf-8
from ctypes import c_int32, c_char_p, c_void_p, c_float, c_size_t, c_ubyte, c_long, cdll, POINTER, CDLL, c_bool, c_long, c_short
from hksdk.hk_class import *
import sys

# 回调函数类型定义
hCNetSDK = None;

if 'linux' == sys.platform:
    fun_ctype = CFUNCTYPE
    hCNetSDK = cdll.LoadLibrary('./lib/linux/libhcnetsdk.so')
else:
    hCNetSDK = CDLL('./lib/win/HCNetSDK.dll')
    fun_ctype = WINFUNCTYPE
    

SERIALNO_LEN = 48  # 序列号长度
NAME_LEN = 32  # 用户名长度

# //boolean NET_DVR_Init();
NET_DVR_Init = hCNetSDK.NET_DVR_Init
NET_DVR_Init.restype = c_bool
NET_DVR_Init.argtypes = ()

# boolean NET_DVR_Cleanup();
NET_DVR_Cleanup = hCNetSDK.NET_DVR_Cleanup
NET_DVR_Cleanup.restype = c_bool
NET_DVR_Cleanup.argtypes = ()

# NativeLong NET_DVR_Login_V30(String sDVRIP, short wDVRPort, String sUserName, String sPassword, NET_DVR_DEVICEINFO_V30 lpDeviceInfo);
NET_DVR_Login_V30 = hCNetSDK.NET_DVR_Login_V30
NET_DVR_Login_V30.restype = c_long
NET_DVR_Login_V30.argtypes = (c_char_p, c_short, c_char_p, c_char_p, POINTER(NET_DVR_DEVICEINFO_V30))

# boolean NET_DVR_Logout_V30(NativeLong lUserID);
NET_DVR_Logout_V30 = hCNetSDK.NET_DVR_Logout_V30
NET_DVR_Logout_V30.restype = c_bool
NET_DVR_Logout_V30.argtypes = (c_long,)

# boolean NET_DVR_SetSTDConfig(NativeLong lUserID, int dwCommand, NET_DVR_STD_CONFIG lpInConfigParam);
NET_DVR_SetSTDConfig = hCNetSDK.NET_DVR_SetSTDConfig
NET_DVR_SetSTDConfig.restype = c_bool
NET_DVR_SetSTDConfig.argtypes = (c_long, c_int32, NET_DVR_STD_CONFIG)

# boolean NET_DVR_GetSTDConfig(NativeLong lUserID, int dwCommand, NET_DVR_STD_CONFIG lpOutConfigParam);
NET_DVR_GetSTDConfig = hCNetSDK.NET_DVR_GetSTDConfig
NET_DVR_GetSTDConfig.restype = c_bool
NET_DVR_GetSTDConfig.argtypes = (c_long, c_int32, NET_DVR_STD_CONFIG)

# boolean NET_DVR_CaptureJPEGPicture_WithAppendData(NativeLong lUserID, int lChannel, NET_DVR_JPEGPICTURE_WITH_APPENDDATA lpJpegWithAppend);
NET_DVR_CaptureJPEGPicture_WithAppendData = hCNetSDK.NET_DVR_CaptureJPEGPicture_WithAppendData
NET_DVR_CaptureJPEGPicture_WithAppendData.restype = c_bool
NET_DVR_CaptureJPEGPicture_WithAppendData.argtypes = (c_long, c_int32, POINTER(NET_DVR_JPEGPICTURE_WITH_APPENDDATA))

# int NET_DVR_GetLastError();
NET_DVR_GetLastError = hCNetSDK.NET_DVR_GetLastError
NET_DVR_GetLastError.restype = c_int32
NET_DVR_GetLastError.argtypes = ()

# 启用日志文件写入接口
# boolean NET_DVR_SetLogToFile(int bLogEnable, String strLogDir, boolean bAutoDel);
NET_DVR_SetLogToFile = hCNetSDK.NET_DVR_SetLogToFile
NET_DVR_SetLogToFile.restype = c_bool
NET_DVR_SetLogToFile.argtypes = (c_int32, c_char_p, c_bool)


# 单帧数据捕获并保存成JPEG存放在指定的内存空间中。

# BOOL NET_DVR_CaptureJPEGPicture_NEW(
#   LONG                 lUserID,
#   LONG                 lChannel,
#   LPNET_DVR_JPEGPARA   lpJpegPara,
#   char                 *sJpegPicBuffer,
#   DWORD                dwPicSize,
#   LPDWORD              lpSizeReturned
# );
NET_DVR_CaptureJPEGPicture_new = hCNetSDK.NET_DVR_CaptureJPEGPicture_NEW
NET_DVR_CaptureJPEGPicture_new.restype = c_bool
NET_DVR_CaptureJPEGPicture_new.argtypes = (c_long, c_long, POINTER(NET_DVR_JPEGPARA), c_char_p, c_ulong, POINTER(c_ulong))

# BOOL NET_DVR_CaptureJPEGPicture_NEW(
#   LONG                 lUserID,
#   LONG                 lChannel,
#   LPNET_DVR_JPEGPARA   lpJpegPara,
#   char                 *sJpegPicBuffer,
#   DWORD                dwPicSize,
#   LPDWORD              lpSizeReturned
# );
NET_DVR_CaptureJPEGPicture = hCNetSDK.NET_DVR_CaptureJPEGPicture
NET_DVR_CaptureJPEGPicture.restype = c_bool
NET_DVR_CaptureJPEGPicture.argtypes = (c_long, c_long, POINTER(NET_DVR_JPEGPARA), c_char_p)


# 回调函数
# LONG->c_uint32 char*->c_void_p DWORD->c_ulong Object*->POINTER(Object)
#(DWORD dwType, void* lpBuffer, DWORD dwBufLen, void* pUserData)
GetThermInfoCallback = fun_ctype(None, c_ulong, c_void_p, c_ulong, c_void_p)