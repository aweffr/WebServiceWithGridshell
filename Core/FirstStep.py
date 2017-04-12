# -*- coding: utf-8 -*-

from Utils import *
import shelve
import os


def init_plain(start, stop, step, shv_file_name, mdb_save_name, odb_save_name,
               vector=(0, 0, 0), point_list=[], abaqus_file_save_path=os.getcwd()):
    spl = get_spl(point_list)
    xcoord = generate_xcoord(spl, start, stop, step)
    ycoord = generate_ycoord(spl, start, stop, step)
    incoord = generate_incoord(spl, start, stop, step)
    xcoord_3d = to_3d_xy(xcoord)
    ycoord_3d = to_3d_xy(ycoord)
    incoord_3d = to_3d_in(incoord)

    fig = plt.figure(figsize=(15, 8))
    plt.plot(xlist(point_list), ylist(point_list), 'r^', markersize=16)
    xx = np.linspace(0, 36, 1000)
    yy = spl(xx)
    plt.plot(xx, yy, 'r--', linewidth=6)
    for lst in xcoord + ycoord:
        plt.plot(xlist(lst), ylist(lst), linewidth=1.2)
    for x, y in incoord:
        plt.plot(x, y, 'ro', markersize=3.5)
    plt.xlim((-3.0, 39.0), )
    fig.savefig("initial_plain.png")

    try:
        shv = shelve.open(shv_file_name)
        shv['time'] = 0
        shv['xCoordPoints'] = xcoord
        shv['yCoordPoints'] = ycoord
        shv['inCoordPoints'] = incoord
        shv['xCoordPoints_3D'] = xcoord_3d
        shv['yCoordPoints_3D'] = ycoord_3d
        shv['inCoordPoints_3D'] = incoord_3d
        shv['vector'] = vector
        shv['abaqusFileSavePath'] = abaqus_file_save_path
        shv['mdbSaveName'] = mdb_save_name
        shv['odbSaveName'] = odb_save_name
    except Exception as e:
        print "Error when writing init_plain.dat:"
        print e
    finally:
        shv.close()

    print "Figure and plain data has been saved at %s" % os.getcwd()


if __name__ == "__main__":
    test = [(0, 0), (7, 9.8), (16, 9), (27, 13), (36, 0)]
    init_plain(0, 36, 1, point_list=test[:])
