import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
import requests as req


class ZoomButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(ZoomButton, self).__init__(*args, **kwargs)
        self._rect = None
        self._geometry = None
        self._animation = QPropertyAnimation(self, b'geometry', duration=150)

    def update_pos(self):
        self._geometry = self.geometry()
        self._rect = QRect(
            self._geometry.x() - 2,
            self._geometry.y() - 2,
            self._geometry.width() + 4,
            self._geometry.height() + 4
        )

    def showEvent(self, event):
        super(ZoomButton, self).showEvent(event)
        self.update_pos()

    def enterEvent(self, event):
        super(ZoomButton, self).enterEvent(event)
        self._animation.stop()

        self._animation.setStartValue(self._geometry)

        self._animation.setEndValue(self._rect)
        self._animation.start()

    def leaveEvent(self, event):
        super(ZoomButton, self).leaveEvent(event)
        self._animation.stop()
        self._animation.setStartValue(self._rect)
        self._animation.setEndValue(self._geometry)
        self._animation.start()

    def mousePressEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._rect)
        self._animation.setEndValue(self._geometry)
        self._animation.start()
        super(ZoomButton, self).mousePressEvent(event)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WeatherApp')
        self.setFixedSize(500, 700)
        self.setStyleSheet("background-color: rgb(27, 32, 39);")
        self.setWindowFlags(Qt.FramelessWindowHint)


        #Input городов
        self.line = QLineEdit(self)
        self.line.setAlignment(Qt.AlignCenter)
        self.line.resize(270, 45)
        self.line.move(45, 45)
        self.line.setStyleSheet('''
                border-radius: 4px;
                border-width: 3px;
                border-color: rgb(36, 42, 52);
                background-color: rgb(36, 42, 52);
                border-style: solid;
                color: rgb(210, 210, 210);''')
        self.line.setFont(QtGui.QFont('Cascadia Mono Semibold', 13, QtGui.QFont.Bold))

        #Кнопка поиска погоды
        self.btn1 = ZoomButton('УЗНАТЬ', self)
        self.btn1.resize(100, 45)
        self.btn1.move(325, 45)
        self.btn1.setStyleSheet('''
                        border-radius: 4px;
                        color: rgb(210, 210, 210);
                        background-color: rgb(52, 121, 214);
                        border-style: solid;''')

        self.btn1.setFont(QtGui.QFont("Cascadia Mono Semibold", 11, QtGui.QFont.Bold))

        #Кнопка выйти
        self.close_btn = ZoomButton(self)
        self.close_btn.resize(20, 45)
        self.close_btn.move(435, 45)
        self.close_btn.setStyleSheet('''
                                        border-radius: 4px;
                                        color: rgb(86, 92, 102);
                                        background-color: rgb(199, 84, 80);
                                        border-style: solid;''')



        #Основной заголовок названия города
        self.text_weather_in_city = QLabel('Введите Город', self)
        self.text_weather_in_city.setAlignment(Qt.AlignCenter)
        self.text_weather_in_city.setFont(QtGui.QFont("Segou UI Black", 10, QtGui.QFont.Bold))
        self.text_weather_in_city.setStyleSheet('color: rgb(95, 104, 118);')
        self.text_weather_in_city.resize(300, 20)
        self.text_weather_in_city.move(100, 10)

        #Описание погода
        self.text_description = QLabel(self)
        self.text_description.setAlignment(Qt.AlignCenter)
        self.text_description.setFont(QtGui.QFont("Segou UI Black", 15, QtGui.QFont.Bold))
        self.text_description.setStyleSheet('color: rgb(95, 104, 118);')
        self.text_description.resize(480, 40)
        self.text_description.move(0, 170)

        self.label = QLabel(self)
        self.label.resize(20, 20)
        self.label.hide()

        #Атмосферное давление
        self.text_pressure = QLabel(self)
        self.text_pressure.setAlignment(Qt.AlignCenter)
        self.text_pressure.setFont(QtGui.QFont("Segou UI Black", 15, QtGui.QFont.Bold))
        self.text_pressure.setStyleSheet('color: rgb(95, 104, 118);')
        self.text_pressure.resize(500, 40)
        self.text_pressure.move(0, 400)

        #Погода по цельсию
        self.text_temp = QLabel(self)
        self.text_temp.setAlignment(Qt.AlignCenter)
        self.text_temp.setFont(QtGui.QFont("Segou UI Black", 30, QtGui.QFont.Bold))
        self.text_temp.setStyleSheet('color: rgb(52, 121, 214)  ;')
        self.text_temp.resize(500, 55)
        self.text_temp.move(0, 250)

        #Погода по ощущению
        self.text_temp_likes = QLabel(self)
        self.text_temp_likes.setAlignment(Qt.AlignCenter)
        self.text_temp_likes.setFont(QtGui.QFont("Segou UI Black", 20, QtGui.QFont.Bold))
        self.text_temp_likes.setStyleSheet('color: rgb(210, 210, 210);')
        self.text_temp_likes.resize(500, 70)
        self.text_temp_likes.move(0, 325)

        #Основная иконка
        self.main_label_image = QLabel(self)
        main_image = QPixmap('icon')
        self.main_label_image.setAlignment(Qt.AlignCenter)
        self.main_label_image.resize(128, 128)
        self.main_label_image.move(175, 285)
        self.main_label_image.setPixmap(main_image)

        #Приветсвующий текст
        self.main_text = QLabel('Интересно, какая сегодня погода?', self)
        self.main_text.setAlignment(Qt.AlignCenter)
        self.main_text.setFont(QtGui.QFont("Segou UI Black", 13, QtGui.QFont.Bold))
        self.main_text.setStyleSheet('color: rgb(160, 170, 180)  ;')
        self.main_text.move(0, 430)
        self.main_text.resize(500, 25)

        #Дополнительная часть
        self.background = QPushButton(self)
        self.background.resize(430, 200)
        self.background.move(35, 470)
        self.background.setStyleSheet('''
                        border-radius: 10px;
                        border-width: 3px;
                        border-color: rgb(36, 42, 52);
                        background-color: rgb(36, 42, 52);
                        border-style: solid;
                        color: rgb(210, 210, 210);''')
        self.background.hide()

        # Парсинг данных о погоде
        def pressed_get():
            self.background.show()
            self.main_label_image.hide()
            self.main_text.hide()
            city = self.line.text()
            print(city)

            response = req.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'q': city, 'lang': 'ru', 'units': 'metric',
                                       'APPID': "9d0864cfefebb1ec3592e7379f7776af"})
            weather = response.json()
            if "message" in weather.keys():
                try:
                    if weather["cod"] == "404":
                        self.text_weather_in_city.setText("Вы ввели неверный город")

                    elif weather["cod"] == "400":
                        self.text_weather_in_city.setText("Вы не ввели город")

                    elif weather["cod"] == "429":
                        self.text_weather_in_city.setText("Ошибка приложения")

                    else:
                        self.text_weather_in_city.setText("Глобальная ошибка сервера")

                    self.text_temp.setText("--° C")
                    self.text_temp.show()
                    self.text_temp_likes.setText("По ощущениям --° C")
                    self.text_temp_likes.show()
                    self.text_description.setText("------------")
                    self.text_description.show()
                    self.text_pressure.setText("Атмосферное д. --- мм.рт.ст")
                    self.text_pressure.show()

                except KeyError:
                    self.text_weather_in_city.setText("Ошибка приложения")
                    self.text_temp.hide()
                    self.text_description.hide()
                    self.label.hide()
                    self.text_temp_likes.hide()
                    self.text_pressure.hide()

            else:
                try:
                    self.text_weather_in_city.setText("Погода " + str(weather["name"]))
                except KeyError:
                    self.text_weather_in_city.setText("Погода неизвестна")
                finally:
                    self.text_weather_in_city.show()

                try:
                    self.text_temp.setText(str(weather["main"]["temp"]) + "° C")
                except KeyError:
                    self.text_temp.setText("--° C")
                finally:
                    self.text_temp.show()

                try:
                    self.text_temp_likes.setText("По ощущениям " + str(weather["main"]["feels_like"]) + "° C")
                except KeyError:
                    self.text_temp_likes.setText("По ощущениям --° C")
                finally:
                    self.text_temp_likes.show()

                try:
                    print(weather)
                    pixmap = QPixmap('')
                    if 'пасмурно' == weather["weather"][0]["description"]:
                        pixmap = QPixmap('04d.png')
                        self.label.move(315, 181)
                        self.label.show()
                    elif "ясно" == weather["weather"][0]["description"]:
                        pixmap = QPixmap('01d.png')
                        self.label.move(277, 181)
                        self.label.show()
                    elif 'переменная облачность' == weather["weather"][0]["description"]:
                        pixmap = QPixmap('02n.png')
                        self.label.move(405, 181)
                    elif 'небольшая облачность' == weather["weather"][0]["description"]:
                        pixmap = QPixmap('02d.png')
                        self.label.move(397, 181)
                        self.label.show()
                    elif 'небольшой снег' == weather["weather"][0]["description"]:
                        pixmap = QPixmap('13d.png')
                        self.label.move(355, 181)
                        self.label.show()
                    elif 'дождь' == weather["weather"][0]["description"]:
                        pixmap = QPixmap('10n.png')
                        self.label.move(295, 181)
                        self.label.show()
                    elif 'небольшой дождь' == weather["weather"][0]["description"]:
                        pixmap = QPixmap('10n.png')
                        self.label.move(365, 181)
                        self.label.show()
                    else:
                        self.label.hide()
                    self.label.setPixmap(pixmap)

                    self.text_description.setText(weather["weather"][0]["description"])
                except KeyError:
                    self.text_description.setText("------------")
                finally:
                    self.text_description.show()

                try:
                    self.text_pressure.setText(
                        "Атмосферное д. " + str(round(weather["main"]["pressure"] * 0.75)) + " мм.рт.ст")
                except KeyError:
                    self.text_pressure.setText("Атмосферное д. --- мм.рт.ст")
                finally:
                    self.text_pressure.show()

        #Закрытие программы
        def close_func():
            QApplication.quit()

        #Всплывающее окно
        def show_message():
            self.msgBox = QMessageBox()
            self.msgBox.setWindowFlags(Qt.FramelessWindowHint)
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.move(800, 600)
            self.msgBox.setText("Вам понравилось приложение?")
            self.msgBox.setStyleSheet('''
                            border-radius: 4px;
                            border-width: 3px;
                            border-color: rgb(36, 42, 52);
                            background-color: rgb(36, 42, 52);
                            border-style: solid;
                            color: rgb(52, 121, 214);''')

            self.btn_msg = QPushButton(self.msgBox)
            self.btn_msg.resize(100, 30)
            self.btn_msg.setStyleSheet('''
                            border-radius: 6px;
                            border-width: 2px;
                            border-color: rgb(199, 84, 80);
                            background-color: rgb(199, 84, 80);
                            border-style: solid;
                            color: rgb(230, 230, 230);''')
            self.btn_msg.setText('Нет')
            self.btn_msg.move(215, 70)

            self.btn_msg1 = ZoomButton(self.msgBox)
            self.btn_msg1.resize(190, 30)
            self.btn_msg1.setStyleSheet('''
                            border-radius: 6px;
                            border-width: 2px;
                            border-color: rgb(75, 168, 89);
                            background-color: rgb(75, 168, 89);
                            border-style: solid;
                            color: rgb(230, 230, 230);''')
            self.btn_msg1.setText('Да')
            self.btn_msg1.move(15, 70)
            self.btn_msg1.clicked.connect(close_func)
            returnValue = self.msgBox.exec()

        self.btn1.clicked.connect(pressed_get)
        self.close_btn.clicked.connect(show_message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
