import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QAction, QFileDialog, QToolBar
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QBrush
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize
import json
import numpy as np
import re
import asyncio
from BluetoothCommandThread import BluetoothCommandThread

class DrawingWidget(QWidget):

    def __init__(self, mainWindow):
        super().__init__()
        self.setMouseTracking(True)
        self.mainWindow = mainWindow
        
        # click tracker
        self.isClicked = False
        self.clickId = -1
        self.isPractice = True
        
        # initialize the button positions
        self.button_size = 40
        self.buttons = []
        ids = [92,94,96,98,100,109,107,105,103,101,62,64,66,68,70,79,77,75,73,71]
        for i in range(4):
            for j in range(5):
                pos = QPoint(213+j*306, 100+i*150)
                id = ids[i*5 + j]
                self.buttons.append({"pos":pos, "id":id, "isClicked":False})

        self.background_image = QImage("data/Full_length_background.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.background_image)
        brush = QBrush(Qt.red) 
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)

        for button in self.buttons:
            if not button["isClicked"]:
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(button["pos"], self.button_size, self.button_size)
                painter.drawText(button["pos"], str(button["id"]))
            else: # clicked button, add color fill
                painter.setBrush(brush)
                painter.drawEllipse(button["pos"], self.button_size, self.button_size)
                painter.drawText(button["pos"], str(button["id"]))


    def mousePressEvent(self, event):
        if not self.isClicked and event.button() == Qt.LeftButton:
            # check if event.pos() is on any button, if yes, update status
            print(event.pos())
            for i in range(len(self.buttons)):
                button = self.buttons[i]
                if (button["pos"] - event.pos()).manhattanLength() < self.button_size*2:
                    self.isClicked = True
                    self.clickId = self.buttons.index(button)
                    print("button ", button["id"], " is clicked")
                    button["isClicked"] = True
                    self.update()
                    if self.isPractice:
                        print("trigger motor")
                        self.mainWindow.triggerPracticeMotor(i)

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
        self.drawing_widget = DrawingWidget(self)
        self.setCentralWidget(self.drawing_widget)
        self.resize(1600, 900)  # Set the window size
        self.createMenu()
        self.createToolbar()

        # state tracker
        self.current_round = 0
        self.isStart = False
        self.experiment_round_total = 0
        self.experiment_commands = []
        self.template_commands = []
        self.clicked_button_ids = []


    '''
    Load experiment file
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
    Load command file
    '''
    def importTemplateFile(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Import Template File", "", "JSON Files (*.json)")
        if file_path:
            # Parse the setup file to extract motor positions
            self.template_commands_total = 0
            self.template_commands.clear()
            with open(file_path, "r") as file:
                lines = file.readlines()
                self.template_commands_total = len(lines)
                for line in lines:
                    command_strs = re.findall(r'{[^{}]*}', line)
                    commands = []
                    for command_str in command_strs:
                        print(command_str)
                        commands.append(command_str)
                    self.template_commands.append(commands)
            print("new template file loaded, template command num = ", self.template_commands_total)
    
    '''
    save experiment results to a local file
    '''
    def saveDataToFile(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Data to File", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "w") as file:
                print(self.clicked_button_ids)
                for i in range(len(self.clicked_button_ids)):
                    file.write(json.dumps(self.clicked_button_ids[i])+"\n")
            print("save data to file", file_path)

    def createMenu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        import_template_action = QAction("Import Template File", self)
        import_template_action.triggered.connect(self.importTemplateFile)
        file_menu.addAction(import_template_action)

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

        self.intensity_button = QAction("low intensity", self)
        self.intensity_button.triggered.connect(self.intensityButtonClicked)
        toolbar.addAction(self.intensity_button)
        self.isLowIntensity = True

        self.toggle_mode_button = QAction("Practice Mode", self)
        self.toggle_mode_button.triggered.connect(self.toggleButtonClicked)
        toolbar.addAction(self.toggle_mode_button)
        self.isPractice = True

        self.message_line = QLabel("message", self)
        background_color = QColor(200, 200, 200)  # Light blue color (RGB: 200, 200, 255)
        self.message_line.setStyleSheet(f'background-color: {background_color.name()};')
        toolbar.addWidget(self.message_line)


    def startButtonClicked(self):
        print("Start button clicked")
        if not self.isStart:
            if self.current_round < self.experiment_round_total:
                print("send command for ", self.current_round)
                self.message_line.setText('trial #'+str(self.current_round))
                self.isStart = True
                ## Trigger Bluetooth command
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
                self.clicked_button_ids.append({"id":self.drawing_widget.buttons[self.drawing_widget.clickId]["id"], "low_intensity":self.isLowIntensity})
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

    def toggleButtonClicked(self):
        if self.isPractice:
            self.isPractice = False
            self.drawing_widget.isPractice = False
            self.toggle_mode_button.setText("Testing Mode")
            print("toggle mode to testing")
        else:
            self.isPractice = True
            self.drawing_widget.isPractice = True
            self.toggle_mode_button.setText("Practice Mode")
            print("toggle mode to practice")

    def intensityButtonClicked(self):
        if self.isLowIntensity:
            self.isLowIntensity = False
            self.intensity_button.setText("high intensity")
        else:
            self.isLowIntensity = True
            self.intensity_button.setText("low intensity")

    def triggerPracticeMotor(self, motor_id): # serving function for practice mode
        print("trigger ", motor_id)
        commands = '\n'.join(self.template_commands[motor_id])
        print("commands = \n", commands)
        self.bluetooth_signal.emit(commands)

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