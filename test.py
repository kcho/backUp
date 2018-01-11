#from backUp import *
#import backUp
import os
from os.path import join, basename, abspath, dirname, isdir
import argparse
import textwrap
import pickle
import pandas as pd
#import motion_extraction
#import freesurfer
#import freesurfer_summary
import numpy as np
from backUp import *


folder_names_count = {'DTI_BLIP_LR_0011':7,
                      'DTI_BLIP_RL_0012':7,
                      'DTI_MB3_LR_B1000_0008':21,
                      'DTI_MB3_LR_B2000_0009':31,
                      'DTI_MB3_LR_B3000_0010':65,
                      'REST_MB1_BLIP_LR_0006':3,
                      'REST_MB1_BLIP_RL_0007':3,
                      'REST_MB4_LR_SBREF_0005':250,
                      'REST_MB4_LR_SBREF_SBREF_0004':1,
                      'SCOUT_HEAD_32CH_0001':9,
                      'T1_0002':224,
                      'T2_0003':224}

class subject(object):
    def __init__(self):
        self.location = abpath('TEST')
        get_dicomDirs = lambda name,num: ['{}/{}.dcm'.format(name, x) for x in np.arange(num)]
        dicomDirDict = {}
        for name, num in folder_names_count.items():
            dicomDirDict[name] = get_dicomDirs(name, num)

        self.dicomDirs=dicomDirDict
        self.dirs = dicomDirDict.keys()
        self.modalityMapping = [modalityMapping(x) for x in self.dirs]
        self.modalityDicomNum = dict(zip(self.modalityMapping, [x[1] for x in self.dirDicomNum]))
        self.firstDicom = next(iter(self.dicomDirs.values()))[0]
        self.age = 10
        self.dob = 19880916
        self.id = 77777777
        self.surname = 'CHO'
        self.name = 'KANGIK'
        self.fullname = 'KangIkCho'
        self.initial = 'KIC'
        self.sex = 'M'
        self.date = '20180111'
        self.experimenter = 'kcho'
        self.koreanName = '김민수'
        self.note = 'ha'
        self.group = 'CHR'
        self.numberForGroup = maxGroupNum(os.path.join(dbLoc, self.group))
        self.study = 'hoho'
        self.timeline = 'baseline'
        self.folderName = self.group + self.numberForGroup + '_' + self.initial
        self.targetDir = join(dbLoc,
                              self.group,
                              self.folderName,
                              self.timeline)    

if __name__ == '__main__':
    log_file_in_hdd = join('TEST', "log.xlsx")
    log_df = copiedDirectoryCheck('TEST', log_file_in_hdd)
    inputDirs, log_df_updated = findNewDirs('Test', log_df)
    log_df_updated.to_excel(log_file_in_hdd,'Sheet1')
    if newDirectoryList == []:
        sys.exit('Everything have been backed up !')

    backUp(inputDirs, 
           'TEST_backUp', 
           'database.xlsx', 
           'spreadsheet.xlsx')


##execute copy test
#try:
    #backUp.executeCopy(subjClass)
#except:
    #pass
#print subjClass.folderName
#subjDf = backUp.saveLog(subjClass)
#print subjDf
#DataBaseAddress = 'database.xls'

#dbDf = backUp.processDB(DataBaseAddress)
#newDf = pd.concat([dbDf, subjDf])
##print newDf
#newDf.koreanName = newDf.koreanName.str.decode('utf-8')
#newDf.note = newDf.note.str.decode('utf-8')
#print 'haha'

#newDf.to_excel(DataBaseAddress, 'Sheet1')
#os.chmod(DataBaseAddress, 0o2770)




#print subjClass.targetDir
##try:
    ###motion_extraction.main(subjClass.targetDir, True, False, False)
##except:
    ##pass

##backUp.server_connect('147.47.228.192', os.path.dirname(subjClass.targetDir))

##freesurfer.main(True, False, False, subjClass.targetDir,
        ##os.path.join(subjClass.targetDir, 'FREESURFER'))


#freesurfer_summary.main('/Volumes/promise/nas_BackUp/CCNC_MRI_3T/CHR/CHR45_JYS/followUp/2yfu', None, "ctx_lh_G_cuneus", True, True, True, True)


##os.popen('sudo rm -rf /Volumes/promise/nas_BackUp/CCNC_MRI_3T/CHR/CHR95_KSU')

##savedList = 
##if 'ha' in os.listdir(os.getcwd()):
    ##with open('ha','r') as f:
        ##[newDirectoryList, logDf] = pickle.load(f)

### copied directory check test

##else:
    ##logDf = copiedDirectoryCheck('pracDir/from', 'pracDir/from/log.xlsx')


    ### newDirectoryGrep
    ##newDirectoryList,logDf = newDirectoryGrep(False, 'pracDir/from', logDf)


    ##with open('ha', 'w') as f:
        ##pickle.dump([newDirectoryList, logDf], f)


##if 'foundDict' in os.listdir(os.getcwd()):
    ##with open('foundDict', 'r') as f:
        ##foundDict = pickle.load(f)

##else:
    ##foundDict=findDtiDkiT1restRest2(newDirectoryList)
    ##with open('foundDict', 'w') as f:
        ##pickle.dump(foundDict, f)

##backUpTo = './pracDir/to'
##backUpFrom = '.pracDir/from'
##DataBaseAddress = '.pracDir/database.xlsx'

##allInfo,df,newDfList=verifyNumbersAndLog(foundDict,backUpTo,backUpFrom,DataBaseAddress)






##print a.fullname
##print a.name
##print a.initial
##print a.number_for_group
##print a.dirDicomNum


##print a.modalityMapping
##print a.dicomDirs
##print a.dirDicomNum
##print a.modalityMapping
##print a.dirs
##print a.targetDir
##print a.dob
##print a.date


