import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QAction, QFileDialog, QToolBar
from PyQt5.QtGui import QPainter, QPen, QColor, QImage
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize
import json
import numpy as np
import re
import asyncio
from BluetoothCommandThread import BluetoothCommandThread

class DrawingWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        
        # click tracker
        self.isClicked = False
        self.clickId = -1
        
        # initialize the button positions
        self.button_size = 20
        self.buttons = []
        ids = [5, 4, 3, 2, 1, 6, 7, 8, 9, 10, 15, 14, 13, 12, 11, 16, 17, 18, 19, 20]
        for i in range(4):
            for j in range(5):
                pos = QPoint(825+j*153, 100+i*150)
                id = ids[i*5 + j]
                self.buttons.append({"pos":pos, "id":id, "isClicked":False})

        self.background_image = QImage("data/Full_length_background.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.background_image)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)

        for button in self.buttons:
            painter.drawEllipse(button["pos"], self.button_size, self.button_size)
            painter.drawText(button["pos"], str(button["id"]))

    def mousePressEvent(self, event):
        if not self.isClicked and event.button() == Qt.LeftButton:
            # check if event.pos() is on any button, if yes, update status
            print(event.pos())
            for button in self.buttons:
                if (button["pos"] - event.pos()).manhattanLength() < self.button_size*2:
                    self.isClicked = True
                    self.clickId = self.buttons.index(button)
                    print("button ", button["id"], " is clicked")
                    button["isClicked"] = True
                    self.update()

    def clearClick(self):
        self.isClicked = False
        self.buttons[self.clickId]["isClicked"] = False
        self.clickId = -1
        self.update()
    

class MainWindow(QMainWindow):
    bluetooth_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawing Application")

        # initialization
        self.drawing_widget = DrawingWidget()
        self.setCentralWidget(self.drawing_widget)
        self.resize(1600, 900)  # Set the window size
        self.createMenu()
        self.createToolbar()

        # state tracker
        self.current_round = 0
        self.isStart = False
        self.experiment_round_total = 0
        self.experiment_commands = []
        self.clicked_button_ids = []


    '''
    Load motor positions from setup file
    '''
    def importSetupFile(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Import Experiment File", "", "JSON Files (*.json)")
        if file_path:
            # Parse the setup file to extract motor positions
            self.experiment_round_total = 0
            self.experiment_commands.clear()
            with open(file_path, "r") as file:
                lines = file.readlines()
                self.experiment_round_total = len(lines)
                for line in lines:
                    command_strs = re.findall(r'{[^{}]*}', line)
                    commands = []
                    for command_str in command_strs:
                        print(command_str)
                        commands.append(command_str)
                    self.experiment_commands.append(commands)
            print("new experiment file loaded, data num = ", self.experiment_round_total)
    
    '''
    save drawings to a local file
    '''
    def saveDataToFile(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Data to File", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "w") as file:
                print(self.clicked_button_ids)
                for i in range(len(self.clicked_button_ids)):
                    file.write(str(self.clicked_button_ids[i])+"\n")
            print("save data to file", file_path)

    def createMenu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        import_action = QAction("Import Experiment File", self)
        import_action.triggered.connect(self.importSetupFile)
        file_menu.addAction(import_action)

        save_action = QAction("Save Data to File", self)
        save_action.triggered.connect(self.saveDataToFile)
        file_menu.addAction(save_action)

    def createToolbar(self):
        toolbar = QToolBar()
        toolbar.setFixedHeight(50)  # Set the desired height for the toolbar
        toolbar.setStyleSheet("QToolButton { min-width: 120px; min-height: 50px}")
        self.addToolBar(toolbar)

        self.start_button = QAction("Start", self)
        self.start_button.triggered.connect(self.startButtonClicked)
        toolbar.addAction(self.start_button)

        self.confirm_button = QAction("Confirm", self)
        self.confirm_button.triggered.connect(self.confirmButtonClicked)
        toolbar.addAction(self.confirm_button)

        self.clear_button = QAction("Clear", self)
        self.clear_button.triggered.connect(self.clearButtonClicked)
        toolbar.addAction(self.clear_button)

        self.message_line = QLabel("message", self)
        toolbar.addWidget(self.message_line)

    def startButtonClicked(self):
        print("Start button clicked")
        if not self.isStart:
            if self.current_round < self.experiment_round_total:
                print("send command for ", self.current_round)
                self.message_line.setText('trial #'+str(self.current_round))
                self.isStart = True
                ### Trigger Bluetooth command
                print(self.experiment_commands[self.current_round])
                commands = '\n'.join(self.experiment_commands[self.current_round])
                self.bluetooth_signal.emit(commands)
                self.start_button.setText("Play Again")
            else:
                print("test finished!")
        else:
            print("play again")
            # Only Trigger Bluetooth command
            commands = '\n'.join(self.experiment_commands[self.current_round])
            self.bluetooth_signal.emit(commands)

    def confirmButtonClicked(self):
        print("Confirm button clicked")
        # save the drawing to results
        if self.isStart:
            if self.drawing_widget.clickId != -1:
                print("Data saved")
                self.clicked_button_ids.append(self.drawing_widget.buttons[self.drawing_widget.clickId]["id"])
                self.drawing_widget.clearClick()
                self.isStart = False
                self.current_round += 1
                self.start_button.setText("Start")
            else:
                print("no button is clicked!")
        else:
            print("trial is not started yet!")

    def clearButtonClicked(self):
        print("Clear button clicked")
        # call the function to clean current drawings
        self.drawing_widget.clearClick()

# Main function
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    ### Create and start the Bluetooth thread
    loop = asyncio.get_event_loop()
    bluetooth_thread = BluetoothCommandThread(loop)
    window.bluetooth_signal.connect(bluetooth_thread.bluetooth_callback)
    bluetooth_thread.start()

    sys.exit(app.exec_())

# Run the main function
if __name__ == "__main__":
    main()
