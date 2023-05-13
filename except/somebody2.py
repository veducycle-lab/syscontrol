from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # main window properties
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle('Main')
        
        # add widgets and interface logic here

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()