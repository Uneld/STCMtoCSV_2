from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

import threading
import json
import os


def parse_stcm_file(filepath):
    st.insert(END, "Считывание файла stcm...\n")  # Вставляем сообщение, указывающее на чтение файла stcm

    with open(filepath, 'r') as file_in:  # Открываем файл stcm
        data_string = file_in.read()  # Читаем содержимое файла

    if data_string[-3] == ",":  # Проверяем, является ли последний символ запятой
        data_string = data_string[:-3] + data_string[-2:]  # Удаляем последнюю запятую, если она есть

    data = json.loads(data_string)  # Разбираем JSON-данные из файла
    st.insert(END, "Данные загружены.\n")  # Вставляем сообщение, указывающее на загрузку данных

    list_group_name = []  # Список для хранения названий групп
    group_var_names = []  # Список для хранения названий переменных для каждой группы
    list_column_groups = []  # Список для хранения данных переменных для каждой группы

    # Перебираем каждый элемент в данных
    for item in data:
        group_name = item['groupname']  # Получаем название группы
        variable_name = item['variablename']  # Получаем название переменной
        variable_data = item['variabledata']  # Получаем данные переменной

        # Проверяем, есть ли уже такое название группы в списке
        if group_name not in list_group_name:
            # Добавляем название группы в список
            list_group_name.append(group_name)
            # Добавляем пустой список для хранения названий переменных для этой группы
            group_var_names.append([])
            # Добавляем пустой список для хранения данных переменных для этой группы
            list_column_groups.append([])

            # Получаем индекс названия группы в списке
        index_group = list_group_name.index(group_name)

        # Проверяем, есть ли уже такое название переменной в списке для этой группы
        if variable_name not in group_var_names[index_group]:
            # Добавляем название переменной в список для этой группы
            group_var_names[index_group].append(variable_name)
            # Добавляем пустой список для хранения данных переменной для этого названия переменной в этой группе
            list_column_groups[index_group].append([])

        # Получаем индекс названия переменной в списке для этой группы
        index = group_var_names[index_group].index(
            variable_name)

        # Добавляем данные переменной в список данных для этого названия переменной в этой группе
        list_column_groups[index_group][index].extend(variable_data)

        # Вставляем сообщение, указывающее на успешное разбиение файла stcm
    st.insert(END, "Файл .stcm распарсен.\n")

    find_log_substr = filepath.find("Log_")  # Находим подстроку "Log_" в пути к файлу
    log_substr = filepath[find_log_substr:]  # Получаем подстроку, начиная с "Log_"

    # Находим последнее вхождение "/" в пути к файлу
    find_start_filename_substr = filepath.rfind("/")
    # Получаем путь к директории и заменяем "/" на "\\"
    filepath_out = filepath[:find_start_filename_substr].replace("/", "\\")

    # Проверяем, найдена ли "Log_" и длина подстроки больше 26
    if find_log_substr > 0 and len(log_substr) > 26:
        # Находим позицию второго "_" в подстроке
        pos = log_substr.find('_', log_substr.find('_') + 1)
        # Получаем название директории из подстроки
        dir_name = log_substr[pos + 1: -5]
    else:
        # Устанавливаем название директории по умолчанию как "Converted"
        dir_name = "Converted"

        # Создаем полный путь к директории
    dir_name = f"{filepath_out}\\{dir_name}"
    # Проверяем, не существует ли уже такая директория
    if not os.path.isdir(dir_name):
        # Создаем директорию
        os.mkdir(dir_name)

    len_group_name = len(list_group_name)  # Получаем длину списка названий групп

    max_len_name_groups = 0  # Переменная для хранения максимальной длины названий групп
    step_text = 0  # Переменная для хранения шага обновления текста прогресса

    # Перебираем каждую группу
    for g in range(len_group_name):
        # Получаем название группы
        name_group = list_group_name[g]
        # Создаем сообщение о записи группы
        group_text = f"Запись группы {name_group}."

        # Создаем путь к директории для этой группы
        dir_group_name = f"{dir_name}\\{name_group.strip().replace(',', '_').replace('.', '_')}"
        # Проверяем, не существует ли уже такая директория
        if not os.path.isdir(dir_group_name):
            # Создаем директорию
            os.mkdir(dir_group_name)

        if max_len_name_groups < len(group_text):  # Проверяем, больше ли длина текста группы максимальной длины
            max_len_name_groups = len(group_text)  # Обновляем максимальную длину

        # Вычисляем шаг обновления текста прогресса
        step_text = 4 + g * 2
        # Заменяем текст прогресса на текст группы
        st.replace(f"{step_text}.0", f"{step_text}.{max_len_name_groups}", group_text)
        # Вставляем новую строку
        st.insert(END, "\n")

        len_variable_name = len(group_var_names[g])  # Получаем длину списка названий переменных для этой группы
        step = 100 / len_variable_name  # Вычисляем шаг обновления прогресс-бара
        counter_load = 0  # Переменная для хранения процента выполнения
        load_string = ""  # Переменная для хранения строки прогресс-бара

        for i in range(len_variable_name):  # Перебираем каждое название переменной в этой группе
            counter_load += step  # Обновляем процент выполнения
            if counter_load > 100:  # Проверяем, превышает ли процент выполнения 100
                counter_load = 100  # Устанавливаем процент выполнения равным 100

            load_string += "##"  # Добавляем символы прогресс-бара
            step_text = 5 + g * 2  # Вычисляем шаг обновления текста прогресс-бара
            st.replace(f"{step_text}.0", f"{step_text}.30",
                       f"{round(counter_load)}% {load_string}")  # Заменяем текст прогресс-бара
            st.insert(END, "\n")  # Вставляем новую строку

            file_name = group_var_names[g][i].replace(".", "_").replace(":", "_").strip()  # Создаем название файла для этой переменной
            with open(f'{dir_group_name}\\{file_name}.csv', 'w') as file_out:  # Открываем файл для записи
                file_out.write(f"Time; {group_var_names[g][i]} \n")  # Записываем заголовок
                for item in list_column_groups[g][i]:  # Перебираем каждый элемент в данных переменной
                    time = item['x']  # Получаем значение времени
                    val = item['y']  # Получаем значение
                    string_out = f"{time};{val}\n"  # Создаем строку для записи в файл
                    file_out.write(string_out)  # Записываем строку в файл

    st.delete(f"{step_text + 1}.0", END)  # Удаляем текст прогресс-бара
    st.insert(END, "\nКонвертация завершена!")  # Вставляем сообщение, указывающее на завершение конвертации


def open_file():
    st.delete("1.0", END)
    filepath = filedialog.askopenfilename()
    if filepath != "" and filepath.rfind(".stcm") > 0:
        threading.Thread(target=parse_stcm_file, args=(filepath,)).start()
    else:
        st.insert(END, "Не верный путь или не верный формат файла\n")


root = Tk()
root.title("GRF")
root.geometry("360x300")

root.grid_rowconfigure(index=0, weight=1)
root.grid_rowconfigure(index=1, weight=2)
root.grid_columnconfigure(index=0, weight=1)

open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=0, sticky=NSEW, padx=4)

st = ScrolledText(root, width=50, height=10)
st.grid(column=0, row=1, sticky=NSEW, padx=10)

root.mainloop()
