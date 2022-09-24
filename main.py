
from window import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt5 import QtGui,QtWidgets,QtCore
from image_info import get_info
from predict_yolov5 import Predict_v5
from predict_yolov4 import Predict_v4
from predict_faster import Predict_faster
import os,shutil
from PIL import Image

class MyWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.org_img.setStyleSheet("background-color: CornflowerBlue")
        self.result_img.setStyleSheet("background-color: CornflowerBlue")
        self.openimg.clicked.connect(self.open_img_handler)
        self.opendir.clicked.connect(self.open_dir_handler)
        self.quit_btn.clicked.connect(QtCore.QCoreApplication.quit)

        self.org_img.resize(600, 300)
        self.org_img.setScaledContents(True)
        self.result_img.resize(600, 300)
        self.result_img.setScaledContents(True)
        self.number.setReadOnly(True)

        self.models.addItem("YOLOv5")
        self.models.addItem("YOLOv4")
        self.models.addItem("Faster RCNN")
        self.models.currentIndexChanged[int].connect(self.get_value)

        self.predict.clicked.connect(self.predict_handler)
        self.save.clicked.connect(self.save_handler)
        self.result_path.setPlainText("null")
        self.mode = 0
        self.detected=False
        self.filename_one_img = ''
        self.directory_path = ''
        self.video_path = ''




    def open_img_handler(self):
        self.result_img.clear()
        self.filename_one_img,_=QtWidgets.QFileDialog.getOpenFileName()
        self.image_path.setPlainText(self.filename_one_img)
        if self.filename_one_img!='':
            width, height, channel = get_info(self.filename_one_img)
            self.width.setPlainText(width)
            self.height.setPlainText(height)
            self.channel.setPlainText(channel)
            self.org_img.setPixmap(QtGui.QPixmap(self.filename_one_img))
        else:

            self.width.setPlainText("null")
            self.height.setPlainText("null")
            self.channel.setPlainText("null")
            self.org_img.setPixmap(QtGui.QPixmap("./static/error.jpeg"))

    def open_dir_handler(self):
        self.result_img.clear()
        self.directory_path=QtWidgets.QFileDialog.getExistingDirectory(self,"选择文件夹")
        self.image_path.setPlainText(self.directory_path)
        if self.directory_path != '':
            self.org_img.setPixmap(QtGui.QPixmap("./static/folder.jpeg"))
            self.width.setPlainText("多张")
            self.height.setPlainText("多张")
            self.channel.setPlainText("多张")
        else:
            self.width.setPlainText("null")
            self.height.setPlainText("null")
            self.channel.setPlainText("null")
            self.org_img.setPixmap(QtGui.QPixmap("./static/error.jpeg"))



    def get_value(self,i):
        self.mode=i


    def predict_handler(self):
        if self.mode==0:
            self.yolov5_predict_handler()
        elif self.mode==1:
            self.yolov4_predict_handler()
        elif self.mode==2:
            self.faster_predict_handler()


    def yolov5_predict_handler(self):
        if self.filename_one_img != '':
            msg_box = QMessageBox(QMessageBox.Information, '使用YOLOV5', '使用Yolov5预测')
            msg_box.exec_()
            result_path,numbers=Predict_v5(self.filename_one_img,1)
            self.result_img.setPixmap(QtGui.QPixmap(result_path))
            numbers_s=str(numbers)
            self.number.setPlainText(numbers_s)
            self.result_path.setPlainText(result_path)

        elif self.directory_path != '':
            msg_box = QMessageBox(QMessageBox.Information, '使用YOLOV5', '使用Yolov5预测')
            msg_box.exec_()
            result_path=Predict_v5(self.directory_path,3)
            self.number.setPlainText("多张")
            self.result_img.setPixmap(QtGui.QPixmap("./static/folder.jpeg"))
            self.result_path.setPlainText(result_path+"/")

        else:
            msg_box = QMessageBox(QMessageBox.Critical, '错误', '未输入图片！')
            msg_box.exec_()

    def yolov4_predict_handler(self):
        if self.filename_one_img != '':
            msg_box = QMessageBox(QMessageBox.Information, '使用YOLOV4', '使用Yolov4预测')
            msg_box.exec_()
            result_path,numbers=Predict_v4(self.filename_one_img,1)
            self.result_img.setPixmap(QtGui.QPixmap(result_path))
            numbers_s=str(numbers)
            self.number.setPlainText(numbers_s)
            self.result_path.setPlainText(result_path)
        elif self.directory_path != '':
            msg_box = QMessageBox(QMessageBox.Information, '使用YOLOV4', '使用Yolov4预测')
            msg_box.exec_()
            result_path=Predict_v4(self.directory_path,3)
            self.number.setPlainText("多张")
            self.result_img.setPixmap(QtGui.QPixmap("./static/folder.jpeg"))
            self.result_path.setPlainText(result_path+"/")

        else:
            msg_box = QMessageBox(QMessageBox.Critical, '错误', '未输入图片！')
            msg_box.exec_()

    def faster_predict_handler(self):
        if self.filename_one_img != '':
            msg_box = QMessageBox(QMessageBox.Information, '使用Faster RCNN', '使用Faster RCNN预测')
            msg_box.exec_()
            result_path,numbers=Predict_faster(self.filename_one_img,1)
            self.result_img.setPixmap(QtGui.QPixmap(result_path))
            numbers_s=str(numbers)
            self.number.setPlainText(numbers_s)
            self.result_path.setPlainText(result_path)
            self.detected=True
        elif self.directory_path != '':
            msg_box = QMessageBox(QMessageBox.Information, '使用Faster RCNN', '使用Faster RCNN预测')
            msg_box.exec_()
            result_path=Predict_faster(self.directory_path,3)
            self.number.setPlainText("多张")
            self.result_img.setPixmap(QtGui.QPixmap("./static/folder.jpeg"))
            self.result_path.setPlainText(result_path+"/")

        else:
            msg_box = QMessageBox(QMessageBox.Critical, '错误', '未输入图片！')
            msg_box.exec_()

    def save_handler(self):

        if self.result_path.toPlainText()=="null":

            msg_box = QMessageBox(QMessageBox.Critical, '错误', '请先运行检测！')
            msg_box.exec_()
        else:
            if self.directory_path!= '':
                result_dir=self.result_path.toPlainText()

                self.save_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'save file')
                save_dir_path=self.save_path+"/"
                src_files=os.listdir(result_dir)
                for filename in src_files:
                    full_name=os.path.join(result_dir,filename)
                    if os.path.isfile(full_name):
                        shutil.copy(full_name,save_dir_path)
                self.result_path.setPlainText(save_dir_path)

            else:
                image = Image.open(self.result_path.toPlainText())

                self.save_path=QtWidgets.QFileDialog.getExistingDirectory(self, 'save file')
                save_image_path=self.save_path+"/"+"result.jpg"
                image.save(save_image_path)
                self.result_path.setPlainText(save_image_path)







if __name__ == '__main__':
    # application 对象
    app = QApplication(sys.argv)

    # QMainWindow对象
    mainwindow = MyWindow()



    # 显示
    mainwindow.show()
    app.exec_()



