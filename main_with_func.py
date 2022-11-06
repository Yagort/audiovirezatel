# -*- coding: utf-8 -*-
from PyQt6 import uic
from PyQt6.QtCore import QTime
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from moviepy.editor import *


Form, Window = uic.loadUiType("krasava.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


# Нажатие на кнопку -Проводник
def get_video_local():
    global PervDirName, name_for_save, end_time, dir_for_save
    form.label.clear()
    form.label_for_image.clear()
    try:
        # Открываем файл и заполняем поле, путем для файла
        #PervDirName = QFileDialog.getOpenFileName(directory='B:\musica')  # Для моей машины
        PervDirName = QFileDialog.getOpenFileName()
        PervDirName = PervDirName[0]
        form.line_for_getvideoinlocal.setText(PervDirName)

        # Вытаскиваем имя файла и расположение из пути к файлу
        dir_for_save = PervDirName[:-4]  # Убираю расширение мп3
        dir_for_save = dir_for_save.split("/")  # Разбиваю по символу /
        name_for_save = dir_for_save[-1]  # Сохраняю название
        peremennaya = ''
        for papki in dir_for_save[:-1]:
            peremennaya += papki + '/'
        dir_for_save = peremennaya[:-1]  # Сохраняю путь

        # Cразу запихиваю в поле для сохранения пути
        form.line_for_save.setText(f'{dir_for_save}/{name_for_save}')

        # расчет длительности трека в секундах
        content = AudioFileClip(PervDirName)
        duration = content.duration
        content.reader.close_proc()

        # Устанавливаем время конца трека с помощью вызова функции конвертации времени
        end_time[0], end_time[1] = convert_time(duration)
        # print(end_time)

        # выставлям значение начала трека, по умолчанию =0
        form.timeEdit_nach.setMaximumTime(QTime(end_time[0], end_time[1]))
        form.timeEdit_nach.setTime(QTime(00, 00))

        # выставлям значение конца трека, по умолчанию = конец трека
        form.timeEdit_konca.setMaximumTime(QTime(end_time[0], end_time[1]))
        form.timeEdit_konca.setTime(QTime(end_time[0], end_time[1]))

    except:
        pass


# Если пользуемся редактором времени для начала трека
def tnach():
    global start_time
    # Берем цыфры из виджета timeEdit_nach
    nachalo = form.timeEdit_nach.time().toString('hh-mm')
    nachalo = nachalo.split("-")

    # Переопределем наши переменные
    start_time[0] = int(nachalo[0])
    start_time[1] = int(nachalo[1][:2])


# Если пользуемся редактором времени для конца трека
def tkon():
    global end_time
    # Берем цыфры из виджета timeEdit_konca
    konec = form.timeEdit_konca.time().toString('hh-mm')
    konec = konec.split("-")

    # Переопределем наши переменные
    end_time[0] = int(konec[0])
    end_time[1] = int(konec[1][:2])


# Функция конвертации трека
def convertation():
    global PervDirName, dir_for_save, name_for_save, start_time, end_time
    # Берем фрагмент из нашего видео\аудиофайла по нашем таймерам.
    audioclip = AudioFileClip(f'{PervDirName}').subclip(t_start=(start_time[0], start_time[1]),
                                                       t_end=(end_time[0], end_time[1]))

    # Сохраняем аудиодорогу из нашего видео\аудиофайла.
    audioclip.write_audiofile(f'{dir_for_save}/{name_for_save}-кекee.mp3', buffersize=2000)

    #Предупреждение о завершении
    form.label.setText("Готово, проверяй")
    form.label_for_image.setPixmap(pixmap)

    # Все к первоначальному виду
    form.line_for_getvideoinlocal.setText("откуда берем файл")
    form.line_for_save.setText("куда сохраняем")
    start_time, end_time = [0, 0], [0, 0]
    form.timeEdit_nach.setMaximumTime(QTime(end_time[0], end_time[1]))
    form.timeEdit_konca.setMaximumTime(QTime(end_time[0], end_time[1]))


# Нажатие на кнопку - Выбрать путь для сохранения
def save_in_pc():
    global dir_for_save, name_for_save

    # Заменяю папку для сохранения из той что выбрана пользователем
    dir_for_save = QFileDialog.getExistingDirectory()
    if dir_for_save != "":
        form.line_for_save.setText(f'{dir_for_save}/{name_for_save}')
    else:
        pass


# Функция конвертирования времени из секунд- в минуты и секунды
def convert_time(duration):
    duration = duration % (24 * 3600)
    duration %= 3600
    min = duration // 60
    min = int(min)
    sec = duration % 60
    sec = int(sec)
    return min, sec

# При наведении курсора на поле для ввода пути сохранения.Для ручного изменении пути и имени
def hand_edit():
    #msg()11111111111111111111111111111111111
    global dir_for_save, name_for_save
    stroka = form.line_for_save.text()

    stroka = stroka.split("/")
    name_for_save = stroka[-1]

    peremennaya = ''
    for papki in stroka[:-1]:
        peremennaya += papki + '/'
    dir_for_save = peremennaya[:-1]

#def msg():111111111111111111111111111111111
#    dialog = QMessageBox()  # .setText("Проверьте правильность ссылки!")
#    dialog.setText("This is a message box")
#    dialog.setInformativeText("This is additional information")
#    dialog.setWindowTitle("MessageBox demo")
#    dialog.setDetailedText("The details are as follows:")

pixmap = QPixmap('imag/husqvarna_130_1.5kvt_2.0_l.s._x_torq_14_3_8_mini_h37_1.3mm__1147262_1.jpg')
name_for_save = ''
PervDirName = ''
dir_for_save = ''

start_time = [0, 0]
end_time = [0, 0]

form.pushButton.clicked.connect(get_video_local)  # Нажатие на кнопку -Проводник
form.Button_for_convertation.clicked.connect(convertation)  # Нажатие на кнопку -Конвертировать
form.timeEdit_nach.timeChanged.connect(tnach)  # Нажатие на смену времени
form.timeEdit_konca.timeChanged.connect(tkon)  # Нажатие на смену времени
form.Button_for_save.clicked.connect(save_in_pc)  # Нажатие на кнопку Выбрать
form.line_for_save.cursorPositionChanged.connect(hand_edit)  # Нажатие на поле сохранения

app.exec()
