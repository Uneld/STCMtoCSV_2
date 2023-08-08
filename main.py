from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

import threading
import json
import os


def main_func(filepath: str):
    with open(filepath, 'r') as file_in:
        data_string = file_in.read()

    if data_string[-3] == ",":
        data_string = data_string[:-3] + data_string[-2:]

    data = json.loads(data_string)
    st.insert(END, f"Данные загружены.\n")

    list_group_name = []
    listVariableName = []
    listColumnParameters = []
    list_column_groups = []
    count = 0
    tstCount = 0
    group_name = ""

    group_var_names = []
    print("---------------------------------------------------------------")
    for item in data:
        tstCount += 1
        group_name = item['groupname']
        variable_name = item['variablename']
        variable_data = item['variabledata']

        if group_name not in list_group_name:
            list_group_name.append(group_name)
            group_var_names.append([])
            list_column_groups.append([])

        index_group = list_group_name.index(group_name)

        if variable_name not in group_var_names[index_group]:
            group_var_names[index_group].append(variable_name)
            listVariableName.append(variable_name)
            list_column_groups[index_group].append([])

        index = listVariableName.index(variable_name)
        list_column_groups[index_group][index].extend(variable_data)

    for item in group_var_names:
        print(item)

    count_groups = 0
    for item in list_column_groups:
        count_groups += 1
        print(count_groups)
        for jitem in item:
            print(jitem)

    print("---------------------------------------------------------------")
    st.insert(END, f"stcm распарсен.\n")
    # for item in listColumnParameters:
    #     print(item)

    find_log_substr = filepath.find("Log_")
    log_substr = filepath[find_log_substr:]

    print(filepath)
    find_start_filename_substr = filepath.rfind("/")
    print(find_start_filename_substr)
    filepath_out = filepath[:find_start_filename_substr].replace("/", "\\")
    print(filepath_out)

    if find_log_substr > 0 and len(log_substr) > 26:  # _2023-08-03_12h40m47s.stcm длинна
        pos = log_substr.find('_', log_substr.find('_') + 1)
        print(log_substr)
        dir_name = log_substr[pos + 1: -5]
        print(dir_name)
    else:
        dir_name = group_name

    dir_name = f"{filepath_out}\\{dir_name}"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    len_variable_name = len(listVariableName)
    st.insert(END, f"Запись файлов {len_variable_name} шт.\n")
    st.insert(END, f"Запись файлов.\n")

    step = 100 / len_variable_name
    counter_load = 0
    load_string = ""
    for i in range(len_variable_name):
        counter_load += step
        if counter_load > 100:
            counter_load = 100

        st.delete(4.0, 5.0)
        load_string += "##"
        st.insert(END, f"{round(counter_load)}% {load_string}\n")

        file_name = listVariableName[i].replace(".", "_").strip()
    #     with open(f'{dir_name}\\{file_name}.csv', 'w') as file_out:
    #         file_out.write(f"Time; {listVariableName[i]} \n")
    #         # print(listColumnParameters[i])
    #         for item in listColumnParameters[i]:
    #             time = item['x']
    #             val = item['y']
    #             string_out = f"{time};{val}\n"
    #             file_out.write(string_out)
    # st.insert(END, f"Конвертация выполнена успешно\n")


root = Tk()
root.title("GRF")
root.geometry("360x300")

root.grid_rowconfigure(index=0, weight=1)
root.grid_rowconfigure(index=1, weight=2)
root.grid_columnconfigure(index=0, weight=1)


def open_file():
    st.delete("1.0", END)
    filepath = filedialog.askopenfilename()
    print("path: " + filepath)
    if filepath != "" and filepath.rfind(".stcm") > 0:
        threading.Thread(target=main_func, args=(filepath,)).start()
    else:
        st.insert(END, f"Не верный путь или не верный формат файла\n")
        print("Не верный путь или не верный формат файла")


open_button = ttk.Button(text="Открыть файл", command=open_file)
open_button.grid(column=0, row=0, sticky=NSEW, padx=4)

st = ScrolledText(root, width=50, height=10)
st.grid(column=0, row=1, sticky=NSEW, padx=10)

root.mainloop()
