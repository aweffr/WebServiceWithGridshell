import os
import sys

sys.path.append('./Core')

from Utils import *
from FirstStep import *
from CovertJson import *

if __name__ == '__main__':
    test = [(0, 0), (7, 12), (16, 9), (27, 13), (36, 0)]
    init_plain(0, 36, 1, "init_plain.dat", 'mdbFile', 'odbJob', point_list=test[:],
               abaqus_file_save_path='./AbaqusFiles')
    with open('init.json', 'w') as json:
        json.writelines(covert_json("init_plain.dat"))
    try:
        os.system("abaqus cae noGUI=./AbaqusAPI/BuildModel.py")
    except Exception as e:
        print e
