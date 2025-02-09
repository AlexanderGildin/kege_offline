from PIL import Image
import os


def image_size_changes(list_, required_width, result_file_name='final_image.png'):  # в функцию передаются список с именами картинок
    # и ширина итогового изображения
    n = 0
    list_modified = []  # список для сохранения имен измененных изображения
    overall_height = []  # список для сохранения высот изображений

    for file_name in list_:
        im = Image.open(file_name)  # открытие изображения
        image_width, image_height = im.size  # получение размеров изображения

        ratio = image_width / required_width  # получение коэффициента пропорциональности
        new_height = int(image_height / ratio)  # получение новой высоты изображения
        overall_height.append(new_height)  # добавление новой высоты в список
        new_size = (required_width, new_height)  # кортеж с новыми размерами изображения
        im_1 = im.resize(new_size)  # создание нового изображения с необходимыми размерами
        im_1.save('file_' + str(n) + '.png')  # сохранение нового изображения в каталог с проектом
        list_modified.append('file_' + str(n) + '.png')  # добавление названия файла в список
        n += 1

    new_im = Image.new('RGB', (required_width, sum(overall_height)), (250, 250, 250))
    # создание нового белого изображения
    for i in range(len(list_modified)):
        im = Image.open(list_modified[i])  # открытие измененного изображения
        if i == 0:
            new_im.paste(im, (0, 0))  # вставляем изображение в верх белого изображения new_im
        else:
            new_im.paste(im, (0, sum(overall_height[:i])))  # вставляем изображение под предыдущее
        os.remove(list_modified[i])  # удаление изображения из каталога с проектом
    new_im.save(result_file_name)  # сохранение итогового изображения


