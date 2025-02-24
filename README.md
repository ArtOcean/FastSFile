# FastSFile - 快速文件传输工具

**FastSFile** 是一个基于 Python 的命令行文件传输工具，专为在局域网内快速、简单地传输文件而设计。通过启动本地 HTTP 服务器，用户可以生成唯一的下载链接，方便在手机或其他设备上轻松下载文件。

---

## ✨ 功能特性

- **局域网传输**：自动获取本机 IP 地址，支持局域网内设备访问。
- **多线程支持**：高效处理多个并发下载请求，提升传输速度。
- **简单易用**：通过直观的命令行界面操作，无需复杂配置。
- **大文件支持**：采用分块传输技术，避免内存溢出，轻松应对大文件。
- **临时链接**：每次生成唯一的下载链接，确保传输过程安全可靠。

---

## 🚀 安装与使用

### 前提条件
确保你的系统已安装 **Python 3.x** 或更高版本。

### 安装步骤
1. 克隆本仓库到本地：
   ```bash
   git clone https://github.com/ArtOcean/FastSFile.git
   cd FastSFile
2. 启动服务器：
   ```bash
   python FastSFile.py
   (FastSFile) start 8000
3. 发送文件：
   ```bash
   (FastSFile) send /path/to/your/file.txt
4. 获取下载链接：
   ```bash
   [*] 下载链接：http://192.168.1.100:8000/download/55a6443e-9d32-11ee-8c90-0242ac120002
5. 停止服务器：
   ```bash
   (FastSFile) stop
6. 退出程序：
   (FastSFile) exit
## 依赖

- **Python 3.x 或以上**
- **标准库**：`cmd`, `os`, `socket`, `threading`, `uuid`, `http.server`, `socketserver`
## FastSFile - 让文件传输更快、更简单！
## 感谢你的使用与支持！如果喜欢这个项目，别忘了给我一个 ⭐ Star！
