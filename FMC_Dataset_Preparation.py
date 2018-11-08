# 0. ИМПОРТИРУЕМЫЕ МОДУЛИ

import os
import shutil
import xlrd as x
import png
import pydicom
import numpy as np

# 1. КОПИРОВАНИЕ ИССЛЕДОВАНИЙ ОБОИХ КЛАССОВ ИЗ БАЗЫ

# 1.1 Создание каталогов для копирования

# Каталог для копирования оригинальных файлов
dir2 = '/media/alex/TOSHIBA EXT/fluro/pat_raw'
dir5 = '/media/alex/TOSHIBA EXT/fluro/norm_raw'
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

def count_end_point(diag_list):
    end_tag = 0
    for sheet in diag_list.sheets():
        end_tag += sheet.nrows
    return(end_tag)

end_norm = count_end_point(read_norm)
end_pat = count_end_point(read_pat)

# 1.3 Создание списка с номерами исследований, соответствующих обоим классам

sheet_norm = read_norm.sheet_by_index(0)
sheet_pat = read_pat.sheet_by_index(0)

def make_the_list(diag_sheet, end_tag):
    diag_list = []
    for numbers in range(0, end_tag):
        diag_list.append(diag_sheet.row_values(numbers)[0])
    return(diag_list)

diag_list_norm = make_the_list(sheet_norm,end_norm)
diag_list_pat = make_the_list(sheet_pat,end_pat)

# 1.4 Копирование DICOM файлов обоих классов в соответствующие каталоги

def dicom_replacer(from_dir, diag_list, where_dir)
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            for element in diag_list:
                if file.startswith(element[2:9]) and file.endswith(".dcm"):

                    shutil.copy(os.path.join(root, file), where_dir)
                    print(os.path.join(root, file))
                else:
                    pass

dicom_replacer(dir3,diag_list_norm,dir5)
dicom_replacer(dir3,diag_list_pat,dir2)

# 2. СОЗДАНИЕ КАТАЛОГОВ С ПРОНУМЕРОВАННЫМИ ФАЙЛАМИ

# 2.1 Копирование файлов в новую папку

folder1 = '/media/alex/TOSHIBA EXT/fluro/norm_source'
folder2 = '/media/alex/TOSHIBA EXT/fluro/norm'
folder3 = '/media/alex/TOSHIBA EXT/fluro/pat_source'
folder4 = '/media/alex/TOSHIBA EXT/fluro/pat'

shutil.copytree(folder1,folder2)
shutil.copytree(folder3,folder4)

# 2.2 Переименовывание всех файлов из folder2, folder4 в нумерованные

def dicom_numeration(directory, name):
    for i, filename in enumerate(os.listdir(directory)):
        os.chdir(directory)
        os.rename(filename, name+'.{0}.dcm'.format(i + 1))

dicom_numeration(folder2,'norm')
dicon_numeration(folder4,'pat')

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

# 3.2 Подсчитываем количество снимков с нормой и патологией

nb_norm = len(os.listdir(folder2))
nb_pat = len(os.listdir(folder4))


# 3.3 Создание каталогов и подкаталогов

def create_directory(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)
    os.makedirs(os.path.join(dir_name, "norms"))
    os.makedirs(os.path.join(dir_name, "pats"))

create_directory(train_dir)
create_directory(val_dir)
create_directory(test_dir)

# 3.4 Заполнение каталогов по классу "НОРМА" и "ПАТОЛОГИЯ"

def dicom_devider(start_index, end_index, source_dir, dest_dir, name1, name2):
    for i in range(start_index, end_index):
        print(dest_dir)
        print(i)
        shutil.copy2(os.path.join(source_dir, name1 + "." + str(i) + ".dcm"),
                     os.path.join(dest_dir, name2))

dicom_devider(1, int(nb_norm * (1 - val_data_portion - test_data_portion)), folder2, train_dir, 'norm', 'norms')
dicom_devider(int(nb_norm * (1 - val_data_portion - test_data_portion)), int(nb_norm * (1 - test_data_portion)),
              folder2, val_dir, 'norm', 'norms')
dicom_devider(int(nb_norm * (1 - test_data_portion)), nb_norm, folder2, test_dir, 'norm', 'norms')

dicom_devider(1, int(nb_pat * (1 - val_data_portion - test_data_portion)), folder4, train_dir, 'pat', 'pats')
dicom_devider(int(nb_pat * (1 - val_data_portion - test_data_portion)), int(nb_pat * (1 - test_data_portion)), folder4,
              val_dir, 'pat', 'pats')
