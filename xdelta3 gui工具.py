
import os
import subprocess
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QFileDialog, QMessageBox,
                            QComboBox, QProgressBar, QSizePolicy)
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self._is_running = True

    def run(self):
        try:
            process = subprocess.Popen(
                self.cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            while self._is_running:
                # 读取标准输出和错误输出
                output = process.stdout.readline()
                error = process.stderr.readline()
                
                if output == '' and error == '' and process.poll() is not None:
                    break
                    
                if output:
                    # 解析xdelta3的输出获取进度
                    progress = self.parse_xdelta_output(output)
                    if progress is not None:
                        self.progress_updated.emit(progress)
                        
                if error:
                    # 处理错误信息
                    pass
                    
                self.msleep(100)
                
            if self._is_running:
                self.progress_updated.emit(100)
                self.finished.emit(True, "操作成功完成")
            else:
                self.finished.emit(False, "操作已取消")
                
        except Exception as e:
            self.finished.emit(False, f"操作失败: {str(e)}")

    def parse_xdelta_output(self, output):
        """
        解析xdelta3命令行输出获取进度百分比
        示例输出行: "50% completed, 1234/5678 bytes"
        """
        try:
            # 查找百分比数字
            percent_index = output.find('%')
            if percent_index > 0:
                # 提取百分比前的数字
                num_str = ''
                i = percent_index - 1
                while i >= 0 and output[i].isdigit():
                    num_str = output[i] + num_str
                    i -= 1
                    
                if num_str:
                    return int(num_str)
        except:
            pass
        return None

    def stop(self):
        self._is_running = False
        self.wait()

class XDeltaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("xdelta3 GUI工具")
        
        # 主控件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # 模式选择
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("生成补丁模式")
        self.mode_combo.addItem("应用补丁模式")
        self.mode_combo.currentIndexChanged.connect(self.switch_mode)
        self.layout.addWidget(self.mode_combo)
        
        # 文件选择区域
        self.create_file_selectors()
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.layout.addWidget(self.progress)
        
        # 操作按钮
        self.create_action_buttons()
        
        main_widget.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(500, 400)
        
        # 确保xdelta3.exe在同一目录
        self.xdelta_path = os.path.join(os.path.dirname(__file__), "xdelta3.exe")
        if not os.path.exists(self.xdelta_path):
            QMessageBox.critical(self, "错误", "未找到xdelta3.exe程序")
            sys.exit(1)
        
        # 初始化模式
        self.switch_mode(0)
        self.worker = None

    def create_file_selectors(self):
        # 旧文件选择
        self.old_file = ""
        self.old_layout = QHBoxLayout()
        self.old_label = QLabel("旧文件:")
        self.old_path_label = QLabel("未选择")
        self.old_path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.old_btn = QPushButton("选择")
        self.old_btn.clicked.connect(lambda: self.select_file("old"))
        self.old_layout.addWidget(self.old_label)
        self.old_layout.addWidget(self.old_path_label)
        self.old_layout.addWidget(self.old_btn)
        self.layout.addLayout(self.old_layout)
        
        # 新文件选择 (生成补丁模式)
        self.new_file = ""
        self.new_layout = QHBoxLayout()
        self.new_label = QLabel("新文件:")
        self.new_path_label = QLabel("未选择")
        self.new_path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.new_btn = QPushButton("选择")
        self.new_btn.clicked.connect(lambda: self.select_file("new"))
        self.new_layout.addWidget(self.new_label)
        self.new_layout.addWidget(self.new_path_label)
        self.new_layout.addWidget(self.new_btn)
        self.layout.addLayout(self.new_layout)
        
        # 补丁文件选择
        self.patch_file = ""
        self.patch_layout = QHBoxLayout()
        self.patch_label = QLabel("补丁文件:")
        self.patch_path_label = QLabel("未选择")
        self.patch_path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.patch_btn = QPushButton("选择")
        self.patch_btn.clicked.connect(lambda: self.select_file("patch"))
        self.patch_layout.addWidget(self.patch_label)
        self.patch_layout.addWidget(self.patch_path_label)
        self.patch_layout.addWidget(self.patch_btn)
        self.layout.addLayout(self.patch_layout)
        
        # 输出文件选择 (应用补丁模式)
        self.output_file = ""
        self.output_layout = QHBoxLayout()
        self.output_label = QLabel("输出文件:")
        self.output_path_label = QLabel("未选择")
        self.output_path_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.output_btn = QPushButton("选择")
        self.output_btn.clicked.connect(lambda: self.select_file("output"))
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output_path_label)
        self.output_layout.addWidget(self.output_btn)
        self.layout.addLayout(self.output_layout)

    def create_action_buttons(self):
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        self.start_btn = QPushButton("开始处理")
        self.start_btn.clicked.connect(self.start_process)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("停止处理")
        self.stop_btn.clicked.connect(self.stop_process)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        btn_layout.addStretch(1)
        self.layout.addLayout(btn_layout)

    def switch_mode(self, index):
        # 生成补丁模式
        if index == 0:
            self.new_label.setText("新文件:")
            self.new_btn.setEnabled(True)
            self.new_layout.itemAt(0).widget().show()  # 显示标签
            self.new_layout.itemAt(1).widget().show()  # 显示路径标签
            self.new_layout.itemAt(2).widget().show()  # 显示按钮
            self.patch_label.setText("补丁保存路径:")
            self.output_layout.itemAt(0).widget().hide()
            self.output_layout.itemAt(1).widget().hide()
            self.output_layout.itemAt(2).widget().hide()
        # 应用补丁模式
        else:
            self.new_layout.itemAt(0).widget().hide()  # 隐藏标签
            self.new_layout.itemAt(1).widget().hide()  # 隐藏路径标签
            self.new_layout.itemAt(2).widget().hide()  # 隐藏按钮
            self.patch_label.setText("补丁文件:")
            self.output_layout.itemAt(0).widget().show()
            self.output_layout.itemAt(1).widget().show()
            self.output_layout.itemAt(2).widget().show()

    def select_file(self, file_type):
        if file_type == "old":
            file, _ = QFileDialog.getOpenFileName(self, "选择旧文件")
            if file:
                self.old_file = file
                self.old_path_label.setText(os.path.basename(file))
        elif file_type == "new":
            file, _ = QFileDialog.getOpenFileName(self, "选择新文件")
            if file:
                self.new_file = file
                self.new_path_label.setText(os.path.basename(file))
        elif file_type == "patch":
            if self.mode_combo.currentIndex() == 0:  # 生成补丁模式
                file, _ = QFileDialog.getSaveFileName(self, "保存补丁文件", "", "Delta Files (*.delta)")
            else:  # 应用补丁模式
                file, _ = QFileDialog.getOpenFileName(self, "选择补丁文件", "", "Delta Files (*.delta)")
            if file:
                self.patch_file = file
                self.patch_path_label.setText(os.path.basename(file))
        elif file_type == "output":
            file, _ = QFileDialog.getSaveFileName(self, "选择输出文件")
            if file:
                self.output_file = file
                self.output_path_label.setText(os.path.basename(file))

    def start_process(self):
        mode = self.mode_combo.currentIndex()
        
        # 生成补丁模式
        if mode == 0:
            if not all([self.old_file, self.new_file, self.patch_file]):
                QMessageBox.warning(self, "警告", "请选择所有必需的文件")
                return
            cmd = [self.xdelta_path, "-e", "-s", self.old_file, self.new_file, self.patch_file]
        # 应用补丁模式
        else:
            if not all([self.old_file, self.patch_file]):
                QMessageBox.warning(self, "警告", "请选择旧文件和补丁文件")
                return
            if not self.output_file:
                base_name = os.path.splitext(os.path.basename(self.patch_file))[0]
                self.output_file = os.path.join(os.path.dirname(self.old_file), f"{base_name}_patched")
                self.output_path_label.setText(os.path.basename(self.output_file))
            cmd = [self.xdelta_path, "-d", "-s", self.old_file, self.patch_file, self.output_file]
        
        self.progress.setValue(0)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        self.worker = Worker(cmd)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.process_finished)
        self.worker.start()

    def stop_process(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.progress.setValue(0)
            QMessageBox.information(self, "信息", "操作已取消")

    def update_progress(self, value):
        self.progress.setValue(value)

    def process_finished(self, success, message):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.critical(self, "错误", message)
        self.progress.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XDeltaGUI()
    window.show()
    sys.exit(app.exec_())
