# 重命名Lighttools .ent库文件，删除版本号
import os
import shutil

path = "D:\APPO\WXWork\1688851319837853\WeDrive\光峰\我的文件\光学数据库\LTUser"
folder_datasheet = "/new/"

path_datasheet = path + folder_datasheet
# path_storage = path + folder_storage

dirlist = os.listdir(path_datasheet)
for name in dirlist:
    # 扩展名检测
    if (name[-4:].lower() == ".ent"):
        if (name[-6] == "."):
            newname = name[:-6] + name[-4:]
            os.rename(path_datasheet+name, path_datasheet+newname)
