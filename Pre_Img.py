from PIL import Image
import os


def dir_name(dir): # 改变图片名
    i = 1
    for filename in os.listdir(dir):
        newName = str(202109) + "_" + str(i) + ".jpg"
        os.rename(dir + filename, dir + newName)
        i += 1


def convert(dir, width, height):  # 裁剪图片大小
    file_list = os.listdir(dir)
    print(file_list)
    for filename in file_list:
        path = dir + filename
        im = Image.open(path)
        out = im.resize((512, 512), Image.ANTIALIAS)
        print("%s has been resize!" % filename)
        out.save(path)


def rotate_img(dir):  # 旋转图片角度
    filelist = os.listdir(dir)
    for filename in filelist:
        path = dir + filename
        im = Image.open(path)
        im1 = im.transpose(Image.ROTATE_270)
        im1.save("D:\\dateset\\dataset_fin\\%s" % filename)


if __name__ == '__main__':
    dir = input('please input the operate dir:')
    dir_name(dir)
    convert(dir, 512, 512)
    rotate_img(dir)
