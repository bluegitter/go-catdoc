## Go-catdoc, get text and metadata from .doc files.
[![GoDoc](https://godoc.org/github.com/semvis123/go-catdoc?status.svg)](https://godoc.org/github.com/semvis123/go-catdoc)
[![Tests](https://github.com/semvis123/go-catdoc/actions/workflows/go.yml/badge.svg)](https://github.com/semvis123/go-catdoc/actions/workflows/go.yml)

Uses Wazero to run catdoc as webassembly in Go.
The catdoc source is slightly modified to support reading metadata in `.doc`.  
The `msdoc.hexpat` file is a pattern file for imhex that can parse the `summaryinformation` ole object inside the `.doc` file.

To compile the webassembly binary, go to ./catdoc/src/ and run `make catdoc-wasm`.  
To run the tests, do `go test ./...`

Usage:
```
f, err := os.Open("test.doc")
text, err := gocatdoc.GetTextFromFile(f)
```
### 编译go-catdoc可执行程序
```bash
Windows
GOOS=windows GOARCH=amd64 go build -o libcatdoc.dylib -buildmode=c-shared .
Linux
GOOS=linux GOARCH=amd64 go build -o libcatdoc.so -buildmode=c-shared .
macOS
GOOS=darwin GOARCH=amd64 go build -o libcatdoc.dylib -buildmode=c-shared .
```

### 编译 Windows `.dll`：

```bash
CGO_ENABLED=1 GOOS=windows GOARCH=amd64 CC=x86_64-w64-mingw32-gcc \
go build -o catdoc.dll -buildmode=c-shared .
```

------

### 编译 Linux `.so`（交叉编译，macOS 上）：

```bash
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC=x86_64-linux-gnu-gcc \
go build -o libcatdoc.so -buildmode=c-shared .
```

如果你没有 `x86_64-linux-gnu-gcc`，可用：

```bash
CC=x86_64-unknown-linux-gnu-gcc
```

（需安装：`brew install messense/macos-cross-toolchains/x86_64-unknown-linux-gnu`）

------

### 编译 macOS `.dylib`（本机原生）：

```bash
CGO_ENABLED=1 GOOS=darwin GOARCH=amd64 go build -o libcatdoc.dylib -buildmode=c-shared .
```

------

## 输出文件说明

| 文件名                                            | 说明                                |
| ------------------------------------------------- | ----------------------------------- |
| `catdoc.dll` / `libcatdoc.so` / `libcatdoc.dylib` | 可被 Python、C、Java 等调用的动态库 |
| `catdoc.h`                                        | 自动生成的 C 头文件（函数声明）     |



## Python 调用示例（跨平台）：

```python
import ctypes
import platform
import os

system = platform.system()

if system == "Windows":
    libname = "catdoc.dll"
elif system == "Linux":
    libname = "libcatdoc.so"
elif system == "Darwin":
    libname = "libcatdoc.dylib"
else:
    raise RuntimeError("不支持的系统")

lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), libname))
lib.GetTextFromPath.argtypes = [ctypes.c_char_p]
lib.GetTextFromPath.restype = ctypes.c_char_p

print(lib.GetTextFromPath(b"test.doc").decode())
```