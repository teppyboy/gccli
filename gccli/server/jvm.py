from datetime import datetime
from pathlib import Path
import platform
import shutil
import subprocess

class JavaError(Exception):
    """Base class for Java exceptions"""

class NoJavaError(JavaError):
    """No usable Java found on your system"""

class JavaExecuteError(JavaError):
    """Execution of Java failed
    
    Attributes:
        message -- explanation of the error
        errors -- errors from Java stderr
        java -- the java binary used
    """
    def __init__(self, message, errors, java):            
        super().__init__(message)
        self.errors = errors
        self.java = java

class JavaInfo:
    def __init__(self, provider: str, version: str, build_date: str):
        self._provider = provider
        self._version = version
        self._build_date = datetime.strptime(build_date, "%Y-%m-%d")

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def version(self) -> str:
        return self._version

    @property
    def build_date(self) -> datetime:
        return self._build_date

    @staticmethod
    def from_output(output: str):
        lines = output.splitlines()
        first_line = lines[0].split(" ")
        provider, version, build_date = first_line[0], first_line[1], first_line[2]
        return JavaInfo(provider, version, build_date)

class JVM:
    """
    Java Version Manager (not Java VM)
    """
    def __init__(self) -> None:
        self._java = None

    @property
    def java(self):
        """
        Get the Java binary used
        """
        if not self._java:
            self._java = self.get_java()
        return self._java

    @java.setter
    def java(self, java: str):
        """
        Set the Java binary to use
        """
        # Check if we can parse java --version output.
        self.java_info(java_binary=java)
        self._java = java

    def _get_javas_linux(self) -> list[str]:
        # Arch Linux
        javas = []
        jvm_path = Path("/usr/lib/jvm/")
        if jvm_path.exists():
            for java in jvm_path.iterdir():
                if java.name in ["default", "default-runtime"]:
                    continue
                javas.append(str(java.absolute()))
        return javas

    def get_javas(self) -> list[str]:
        """
        Get all installed Java versions
        """
        javas = []
        if shutil.which("java"):
            javas.append(shutil.which("java"))

        match platform.system():
            case "Linux":
                javas += self._get_javas_linux()
        # I hope Windows support will come soon.
        return javas

    def get_java(self) -> str:
        """
        Get the first installed Java version
        """
        javas = self.get_javas()
        if not javas:
            raise NoJavaError("No Java was found on your system")
        return javas[0]

    def java_info(self, java_binary: str = None) -> JavaInfo:
        output = self.run("--version", java_binary=java_binary)
        return JavaInfo.from_output(output)

    def run(self, args: str, java_binary: str = None) -> str:
        """
        Execute Java with the given arguments
        """
        java = java_binary if java_binary else self.java
        args = java + " " + args
        process = subprocess.Popen(args.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode != 0:
            raise JavaExecuteError("Return code is not 0", error.decode("utf-8"), self._java)
        return output.decode("utf-8")