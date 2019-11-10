from PIL import Image
import random


def bits2string(b=None):
    lst = []
    a = ""
    for i in b:
        a += i
        if len(a) == 11:
            lst.append(a)
            a = ""
    return ''.join([chr(int(x, 2)) for x in lst])


def string2bits(s=''):
    lst = [bin(ord(x))[2:].zfill(11) for x in s]
    string = ""
    for i in lst:
        string += str(i)
    return string

def image_encode(file_, bintext, seed):
    try:
        img = Image.open(file_)
    except FileNotFoundError:
        print("Ошибка!\nКонтейнер не найден")
        return
    img = img.convert('RGB')
    width, height = img.size
    mod = width*height // len(bintext) - 1
    if mod == 0:
        print("Ошибка!\nКонтейнер имеет недостаточный размер\n")
        return
    out_file = 'out' + file_[len(file_)-file_[::-1].index('.')-1:]
    new_img = Image.new('RGB', (width,height))
    count = 0
    random.seed(seed)
    j = random.randint(1,mod)
    for i in range(width*height):
        r, g, b = img.getpixel((i % width, i // width))
        if j == i:
            if int(bintext[count]) == 0:
                    b &= 254
            else:
                b |= 1
            j += random.randint(1,mod)
            count += 1
            if count == len(bintext):
                j = 0
        new_img.putpixel((i % width, i // width),(r, g, b))
    new_img.save(out_file)


def image_decode(file_, seed, size):
    size *= 11
    bintext = ""
    try:
        img = Image.open(file_)
    except FileNotFoundError:
        print("Ошибка!\nКонтейнер не найден")
        return
    img = img.convert('RGB')
    width, height = img.size
    mod = width*height // size - 1
    random.seed(seed)
    j = random.randint(1,mod)
    count = 0
    for i in range(width*height):
        r, g, b = img.getpixel((i % width, i // width))
        if j == i:
            bintext += str(b % 2)
            j += random.randint(1,mod)
            count += 1
            if count == size:
                break
    return bits2string(bintext)


while 1:
    print("Выберите действие:\n1.Зашить текст в файл\n2.Получить данные из изображения\n3.Выход")
    c = str(input())
    if c == '1':
        print("Введите текст для сокрытия")
        string = str(input())
        print("Введите имя файла изображения")
        in_name = str(input())
        print("Введите ключ")
        try:
            key = int(input())
        except ValueError:
            print("Ошибка!\nКлюч - это десятичное число")
        else:
            image_encode(in_name, string2bits(string),key)
    elif c == '2':
        print("Введите имя файла изображения")
        name = str(input())
        print("Введите ключ")
        try:
            seed,ln = map(int,input().split())
        except ValueError:
            print("Ошибка!\nНеверный формат ключа")
        else:
            print(image_decode(name,seed,ln))
    elif 1:
        break
