import sys
import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import datetime

from PyQt5.QtCore import QDate

class AddTaskWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.UI()


    def UI(self):



        self.hor01 = QHBoxLayout()
        self.hor02 = QHBoxLayout()
        self.hor03 = QHBoxLayout()
        self.hor04 = QHBoxLayout()
        self.hor05 = QHBoxLayout()
        self.ver = QVBoxLayout()

        self.task_name = QTextEdit()
        self.task_notes = QTextEdit()
        self.task_name.setMaximumHeight(30)
        self.task_name.setMaximumHeight(60)
        self.setWindowTitle("Add New Task")
        self.setWindowIcon((QIcon("../images/images.png")))
        self.setFixedSize(400,200)
        self.task_name_label = QLabel("Task Name:: ")
        self.task_date_label = QLabel("Dead Line::")
        self.task_note_label = QLabel("Task Note::")
        self.task_link = QTextEdit()
        self.task_link.setMaximumHeight(30)
        self.task_link_label = QLabel("Task Link:: ")

        self.save_button = QPushButton("Save")

        self.cancel_button = QPushButton("Cancel")

        self.update_button = QPushButton("Update")

        self.date = QDateTimeEdit()
        self.date.setCalendarPopup(True)

        self.date.setDate(QDate(2015,1,1))

        #self.date.setMinimumDate(QDate(2019,1,1))

        # self.date.setMinimumDate(datetime.datetime.now().date())  # QDate(2019,1,1)
        #
        # self.date.setMinimumTime(datetime.datetime.now().time())  # QDate(2019,1,1) Set Min Time

        self.date.dateChanged.connect(self.get_date)

        self.hor01.addWidget(self.task_name_label)
        self.hor01.addWidget(self.task_name)

        self.hor02.addWidget(self.task_link_label)
        self.hor02.addWidget(self.task_link)

        self.hor03.addWidget(self.save_button)
        self.hor03.addWidget(self.update_button)

        self.hor03.addWidget(self.cancel_button)
        self.hor04.addWidget(self.task_date_label)

        self.hor05.addWidget(self.task_note_label)
        self.hor05.addWidget(self.task_notes)

        self.hor04.addWidget(self.date)

        self.ver.addLayout(self.hor01)
        self.ver.addLayout(self.hor02)
        self.ver.addLayout(self.hor05)
        self.ver.addLayout(self.hor04)

        self.ver.addLayout(self.hor03)


        self.setLayout(self.ver)

    def get_date(self):
        print(self.date.date())





    def closeEvent(self, QCloseEvent):

        self.task_link.setText("")

        self.task_name.setText("")





if __name__ == "__main__":
    app = QApplication(sys.argv)

    AddTaskWindow = AddTaskWindow()

    sys.exit(app.exec_())