dicom_devider(int(nb_pat * (1 - test_data_portion)), nb_norm, folder4, test_dir, 'pat', 'pats')


# 4. Конвертация DICOM в PNG(https://github.com/danishm/mritopng)

def auto_contrast(image):

    hist = histogram(image)
    p5 = shade_at_percentile(hist, .01)
    p95 = shade_at_percentile(hist, .99)
    a = 255.0 / (p95 + p5)
    b = -1.0 * a * p5

    result = (image.image.astype(float) * a) + b
    result = result.clip(0, 255.0)

    return GrayscaleImage(np.uint8(result), image.width, image.height)

class GrayscaleImage(object):

    def __init__(self, image, width, height):
            self.image = image
            self.width = width
            self.height = height

    def __str__(self):
     return '[%dx%d]' % (self.width, self.height)

def dcm_to_png(dcm_file, png_file, do_auto_contrast=False):
    image_2d = extract_grayscale_image(dcm_file)
    if do_auto_contrast:
        image_2d = auto_contrast(image_2d)
    w = png.Writer(image_2d.width, image_2d.height, greyscale=True)
    w.write(png_file, image_2d.image)

def extract_grayscale_image(dcm_file):
    # Извлечение данных из заголовка
    plan = pydicom.read_file(dcm_file)
    shape = plan.pixel_array.shape

    # Перевод в целочисленный тип во избежании потери данных
    image_2d = plan.pixel_array.astype(float)

    # Перешкалирование серой шкалы в диапазоне 0-255
    image_2d_scaled = (np.maximum(image_2d ,0) / image_2d.max()) * 255.0

    # Конвертация в кодировку массива
    image_2d_scaled = np.uint8(image_2d_scaled)

    return GrayscaleImage(image_2d_scaled, shape[1], shape[0])

def convert_file(dcm_file_path, png_file_path, auto_contrast=False):

    if not os.path.exists(dcm_file_path):
        raise Exception('Source file "%s" does not exists' % dcm_file_path)

    if os.path.exists(png_file_path):
        print('Removing existing output file %s' % png_file_path)
        os.remove(png_file_path)

    dcm_file = open(dcm_file_path, 'rb')
    png_file = open(dcm_file_path, 'wb')
    dcm_to_png(dcm_file, png_file, auto_contrast)
    png_file.close()

def convert_folder(dcm_folder, png_folder, auto_contrast=False):
    os.makedirs(png_folder)
    for dcm_sub_folder, subdirs, files in os.walk(dcm_folder):
        for dcm_file in os.listdir(dcm_sub_folder):
            dcm_file_path = os.path.join(dcm_sub_folder, dcm_file)

            if os.path.isfile(dcm_file_path):

                rel_path = os.path.relpath(dcm_sub_folder, dcm_folder)
                png_folder_path = os.path.join(png_folder, rel_path)
                if not os.path.exists(png_folder_path):
                    os.makedirs(png_folder_path)
                png_file_path = os.path.join(png_folder_path, '%s.png' % dcm_file)

                try:
                    # Convert the actual file
                    convert_file(dcm_file_path, png_file_path, auto_contrast)
                    print('SUCCESS: %s --> %s' % (dcm_file_path, png_file_path))
                except Exception as e:
                    print('FAIL: %s --> %s : %s' % (dcm_file_path, png_file_path, e))


folder1 ='/home/alex/fluro/test/norms'
folder2 ='/home/alex/fluro/test_png/norms'
folder3 ='/home/alex/fluro/test/pats'
folder4 ='/home/alex/fluro/test_png/pats'

folder5 ='/home/alex/fluro/val/norms'
folder6 ='/home/alex/fluro/val_png/norms'
folder7 ='/home/alex/fluro/val/pats'
folder8 ='/home/alex/fluro/val_png/pats'

folder9 ='/home/alex/fluro/train/norms'
folder10 ='/home/alex/fluro/train_png/norms'
folder11 ='/home/alex/fluro/train/pats'
folder12 ='/home/alex/fluro/train_png/pats'

convert_folder(folder1, folder2, auto_contrast=False)
convert_folder(folder3, folder4, auto_contrast=False)
convert_folder(folder5, folder6, auto_contrast=False)
convert_folder(folder7, folder8, auto_contrast=False)
convert_folder(folder9, folder10, auto_contrast=False)
convert_folder(folder11, folder12, auto_contrast=False)

if __name__ == '__main__':
    main()










