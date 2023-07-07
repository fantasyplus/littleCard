import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox, QFileDialog
import sys
import os
from os import path
d = path.dirname(__file__)  # 获取当前路径
parent_path = os.path.dirname(d)  # 获取上一级路径
sys.path.append(parent_path)    # 如果要导入到包在上一级

from backend.database import writeToDataBase

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('狗宝的Qt界面')
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        file_layout = QHBoxLayout()
        self.button = QPushButton('涛涛三分糖更新数据库', self)
        self.button.clicked.connect(self.buttonClicked)
        file_layout.addWidget(self.button)

        # 添加新按钮
        self.extraButton = QPushButton('涛涛三分糖额外按钮', self)
        file_layout.addWidget(self.extraButton)

        layout.addLayout(file_layout)

        self.confirmButton = QPushButton('三分糖确认', self)
        self.confirmButton.clicked.connect(self.confirmButtonClicked)
        layout.addWidget(self.confirmButton)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(3)  # 设置表格有三列
        layout.addWidget(self.tableWidget)

        self.setLayout(layout)

        self.selected_file_path = None

    def buttonClicked(self):
        output=writeToDataBase()
        # 将output插入到QTableWidget的某一行的第一格中
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        item = QTableWidgetItem(output)
        self.tableWidget.setItem(row, 0, item)

    def confirmButtonClicked(self):
        if self.selected_file_path:
            print("文件路径: {}".format(self.selected_file_path))
        else:
            print("未选择任何文件！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
