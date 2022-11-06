# -*- coding: utf-8 -*-
import sys
import os
#from moviepy.editor import *
from PyQt6.QtCore import QTime, QSize
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from moviepy.audio.io.AudioFileClip import AudioFileClip#благодаря обращению пайинсталлер корректно наследует библеотку

from krasava import Ui_MainWindow  # импорт графического интерфейса из файла
######## Логика программы ######
class AudioRedactorWindow(QtWidgets.QMainWindow):

    # Конструктор класса
    def __init__(self):

        #Наследуемся от родительского класса QMainWindow
        super(AudioRedactorWindow, self).__init__()

        # Атрибуты для правильного переписывания в последующем
        self.finishImg = QPixmap('imag\husqvarna.jpg')
        self.logoimg = QIcon("imag\logo.jpg")
        self.PervDirName = ""
        self.dir_for_save = ""
        self.name_for_save = ""
        self.start_time = [0, 0, 0]
        self.end_time = [0, 0, 0]


        # Связываем класс AudioRedactorWindow и класс ГИ из файла красава
        self.ui = Ui_MainWindow()  # графический интерфейс из файла красава
        self.ui.setupUi(self)
        self.init_UI()  # дает изменения в окно


        # Связываю кнопки и функции
        self.ui.pushButton.clicked.connect(self.get_video_local)  # Нажатие на кнопку -Проводник
        self.ui.Button_for_convertation.clicked.connect(self.convertation)  # Нажатие на кнопку -Конвертировать
        self.ui.timeEdit_nach.timeChanged.connect(self.tnach)  # Нажатие на смену времени
        self.ui.timeEdit_konca.timeChanged.connect(self.tkon)  # Нажатие на смену времени
        self.ui.Button_for_save.clicked.connect(self.save_in_pc)  # Нажатие на кнопку Выбрать
        self.ui.line_for_save.cursorPositionChanged.connect(self.hand_edit)  # Нажатие на поле сохранения

    # Конструктор для ГИ из класса AudioRedactorWindow
    def init_UI(self):
        self.setWindowIcon(self.logoimg)
        self.ui.line_for_getvideoinlocal.setPlaceholderText("укажи файл")
        self.ui.line_for_save.setPlaceholderText("укажи папку для сохранения")

        self.ui.timeEdit_nach.setDisplayFormat("HH:mm:ss")
        self.ui.timeEdit_konca.setDisplayFormat("HH:mm:ss")

    # Нажатие на кнопку -Проводник
    def get_video_local(self):
        self.ui.label.clear()
        self.ui.label_for_image.clear()
        try:
            # Открываем файл и заполняем поле, путем для файла
            self.PervDirName = QFileDialog.getOpenFileName(directory='B:\musica')  # Для моей машины
            #self.PervDirName = QFileDialog.getOpenFileName()
            self.PervDirName = self.PervDirName[0]
            self.ui.line_for_getvideoinlocal.setText(self.PervDirName)

            # Вытаскиваем имя файла и расположение из пути к файлу
            self.dir_for_save = self.PervDirName[:-4]  # Убираю расширение мп3
            self.dir_for_save = self.dir_for_save.split("/")  # Разбиваю по символу /
            self.name_for_save = self.dir_for_save[-1]  # Сохраняю название
            peremennaya = ''
            for papki in self.dir_for_save[:-1]:
                peremennaya += papki + '/'
            # self.dir_for_save = peremennaya[:-1]  # Сохраняю путь
            self.dir_for_save = peremennaya  # Сохраняю путь

            # Cразу запихиваю в поле для сохранения пути
            self.ui.line_for_save.setText(f'{self.dir_for_save}{self.name_for_save}')

            # расчет длительности трека в секундах и закрытие видео файла
            content = AudioFileClip(self.PervDirName)
            duration = content.duration
            content.reader.close_proc()

            # Устанавливаем время конца трека с помощью вызова функции конвертации времени
            self.end_time[0], self.end_time[1], self.end_time[2] = self.convert_time(duration)

            # выставлям значение начала трека, по умолчанию =0
            self.ui.timeEdit_nach.setMaximumTime(QTime(self.end_time[0], self.end_time[1], self.end_time[2]))
            self.ui.timeEdit_nach.setTime(QTime(00, 00, 00))

            # выставлям значение конца трека, по умолчанию = конец трека
            self.ui.timeEdit_konca.setMaximumTime(QTime(self.end_time[0], self.end_time[1], self.end_time[2]))
            self.ui.timeEdit_konca.setTime(QTime(self.end_time[0], self.end_time[1], self.end_time[2]))
        except:
            pass

    # Нажатие на кнопку - Выбрать путь для сохранения
    def save_in_pc(self):
        # Заменяю папку для сохранения из той что выбрана пользователем
        self.dir_for_save = QFileDialog.getExistingDirectory()
        if self.dir_for_save != "":
            self.dir_for_save += "/"
            self.ui.line_for_save.setText(f'{self.dir_for_save}{self.name_for_save}')
        else:
            pass

    # Функция конвертирования времени из секунд- в минуты и секунды
    def convert_time(self, duration):
        duration = duration % (24 * 3600)
        hour = duration // 3600
        hour = int(hour)
        duration %= 3600
        min = duration // 60
        min = int(min)
        sec = duration % 60
        sec = int(sec)
        return hour, min, sec

    # Если пользуемся редактором времени для начала трека
    def tnach(self):
        # Берем цифры из виджета timeEdit_nach
        nachalo = self.ui.timeEdit_nach.time().toString('hh-mm-ss')
        nachalo = nachalo.split("-")

        # Переопределем наши переменные
        self.start_time[0] = int(nachalo[0])
        self.start_time[1] = int(nachalo[1])
        self.start_time[2] = int(nachalo[2])

    # Если пользуемся редактором времени для конца трека
    def tkon(self):
        # Берем цифры из виджета timeEdit_konca
        konec = self.ui.timeEdit_konca.time().toString('hh-mm-ss')
        konec = konec.split("-")

        # Переопределем наши переменные
        self.end_time[0] = int(konec[0])
        self.end_time[1] = int(konec[1])
        self.end_time[2] = int(konec[2])

    # Функция конвертации трека
    def convertation(self):

        if (self.start_time[0]*3600)+(self.start_time[1] * 60) + self.start_time[2] < (self.end_time[0]*3600) +\
                (self.end_time[1] * 60) + self.end_time[2]: #
            # Берем фрагмент из нашего видео\аудиофайла по нашем таймерам.
            audioclip = AudioFileClip(f'{self.PervDirName}').subclip(t_start=(self.start_time[0], self.start_time[1],
                                                                              self.start_time[2]),
                                                                     t_end=(self.end_time[0], self.end_time[1],
                                                                            self.end_time[2]))

            # Сохраняем аудиодорогу из нашего видео\аудиофайла.
            audioclip.write_audiofile(f'{self.dir_for_save}{self.name_for_save}-кек.mp3', buffersize=2000)
            audioclip.reader.close_proc()

            # Предупреждение о завершении
            self.gotovo()
            # self.ui.label.setText("Готово, проверяй")
            # self.ui.label_for_image.setPixmap(self.pixmap)

            # Все к первоначальному виду
            self.ui.line_for_getvideoinlocal.setText("")
            self.ui.line_for_save.setText("")
            self.start_time, self.end_time = [0, 0, 0], [0, 0, 0]
            self.ui.timeEdit_nach.setMaximumTime(QTime(self.start_time[0], self.start_time[1], self.start_time[1]))
            self.ui.timeEdit_konca.setMaximumTime(QTime(self.end_time[0], self.end_time[1], self.end_time[1]))
        else:
            self.msg()

    # Предупреждение об ошибке
    def msg(self):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Внимание!")
        dialog.setText("Ошибка таймингов")
        dialog.setWindowIcon(self.logoimg)
        dialog.setIcon(QMessageBox.Icon.Warning)  # Догружаю стандартную иконку ошибки
        dialog.setInformativeText("<i>Начало трека должно быть раньше его окончания...</i>")
        dialog.setStandardButtons(QMessageBox.StandardButton.Cancel)  # Будет Cancel, вместо Ок
        dialog.setDetailedText(f"У вас трек начинается {self.start_time[0]}:{self.start_time[1]}:{self.start_time[2]}, "
                               f"а заканчивается {self.end_time[0]}:{self.end_time[1]}:{self.end_time[1]}")
        # dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        dialog.exec()

    # Предупреждение о готовности аудио
    def gotovo(self):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Готово!")
        dialog.setIconPixmap(self.finishImg.scaled(QSize(250, 200)))  # подогнал под нужный размер имеющуюся картинку.
        dialog.setWindowIcon(self.logoimg)
        dialog.setInformativeText("<i>Проверяй...</i>")
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        dialog.exec()

    # При наведении курсора на поле для ввода пути сохранения. Для ручного изменении пути и имени
    def hand_edit(self):
        stroka = self.ui.line_for_save.text()
        stroka = stroka.split("/")

        self.name_for_save = stroka[-1]

        peremennaya = ''
        for papki in stroka[:-1]:
            peremennaya += papki + '/'
        # self.dir_for_save = peremennaya[:-1]
        self.dir_for_save = peremennaya



######## Для запуска приложения ######
def main():
    # appa = QtWidgets.QApplication([])
    appa = QtWidgets.QApplication(sys.argv)
    application = AudioRedactorWindow()
    application.show()
    # sys.exit(appa.exec())
    appa.exec()


if __name__ == '__main__':
    main()


