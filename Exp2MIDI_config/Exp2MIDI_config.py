import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports

class ExpressionPedalCalibrator:
    def __init__(self, root):
        self.root = root
        self.root.title("Expression Pedal Calibrator")
        self.serial_port = None
        self.calibration_step = 0  # 캘리브레이션 단계 (0: 준비, 1: 최소값, 2: 최대값, 3: 완료)

        # GUI 요소 생성
        self.label = tk.Label(root, text="Expression Pedal Calibrator")
        self.label.pack(pady=10)

        self.calibrate_button = tk.Button(root, text="Calibrate", command=self.start_calibration)
        self.calibrate_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next", command=self.next_step, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Not Connected")
        self.status_label.pack(pady=10)

        self.detect_port_button = tk.Button(root, text="Detect Arduino", command=self.detect_arduino)
        self.detect_port_button.pack(pady=10)

        self.cc11_button = tk.Button(root, text="Set CC# to 11", command=self.set_cc11)
        self.cc11_button.pack(pady=10)

        self.cc1_button = tk.Button(root, text="Set CC# to 1", command=self.set_cc1)
        self.cc1_button.pack(pady=10)

        self.default_button = tk.Button(root, text="Set Default", command=self.set_default)
        self.default_button.pack(pady=10)

    def detect_arduino(self):
        # 사용 가능한 포트 탐지
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "Arduino Leonardo" in port.description:
                self.serial_port = serial.Serial(port.device, 9600, timeout=1)
                self.status_label.config(text=f"Status: Connected to {port.device}")
                return
        messagebox.showerror("Error", "Arduino Leonardo not found!")

    def start_calibration(self):
        if self.serial_port is None:
            messagebox.showerror("Error", "Arduino not connected!")
            return

        self.calibration_step = 1
        self.calibrate_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)
        self.serial_port.write(b'S')  # 캘리브레이션 시작 명령 전송
        self.status_label.config(text="Step 1: Move pedal to MIN position and click Next.")

    def next_step(self):
        if self.calibration_step == 1:
            self.serial_port.write(b'N')  # 최소값 설정 명령 전송
            self.calibration_step = 2
            self.status_label.config(text="Step 2: Move pedal to MAX position and click Next.")
        elif self.calibration_step == 2:
            self.serial_port.write(b'F')  # 캘리브레이션 완료 명령 전송
            self.calibration_step = 0
            self.next_button.config(state=tk.DISABLED)
            self.calibrate_button.config(state=tk.NORMAL)
            self.status_label.config(text="Calibration complete!")
    
    def set_cc11(self):
        if self.serial_port is None:
            messagebox.showerror("Error", "Arduino not connected!")
            return
        self.serial_port.write(b'C')
        self.status_label.config(text="CC# set to 11")
    
        
    def set_cc1(self):
        if self.serial_port is None:
            messagebox.showerror("Error", "Arduino not connected!")
            return
        self.serial_port.write(b'D')
        self.status_label.config(text="CC# set to 1")

    def set_default(self):
        if self.serial_port is None:
            messagebox.showerror("Error", "Arduino not connected!")
            return
        self.serial_port.write(b'E')
        self.status_label.config(text="Configurations set to default")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpressionPedalCalibrator(root)
    root.mainloop()