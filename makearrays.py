import numpy as np
import os
import glob
from readfiles import *


def makearrays(dir_bed):
    """function for numpy arrays"""
    n = 1
    #data = []
    for file in glob.glob(os.path.join(dir_bed, '*narrowPeak1')):
        data = []
        print file
        for fileres in sorted(glob.glob(os.path.join(dir_bed, '*_' + str(n)))):
            valuesfromeachfile1 = np.loadtxt(fileres, usecols=[3])
            valuesfromeachfile = valuesfromeachfile1.astype(int)
            # np.concatenate([data, valuesfromeachfile])
            data.append(valuesfromeachfile)
            print (fileres)
        data1 = np.array(data)
        data2 = np.transpose(data1)
        #datanew = data2[~np.all(np.equal(data2, 0), axis=1)]

        print data2
        #fileout3 = os.path.join(dir_bed, 'res' + str(n))
        fileout3 = file +"finalthreecol.xls"
        # np.savetxt(fileout1, data1, fmt='%i')
        # np.savetxt(fileout2, data2, fmt='%i')
        np.savetxt(fileout3, data2, fmt='%i')
        #np.savetxt(fileout3, data2)
        # data3 = np.loadtxt(fileout2)
        filtercriteria(dir_bed,  file, fileout3)
        n += 1
    #return data3


def filtercriteria(dir_bed, file, fileout3):
    fileoutxls = os.path.join(dir_bed, fileout3)
    data3 = np.loadtxt(fileoutxls)

    #todel = [0]
    data4 =np.unique(data3[:, 0])
    data5 = np.unique(data3[:, 1])
    data6 = np.unique(data3[:, 2])
    print data4
    # Last column is factor; First two are modifications
    # Lesser than 20
    ##### higher = 600
    ###lower = 400
    perc1low = np.percentile(data4, 40)
    perc2high = np.percentile(data4, 60)
    #perc1low = np.percentile(data4[:, 0], 20)
    #perc2high = np.percentile(data4[:, 0], 80)
    perc3low = np.percentile(data5, 40)
    perc4high = np.percentile(data5, 60)
    perc5low = np.percentile(data6, 40)
    perc6high = np.percentile(data6, 60)
    print perc1low
    print perc2high
    print perc3low
    print perc4high
    print perc5low
    print perc6high

    #higher = 80
    #lower = 30
    crit1_ggl = data3[(data3[:, 0] > perc2high) & (data3[:, 1] > perc4high) & (data3[:, 2] < perc5low)]
    # print (np.mean(criteria1[:2]))
    crit2_gll = data3[(data3[:, 0] > perc2high) & (data3[:, 1] < perc3low) & (data3[:, 2] < perc5low)]
    crit3_lgl = data3[(data3[:, 0] < perc1low) & (data3[:, 1] > perc4high) & (data3[:, 2] < perc5low)]
    crit4_lll = data3[(data3[:, 0] < perc1low) & (data3[:, 1] < perc3low) & (data3[:, 2] < perc5low)]

    # Greater than 80
    crit5_ggg = data3[(data3[:, 0] > perc2high) & (data3[:, 1] > perc4high) & (data3[:, 2] > perc6high)]
    crit6_glg = data3[(data3[:, 0] > perc2high) & (data3[:, 1] < perc3low) & (data3[:, 2] > perc6high)]
    crit7_llg = data3[(data3[:, 0] < perc1low) & (data3[:, 1] < perc3low) & (data3[:, 2] > perc6high)]
    crit8_lgg = data3[(data3[:, 0] < perc1low) & (data3[:, 1] > perc4high) & (data3[:, 2] > perc6high)]

    fileout1 = os.path.join(dir_bed, 'test1.txt')
    np.savetxt(fileout1, crit1_ggl, fmt='%i')
    fileout2 = os.path.join(dir_bed, 'test2.txt')
    np.savetxt(fileout2, crit2_gll, fmt='%i')
    fileout3 = os.path.join(dir_bed, 'test3.txt')
    np.savetxt(fileout3, crit3_lgl, fmt='%i')
    fileout4 = os.path.join(dir_bed, 'test4.txt')
    np.savetxt(fileout4, crit4_lll, fmt='%i')
    fileout5= os.path.join(dir_bed, 'test5.txt')
    np.savetxt(fileout5, crit5_ggg, fmt='%i')
    fileout6 = os.path.join(dir_bed, 'test6.txt')
    np.savetxt(fileout6, crit6_glg, fmt='%i')
    fileout7 = os.path.join(dir_bed, 'test7.txt')
    np.savetxt(fileout7, crit7_llg, fmt='%i')
    fileout8 = os.path.join(dir_bed, 'test8.txt')
    np.savetxt(fileout8, crit8_lgg, fmt='%i')

    print crit3_lgl.size/3
    filecount = file+"_result.xls"
    fileoutcounts = os.path.join(dir_bed, filecount)
    np.savetxt(fileoutcounts, (crit1_ggl.size/3, crit2_gll.size/3, crit3_lgl.size/3, crit4_lll.size/3, crit5_ggg.size/3, crit6_glg.size/3, crit7_llg.size/3, crit8_lgg.size/3), fmt="%s", newline='\r\n')
