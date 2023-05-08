import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QRect

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем сцену и вид
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Загружаем изображение и добавляем его на сцену
        self.pixmap = QPixmap("example.jpg")
        self.scene.addPixmap(self.pixmap)

        # Создаем кнопку и добавляем ее на сцену
        self.button = QPushButton("Save", self)
        self.button.move(10, 10)
        self.button.clicked.connect(self.save_image)
        self.scene.addWidget(self.button)

        # Создаем лэйбл и добавляем его на сцену
        self.label = QLabel("Label", self)
        self.label.move(10, 40)
        self.scene.addWidget(self.label)

    def save_image(self):
        # Открываем диалог сохранения файла
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg)")

        if file_name:
            # Получаем область изображения на сцене
            rect = self.view.viewport().rect()

            # Создаем painter для сохранения области
            painter = QPainter()
            painter.begin(self.pixmap)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))

            # Отрисовываем красную линию на изображении
            painter.drawLine(QPoint(0, 0), QPoint(100, 100))

            # Получаем область, которую нужно сохранить
            cropped = self.pixmap.copy(rect)

            # Сохраняем область в файл
            cropped.save(file_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageEditor()
    ex.show()
    sys.exit(app.exec_())
