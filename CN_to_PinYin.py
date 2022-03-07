from xpinyin import Pinyin
import os


p = Pinyin()
path = "\\char_change\\20201212_(6)\\"
filename_list = os.listdir("\\char_change\\20201212_(6)\\")

for i in filename_list:
    # print(i)
    for j in os.listdir(path + i):
        # print(j)
        used_name = path + i + "\\" + j
        # print(used_name)
        new_name = path + i + '\\' + p.get_pinyin(i[:3], '') + j[3:]
        # print(new_name)
        os.rename(used_name, new_name)
        print("文件%s重命名成功，新的文件名为%s" % (used_name, new_name))
