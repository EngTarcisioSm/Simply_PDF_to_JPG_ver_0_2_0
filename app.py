import sys
import os
import shutil

from pdf2image import convert_from_path

from threading import Thread
from time import sleep

import math

from models.design import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog


class MainWindow(QMainWindow, Ui_MainWindow):
     
     def __init__(self, parent=None):
          super().__init__(parent)
          super().setupUi(self)

          self.dir_file = ''
          self.dir_name = ''
          self.dir_work = ''
          self.value_progress_bar = 0
          self.convert_proc = 0
          self.cwd = ''

          self.percent = 0

          self.where_i_am()

          self.pushButtonOpen.clicked.connect(self.open_pdf)
          self.pushButtonSave.clicked.connect(self.save_img)
     
     
     def open_pdf(self):
          self.value_progress_bar = 0
          self.progressBar.setValue(self.value_progress_bar)
          file_pdf, _ = QFileDialog.getOpenFileName(
               None,
               'Open PDF',
               r'',
          )
          self.dir_file = file_pdf
          self.openFile.setText(file_pdf)
     
     def save_img(self):
          self.value_progress_bar = 0
          self.progressBar.setValue(self.value_progress_bar)

          save_jpg = QFileDialog.getExistingDirectory(
               None,
               'Save Dir',
               r'',
          )
          self.dir_name = save_jpg
          self.define_dir()

          if self.create_new_dir():
               self.convert()

     def convert(self):
          
          try:
               proc = Thread(target=self.convert_process, args=())
               proc.start()
               while proc.is_alive():
                    sleep(1)

               self.percent = math.floor(100 / len(self.convert_proc))
               print(self.percent)

               for num in range(len(self.convert_proc)):
                    path_img = self.dir_work + '\\' + 'page' + " " + str(num) + '.png'
                    sv = Thread(target=self.save_images, args=(self.convert_proc[num], path_img))
                    sv.start()

                    while sv.is_alive():
                         sleep(1)

                    self.progress()
          except:
               ...
          self.dir_file = ''
          self.dir_name = ''
          self.dir_work = ''
          if self.value_progress_bar != 0 and self.value_progress_bar != 100:
               self.progressBar.setValue(100)

          
     def save_images(self, img, path_img):
          img.save(path_img, 'PNG')

     def convert_process(self):
          self.convert_proc = convert_from_path(self.dir_file, poppler_path=self.cwd)

     def where_i_am(self):
          self.cwd = os.getcwd()
          self.cwd = os.path.join(self.cwd, 'poppler-0.68.0')
          self.cwd = os.path.join(self.cwd, 'bin')
     
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

     def progress(self):
          self.value_progress_bar += self.percent 
          self.progressBar.setValue(self.value_progress_bar)

if __name__ == '__main__':

     qt = QApplication(sys.argv)
     new = MainWindow()
     new.show()
     qt.exec_()