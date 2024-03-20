# インストール
#pip install pypiwin32
#pip install wmi

import os
import wmi
import getpass

#現在地点
path = os.getcwd() 

# ログイン名の取得
user = getpass.getuser()

# https://stackoverflow.com/questions/61168145/get-drive-letter-of-storage-drive-by-name-id-in-python

DRIVE_TYPES = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}

drive_list = []

c = wmi.WMI ()
for drive in c.Win32_LogicalDisk ():
    # prints all the drives details including name, type and size
    #print(drive)
    #print (drive.Caption, drive.VolumeName, DRIVE_TYPES[drive.DriveType])
    drive_list.append(drive.DeviceID + "/Users/" + f'{user}' + "/AppData/Local/Programs/" + "Python")
    #print(drive.DeviceID + "/Users/" + f'{user}' + "/AppData/Local/Programs/")

print(drive_list)

for i in range(3):
  try:
    dir_path = drive_list[i]
    files = os.listdir(dir_path)
    print(files)
  except FileNotFoundError:
    print(dir_path + " には指定されたパスが見つかりませんでした。")  