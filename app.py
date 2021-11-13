import sys
from models.design import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

class MainWindow(QMainWindow, Ui_MainWindow):
     
     def __init__(self, parent=None):
          super().__init__(parent)
          super().setupUi(self)

          self.pushButtonOpen.clicked.connect(self.open_pdf)
          self.pushButtonSave.clicked.connect(self.save_img)
     
     
     def open_pdf(self):
          print('passou aqui')
          file_pdf, _ = QFileDialog.getOpenFileName(
               None,
               'Open PDF',
               r'/%HOME',
          )
          self.openFile.setText(file_pdf)
     
     def save_img(self):
          print('passou aqui')
          save_jpg = QFileDialog.getExistingDirectory(
               None,
               'Save Dir',
               r'/%HOME',
          )
          print(save_jpg)


if __name__ == '__main__':
     qt = QApplication(sys.argv)
     new = MainWindow()
     new.show()
     qt.exec_()