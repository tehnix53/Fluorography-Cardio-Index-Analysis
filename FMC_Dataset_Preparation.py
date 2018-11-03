# 0. ИМПОРТИРУЕМЫЕ МОДУЛИ

import os
import shutil
import xlrd as x

# 1. КОПИРОВАНИЕ ИССЛЕДОВАНИЙ ОБОИХ КЛАССОВ ИЗ БАЗЫ

# 1.1 Создание каталогов для копирования

# Каталог для копирования оригинальных файлов
dir2 = '/home/alex/fluro/pat_raw'
dir5 = '/home/alex/fluro/norm_raw'
# Таблицы с разметкой (норма и патология)
dir1 = '/home/alex/fluro/diag2.xlsx'
dir4 = '/home/alex/fluro/diag1.xlsx'
# База данных
dir3 = '/media/alex/TOSHIBA EXT/2016'
os.makedirs(dir2)
os.makedirs(dir5)

# 1.2 Считывание из таблицы колличества строк = число исследований

read_pat = x.open_workbook(dir1)
read_norm = x.open_workbook(dir4)

end_norm = 0
for sheet in read_norm.sheets():
    end_norm += sheet.nrows
print(end_norm)

end_pat = 0
for sheet in read_pat.sheets():
    end_pat += sheet.nrows
print(end_pat)

# 1.3 Создание списка с номерами исследований, соответствующих обоим классам

sheet_norm = x.open_workbook(dir4).sheet_by_index(0)
diag_list_norm = []
for numbers in range(0, end_norm):
    diag_list_norm.append(sheet_norm.row_values(numbers)[0])

sheet_pat = x.open_workbook(dir1).sheet_by_index(0)
diag_list_pat = []
for numbers in range(0, end_pat):
    diag_list_pat.append(sheet_pat.row_values(numbers)[0])

# 1.4 Копирование DICOM файлов обоих классов в соответствующие каталоги

for root, dirs, files in os.walk(dir3):
    for file in files:
        for element in diag_list_norm:
            if file.startswith(element[2:10]) and file.endswith(".dcm"):

                shutil.copy(os.path.join(root, file), dir5)
                print(os.path.join(root, file))
            else:
                pass

for root,dirs,files in os.walk(dir3):
    for file in files:
        for element in diag_list_pat:
            if file.startswith(element[2:10]) and file.endswith(".dcm"):

                shutil.copy(os.path.join(root, file), dir2)
                print(os.path.join(root, file))
            else:
                pass

# 2. СОЗДАНИЕ КАТАЛОГОВ С ПРОНУМЕРОВАННЫМИ ФАЙЛАМИ

# 2.1 Копирование файлов в новую папку

folder1 = '/home/alex/fluro/norm_raw'
folder2 = '/home/alex/fluro/norm'
folder3 = '/home/alex/fluro/pat_raw'
folder4 = '/home/alex/fluro/pat'

shutil.copytree(folder1,folder2)
shutil.copytree(folder3,folder4)

# 2.2 Переименовывание всех файлов из folder2, folder4 в нумерованные

files = os.listdir(folder2)
for i, filename in enumerate(os.listdir(folder2)):
    os.chdir(folder2)
    os.rename(filename, 'norm.{0}.dcm'.format(i+1))

files = os.listdir(folder4)
for i, filename in enumerate(os.listdir(folder4)):
    os.chdir(folder4)
    os.rename(filename, 'pat.{0}.dcm'.format(i + 1))

# 3. ПОДГОТОВКА ДАТАСЕТА. РАСПРЕДЕЛЕНИЕ В КАТАЛОГИ Val. Test. Train

# 3.1 Основные переменные
# Каталог с данными для обучения
train_dir = '/home/alex/fluro/train'
# Каталог с данными для проверки
val_dir = '/home/alex/fluro/val'
# Каталог с данными для тестирования
test_dir = '/home/alex/fluro/test'
# Часть набора данных для тестирования
test_data_portion = 0.15
# Часть набора данных для проверки
val_data_portion = 0.15
# Количество элементов данных в одном классе

# 3.2 Подсчитываем количество снимков с нормой
list1 = os.listdir(folder2)
nb_norm = len(list1)
# 3.3 Подсчитываем количество снимков с паталогией
list2 = os.listdir(folder4)
nb_pat = len(list2)


# 3.4 Создание каталогов и подкаталогов

def create_directory(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    os.makedirs(os.path.join(dir_name, "norms"))
    os.makedirs(os.path.join(dir_name, "pats"))

create_directory(train_dir)
create_directory(val_dir)
create_directory(test_dir)


# 3.5 Заполнение каталогов по классу "НОРМА"

def copy_norm(start_index, end_index, source_dir, dest_dir):
    for i in range(start_index, end_index):
        print(dest_dir)
        print(i)
        shutil.copy2(os.path.join(source_dir, "norm." + str(i) + ".dcm"),
                    os.path.join(dest_dir, "norms"))

start_val_data_idx_norm = int(nb_norm * (1 - val_data_portion - test_data_portion))
start_test_data_idx_norm = int(nb_norm * (1 - test_data_portion))
print(start_val_data_idx_norm)
print(start_test_data_idx_norm)
print(nb_norm)

copy_norm(1, start_val_data_idx_norm, folder2, train_dir)
copy_norm(start_val_data_idx_norm, start_test_data_idx_norm, folder2, val_dir)
copy_norm(start_test_data_idx_norm, nb_norm, folder2, test_dir)

# 3.6 Заполнение каталогов по классу "ПАТОЛОГИЯ"

def copy_pat(start_index, end_index, source_dir, dest_dir):
    for i in range(start_index, end_index):
        print(dest_dir)
        print(i)

        shutil.copy2(os.path.join(source_dir, "pat." + str(i) + ".dcm"),
                   os.path.join(dest_dir, "pats"))

start_val_data_idx_pat = int(nb_pat * (1 - val_data_portion - test_data_portion))
start_test_data_idx_pat = int(nb_pat * (1 - test_data_portion))
print(start_val_data_idx_pat)
print(start_test_data_idx_pat)

copy_pat(1, start_val_data_idx_pat, folder4, train_dir)
copy_pat(start_val_data_idx_pat, start_test_data_idx_pat, folder4, val_dir)
copy_pat(start_test_data_idx_pat, nb_pat, folder4, test_dir)












