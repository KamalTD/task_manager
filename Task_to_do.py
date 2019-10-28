
import sys
import json
import os
import webbrowser

import winsound

from PyQt5.QtWidgets import *

from  Creat_New_Task import AddTaskWindow

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import Qt

from PyQt5.QtCore import QTimer

from PyQt5.QtGui import QFont

from PyQt5.QtCore import QDate

import time

from datetime import datetime

from PyQt5.QtCore import QTime

class window(QMainWindow):

    def __init__(self):

        super(window,self).__init__()

        self.show_AddTaskWindow = AddTaskWindow()

        self.UI()

        self.center()

        self.update_list_task()

        self.show()

    def update_list_task(self):

        self.Task_List.clear()

        try:
            task_data_file = open("task_data.txt","r")

            self.data = json.load(task_data_file)



            for task in self.data:



                global task_list_item

                task_list_item = QListWidgetItem()

                task_list_item.setText(task)

                task_list_item.setFlags(task_list_item.flags() | Qt.ItemIsUserCheckable)

                for i in self.data[task]:

                    self.Task_List.addItem(task_list_item)

                    task_list_item.setCheckState(i["Done"])

                    if i["Done"] == 0:

                        task_list_item.setFont(self.font_StrikeOut)
                    elif i["Done"]==2:
                        task_list_item.setFont(self.font_UnStrikeOut)




            return task_list_item

        except:

            pass

    def UI(self):
        
        self.font_StrikeOut = QFont()
        self.font_StrikeOut.setStrikeOut(True)

        self.font_UnStrikeOut = QFont()

        self.font_UnStrikeOut.setStrikeOut(False)

        #=========================== Main Window Setup
        self.setWindowTitle("My Tasks Today")
        self.setGeometry(500,50,290,800)
        self.setWindowIcon((QIcon("../images/images.png")))
        self.setMaximumHeight(800)
        self.setMaximumWidth(290)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        #========================== Layout Setup
        self.Vertical_Layout = QVBoxLayout()
        self.Horizontal_Layout = QHBoxLayout()
        self.Horizontal_Layout02 = QHBoxLayout()
        self.Horizontal_Layout03 = QHBoxLayout()
        #========================== Widgets Setup
        self.Button_Add = QPushButton("Add")
        self.Button_Add.clicked.connect(self.add_task)

        self.Button_Remove = QPushButton("Remove")
        self.Button_Remove.clicked.connect(self.remove_task)


        self.Button_refresh = QPushButton("Refresh")
        self.Button_refresh.clicked.connect(self.refresh)

        self.timer = QTimer(self)
        self.alarm_timer = QTimer(self)
        self.alarm_timer.setInterval(50)
        self.alarm_timer.timeout.connect(self.alarm)
        self.alarm_timer.start()
        self.timer.setInterval(50)
        self.timer.stop()
        self.timer.timeout.connect(self.show_me)

        self.tool_bar = QToolBar("Tool Bar")
        self.new_Tool = QAction(QIcon("../images/document_add_100293.png"),"NewTask")
        self.tool_bar.addAction(self.new_Tool)
        self.edit_Tool = QAction(QIcon("../images/misc_edit_98007.jpg"),"EditTask")
        self.tool_bar.addAction(self.edit_Tool)
        self.delete_Tool = QAction(QIcon("../images/document_delete_100294.png"),"DeleteTask")
        self.tool_bar.addAction(self.delete_Tool)
        self.show_AddTaskWindow.save_button.clicked.connect(lambda: self.save_task(2))

        self.show_AddTaskWindow.cancel_button.clicked.connect(self.close_window)

        self.refresh_Tool = QAction(QIcon("../images/rounded_blue_refresh_button_4808.png"),"RefreshTasks")
        self.tool_bar.addAction(self.refresh_Tool)

        self.new_Tool.triggered.connect(self.add_task)
        self.delete_Tool.triggered.connect(self.remove_task)
        self.refresh_Tool.triggered.connect(self.refresh)
        self.edit_Tool.triggered.connect(self.edit_task)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.Task_List = QListWidget()
        self.Task_List.itemClicked.connect(self.task_one_click)

        #self.Task_List.doubleClicked.connect(self.run_task)
        self.data_table = QTableWidget()
        self.data_table.setMaximumHeight(200)
        self.data_table.setRowCount(5)
        self.data_table.setColumnCount(1)
        self.data_table.setColumnWidth(0,self.maximumWidth()-40)
        self.data_table.setVerticalHeaderItem(0, QTableWidgetItem("Name"))
        self.data_table.setVerticalHeaderItem(1, QTableWidgetItem("Link"))
        self.data_table.setVerticalHeaderItem(2, QTableWidgetItem("End By"))
        self.data_table.setVerticalHeaderItem(3, QTableWidgetItem("Status"))
        self.data_table.setVerticalHeaderItem(4, QTableWidgetItem("Notes"))
        self.data_table.setRowHeight(4,70)
        self.data_table.horizontalHeader().hide()
        self.data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.data_table.cellDoubleClicked.connect(self.run_task)


        #=========================== Add Widget to Layout
        self.Vertical_Layout.addWidget(self.tool_bar)
        #self.Horizontal_Layout.addWidget(self.Button_Add)

        #self.Horizontal_Layout.addWidget(self.Button_Remove)
        self.Horizontal_Layout02.addWidget(self.Task_List)


        #self.Horizontal_Layout03.addWidget(self.Button_refresh)

        #================================================
        self.Vertical_Layout.addLayout(self.Horizontal_Layout03)
        self.Vertical_Layout.addLayout(self.Horizontal_Layout)
        self.Vertical_Layout.addLayout(self.Horizontal_Layout02)
        self.Vertical_Layout.addWidget(self.data_table)
        self.show_AddTaskWindow.update_button.clicked.connect(self.update_task)
        self.widget.setLayout(self.Vertical_Layout)


        #============================================ Build Actions




    def add_task(self):

        now = datetime.now()

        self.show_AddTaskWindow.show()

        self.show_AddTaskWindow.setWindowTitle("Add New Task")

        self.show_AddTaskWindow.save_button.setHidden(False)

        self.show_AddTaskWindow.update_button.setHidden(True)

        self.show_AddTaskWindow.date.setTime(QTime(datetime.now().time().hour,datetime.now().time().minute,datetime.now().time().second))

        self.show_AddTaskWindow.date.setDate(QDate(datetime.now().date()))

        self.timer.start()

        self.update_list_task()

    def table_data_build(self,item_name,link,dead_line,status,note):

        try:

            self.data_table.setItem(0,0,QTableWidgetItem(item_name))

            self.data_table.setItem(1, 0, QTableWidgetItem(link))

            self.data_table.setItem(2, 0, QTableWidgetItem(dead_line))

            if status == 0:

                status_ = "Done"

            elif status == 2:

                status_ = "In Progress"

            else:

                status_ = "None"

            self.data_table.setItem(3, 0, QTableWidgetItem(status_))

            self.data_table.setItem(4, 0, QTableWidgetItem(note))

        except:

            print ("Error To Apply")



    def remove_task(self):

        try:
            self.message = QMessageBox.question(self,"Confirm",'Are You Sure! You Need To Delete "%s""'%self.Task_List.currentItem().text(),QMessageBox.Yes,QMessageBox.No)

            if self.message == QMessageBox.Yes:

                del self.data[self.Task_List.currentItem().text()]

                outfile = open("task_data.txt","w")

                json.dump(self.data, outfile,indent=4)

                self.Task_List.takeItem(self.Task_List.row(self.Task_List.selectedItems()[0]))
        except:

            self.message = QMessageBox.information(self, "Hold","Nothing to Remove", QMessageBox.Ok)



    def refresh(self):

        python = sys.executable

        os.execl(python, python, *sys.argv)


    def run_task(self):

        for i in self.data[self.Task_List.currentItem().text()]:

            webbrowser.open_new(i['website'])


    def task_one_click(self,item):

        try:
            check_state = item.checkState()

            task_data_file = open("task_data.txt", "r")

            data = json.load(task_data_file)


            self.update_done_startus(item,item.text(),check_state)

            for data_ in data[item.text()]:

                self.table_data_build(item.text(),data_["website"],data_["Dead_Line"],data_["Done"],data_['Note'])
        except:
            print("Error")



    def edit_task(self):

        try:

            self.timer.start()

            self.show_AddTaskWindow.task_name.setText(self.Task_List.currentItem().text())

            self.show_AddTaskWindow.task_link.setText(self.data[self.Task_List.currentItem().text()][0]['website'])

            self.show_AddTaskWindow.task_notes.setText(self.data[self.Task_List.currentItem().text()][0]['Note'])

            dead_line_date = self.data[self.Task_List.currentItem().text()][0]['Dead_Line'].split(" || ")

            self.show_AddTaskWindow.date.setDate(QDate(datetime.strptime(dead_line_date[0], '%a %b %d %Y')))

            dead_line_time = dead_line_date[1].split(":")



            self.show_AddTaskWindow.date.setTime(QTime(int(dead_line_time[0]), int(dead_line_time[1]), int(dead_line_time[2]) ))



            self.show_AddTaskWindow.save_button.setHidden(True)

            self.show_AddTaskWindow.update_button.setHidden(False)

            self.show_AddTaskWindow.setWindowTitle("Edit %s" % self.Task_List.currentItem().text())

            self.show_AddTaskWindow.show()
        except:
            self.message_err = QMessageBox.information(self, "Hold", "Select Item From The List", QMessageBox.Ok)

    def show_me(self):

        if self.show_AddTaskWindow.isVisible():

            self.setDisabled(True)


        else:

            self.setDisabled(False)

            self.update_list_task()

            self.timer.stop()


    def update_task(self):

        self.delete_old_task()

        self.save_task(2)

        self.update_list_task()



    def delete_old_task(self):

        global current_task

        current_task = self.Task_List.currentItem().text()

        self.data.pop(current_task, None)

        outfile = open("task_data.txt", "w")

        json.dump(self.data, outfile, indent=4)


    def save_task(self,Done=2):

        task_name_var = self.show_AddTaskWindow.task_name.toPlainText()

        task_link_var = self.show_AddTaskWindow.task_link.toPlainText()

        task_note_var = self.show_AddTaskWindow.task_notes.toPlainText()

        try:
            task_data_file = open("task_data.txt", "r")

            data = json.load(task_data_file)

        except:


            data = {}
        outfile = open("task_data.txt", "w")

        data['%s'%task_name_var] = []




        data['%s'%task_name_var].append({'name': task_name_var,'website': task_link_var, "Done": Done,

        "Dead_Line" : "%s || %s" %(self.show_AddTaskWindow.date.date().toString() , self.show_AddTaskWindow.date.time().toString()) ,

        "Date" : self.show_AddTaskWindow.date.date().toString(), "Status": "False","Note":task_note_var,
        })




        outfile.seek(0)

        json.dump(data, outfile,indent=4)



        self.show_AddTaskWindow.close()



    def alarm(self):
        now = datetime.now()



        try:
            try:
                task_data_file = open("task_data.txt", "r")

                data = json.load(task_data_file)

            except:

                data = {}

            for task in data:

                for data_ in data[task]:

                    data_date = data_["Dead_Line"].split(" || ")

                    if data_date[1][:-3] == now.time().strftime("%H:%M") and QDate(datetime.strptime(data_date[0], '%a %b %d %Y')) == now.date():

                        if data_["Status"] == "False":

                            task_data_file = self.update_list_task()

                            task_data_file.setCheckState(0)

                            task_data_file.setFont(self.font_StrikeOut)

                            outfile = open("task_data.txt", "w")

                            print(data_["name"],data_["Status"])

                            del data_["Status"]

                            del data_["Done"]

                            data_["Done"] = 0

                            data_["Status"] = "True"


                            #
                            outfile.seek(0)
                            #
                            json.dump(data, outfile, indent=4)
                            #self.setWindowFlag(Qt.WindowStaysOnTopHint)
                            winsound.PlaySound("ALERT.wav", winsound.SND_FILENAME )
                            message = QMessageBox.information(self,"Time's Gone!" ,"%s | Task Hase Ended "%data_["name"],QMessageBox.Ok)
                            if message == QMessageBox.Ok:
                                task_data_file.setSelected(1)

                                self.setWindowFlag(Qt.StrongFocus)

                            break




        except:
            pass






    def update_done_startus(self,item,task_name_var,Done=2):

        try:
            task_data_file = open("task_data.txt", "r")

            data = json.load(task_data_file)

        except:


            data = {}

        outfile = open("task_data.txt", "w")

        for don in data['%s'%task_name_var]:

            del don["Done"]

            don["Done"]= Done

        if Done == 0:

            item.setFont(self.font_StrikeOut)
        elif Done == 2:

            item.setFont(self.font_UnStrikeOut)

        print(item.checkState())

        outfile.seek(0)

        json.dump(data, outfile,indent=4)

    def close_window(self):

        self.show_AddTaskWindow.close()

    def center(self):
        frameGm = self.frameGeometry()

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())

        centerPoint =QApplication.desktop().screenGeometry(screen).center()

        frameGm.moveCenter(centerPoint)

        self.move(frameGm.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    import qdarkstyle

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = window()

    sys.exit(app.exec_())
