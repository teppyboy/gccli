import subprocess
import platform

class ProxyError(Exception):
    """
    """

class SetSystemProxyError(ProxyError):
    """
    """

class NotSupportedPlatform(SetSystemProxyError):
    """
    """

class Proxy:
    def __init__(self):
        self._port = None
        self._ssl = None
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def _set_system_proxy_win(self):
        subprocess.run('netsh winhttp set proxy proxy-server="http=localhost:{port}"'.format(port=self._port).split())

    def set_system_proxy(self):
        match platform.system():
            case "Windows":
                self._set_system_proxy_win()
            case "Linux":
                raise NotSupportedPlatform("Linux is not supported, you must append http_proxy & https_proxy environment\
                    variable manually or use proxychains.")
            case "Darwin":
                pass