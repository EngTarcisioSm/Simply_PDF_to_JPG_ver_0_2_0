import sys
import os
import shutil

from pdf2image import convert_from_path

from models.design import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

class MainWindow(QMainWindow, Ui_MainWindow):
     
     def __init__(self, parent=None):
          super().__init__(parent)
          super().setupUi(self)

          self.dir_file = ''
          self.dir_name = ''
          self.dir_work = ''

          self.pushButtonOpen.clicked.connect(self.open_pdf)
          self.pushButtonSave.clicked.connect(self.save_img)
     
     
     def open_pdf(self):
          file_pdf, _ = QFileDialog.getOpenFileName(
               None,
               'Open PDF',
               r'/%HOME',
          )
          self.dir_file = file_pdf
          self.openFile.setText(file_pdf)
     
     def save_img(self):
          save_jpg = QFileDialog.getExistingDirectory(
               None,
               'Save Dir',
               r'/%HOME',
          )
          self.dir_name = save_jpg
          self.define_dir()

          if self.create_new_dir():
               self.convert()

     def convert(self):
          cwd = os.getcwd()
          cwd = os.path.join(cwd, 'poppler-0.68.0')
          cwd = os.path.join(cwd, 'bin')
          
          print(self.dir_work + 'xyz')
          
          try:
               images = convert_from_path(self.dir_file, poppler_path=cwd)
               for num in range(len(images)):
                    path_img = self.dir_work + '\\' + 'page' + " " + str(num) + '.png'
                    images[num].save(path_img, 'PNG')
          except:
               ...
     
     def define_name_new_dir(self):
          aux = self.dir_file.split('/')
          aux1 = aux[-1].split('.')
          
          if 'pdf' != aux1[1]:
               return None 
          else:
               return aux1[0]

     def create_new_dir(self):
          name_dir = self.define_name_new_dir()
          if name_dir:
               self.dir_work += name_dir
               if os.path.isdir(self.dir_work):
                    shutil.rmtree(self.dir_work)
               os.mkdir(self.dir_work)
               return 1
          else:
               return None            

     def define_dir(self):
          aux = self.dir_name.split('/')
          for part in aux:
               self.dir_work = self.dir_work + part + "\\"

if __name__ == '__main__':
     qt = QApplication(sys.argv)
     new = MainWindow()
     new.show()
     qt.exec_()