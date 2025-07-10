import ctypes
import sys
import platform
import os

# 检测操作系统
system = platform.system()

if system == "Windows":
    libname = "catdoc.dll"
elif system == "Darwin":  # macOS
    libname = "libcatdoc.dylib"
elif system == "Linux":
    libname = "libcatdoc.so"
else:
    raise RuntimeError(f"不支持的操作系统: {system}")

# 加载共享库（当前目录）
libpath = os.path.join(os.path.dirname(__file__), libname)
lib = ctypes.CDLL(libpath)

# 设置参数和返回类型
lib.GetTextFromPath.argtypes = [ctypes.c_char_p]
lib.GetTextFromPath.restype = ctypes.c_char_p

# 调用函数
file_path = b"test.doc"  # 用 b'' 传入字节串
result = lib.GetTextFromPath(file_path)

print("结果:", result.decode("utf-8"))
