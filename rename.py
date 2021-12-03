import os

path = input('请输入文件路径(结尾加上/)：')

# 获取该目录下所有文件，存入列表中
fileList = os.listdir(path)

n = 0
for i in fileList:
    # 设置旧文件名（就是路径+文件名）
    oldName = path + os.sep + fileList[n]  # os.sep添加系统分隔符
    print(oldName)

    # 设置新文件名
    newName = os.path.splitext(oldName)[0]
    newName = newName[: -6] + '.png'
    print(newName)

    os.rename(oldName, newName)  # 用os模块中的rename方法对文件改名
    print(oldName, '======>', newName)

    n += 1
