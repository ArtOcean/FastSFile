import cmd
import os
import socket
import threading
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """支持多线程的HTTP服务器"""
    daemon_threads = True

class FileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            # 展示使用说明页面
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = """
            <html><body>
            <h1>FastXfer文件传输服务</h1>
            <p>请使用 <code>/download/{令牌(uuid)}</code> 路径下载文件</p>
            <p>在电脑端执行 <code>send 文件路径</code> 获取下载链接</p>
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/favicon.ico':
            # 返回空响应避免404错误
            self.send_response(204)
            self.end_headers()
            
        elif self.path.startswith('/download/'):
            # 原有文件下载逻辑
            token = self.path.split('/')[-1]
            file_info = self.server.file_map.get(token)
            
            if not file_info or not os.path.exists(file_info['path']):
                self.send_error(404, "文件不存在或链接已过期")
                return
            
            try:
                with open(file_info['path'], 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/octet-stream')
                    self.send_header('Content-Disposition', 
                                   f'attachment; filename="{file_info["name"]}"')
                    fs = os.path.getsize(file_info['path'])
                    self.send_header('Content-Length', str(fs))
                    self.end_headers()
                    
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, f"无效路径:{self.path}")


class FileTransferApp(cmd.Cmd):
    prompt = "(FastSFile) "
    
    def __init__(self):
        super().__init__()
        self.server = None
        self.server_thread = None
        self.ip = self.get_local_ip()
    
    @staticmethod
    def get_local_ip():
        """获取本机局域网IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def do_start(self, arg):
        """启动服务器:start [端口] (默认8000)"""
        port = int(arg) if arg.isdigit() else 8000
        
        try:
            self.server = ThreadedHTTPServer(('', port), FileHandler)
            self.server.file_map = {}
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.start()
            print(f"[*] 服务已启动，访问地址:http://{self.ip}:{port}")
        except Exception as e:
            print(f"[!]:启动失败：{str(e)}")

    def do_send(self, arg):
        """发送文件:send <文件路径>"""
        if not self.server:
            print("[!]:请先启动服务器")
            return
        
        path = os.path.abspath(arg)
        if not os.path.exists(path):
            print(f"[!]:文件不存在：{arg}")
            return
        
        token = str(uuid.uuid4())
        self.server.file_map[token] = {
            'name': os.path.basename(path),
            'path': path
        }
        print(f"[*] 下载链接：http://{self.ip}:{self.server.server_address[1]}/download/{token}")
        print("[*] 请在手机浏览器打开此链接下载")

    def do_stop(self, arg):
        """停止服务器:stop"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
            self.server = None
            print("[*] 服务已停止")

    def do_exit(self, arg):
        """退出程序:exit"""
        if self.server:
            self.do_stop(None)
        print("[*] 再见！")
        return True

if __name__ == '__main__':
    print("""\
  _____   ____ _____     __        _      __ 
 |  _  | / ___|  ___|   /  \      / \    / /
 | | | |/ /   | |___   / __ \    / _ \  / /
 | |_| |\ \___| |___  / /  \ \  / / \ \/ /
 |_____| \____|_____|/_/    \_\/_/   \_\/
                                                    """)
    print("输入 help 查看可用命令\n")
    FileTransferApp().cmdloop()