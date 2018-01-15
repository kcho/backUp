#from backUp import *
#import backUp
import os
import shutil
from os.path import join, basename, abspath, dirname, isdir
import argparse
import textwrap
import pickle
import pandas as pd
import numpy as np
from backUp import *
import subject as subj
import subject


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

folder_names_modality = {'DTI_BLIP_LR_0011':'DTI_BLIP_LR',
                      'DTI_BLIP_RL_0012':'DTI_BLIP_RL',
                      'DTI_MB3_LR_B1000_0008':'DTI_LR_1000',
                      'DTI_MB3_LR_B2000_0009':'DTI_LR_2000',
                      'DTI_MB3_LR_B3000_0010':'DTI_LR_3000',
                      'REST_MB1_BLIP_LR_0006':'REST_BLIP_LR',
                      'REST_MB1_BLIP_RL_0007':'REST_BLIP_RL',
                      'REST_MB4_LR_SBREF_0005':'REST_LR',
                      'REST_MB4_LR_SBREF_SBREF_0004':'REST_LR_SBRef',
                      'SCOUT_HEAD_32CH_0001':'SCOUT',
                      'T1_0002':'T1',
                      'T2_0003':'T2'}

modalityCountDict = {'DTI_BLIP_LR': 7,
                        'DTI_BLIP_RL': 7,
                        'DTI_LR_1000': 21,
                        'DTI_LR_2000': 31,
                        'DTI_LR_3000': 65,
                        'REST_BLIP_LR': 3,
                        'REST_BLIP_RL': 3,
                        'REST_LR': 250,
                        'REST_LR_SBRef': 1,
                        'SCOUT': 9,
                        'T1': 224,
                        'T2': 224}


# Original subject
# subjClass = subj.subject(newDirectory, backUpTo)
class subject(subj.subject):
    def __init__(self, subjectDir, dbLoc):
        super().__init__(subjectDir)
        #self.location = abspath('TEST')
        #get_dicomDirs = lambda name,num: ['{}/{}/{}/{}.dcm'.format(self.location, 'KANG_IK_CHO_77777777', name, x) for x in np.arange(num)]
        #dicomDirDict = {}
        #for name, num in folder_names_count.items():
            #dicomDirDict[join(self.location, 'KANG_IK_CHO_77777777', name)] = get_dicomDirs(name, num)

        #self.dicomDirs=dicomDirDict
        #self.dirs = dicomDirDict.keys()

        #self.modalityMapping = [folder_names_modality[basename(x)] for x in self.dirs]
        #print(self.modalityMapping)
        #self.modalityDicomNum = modalityCountDict
        #allDicoms = []
        #for i in dicomDirDict.values():
            #for j in i:
                #allDicoms.append(j)
        #self.allDicomNum = len(allDicoms)

        #self.dirDicomNum = [(join(self.location, x[0]), x[1]) for x in zip(dicomDirDict.keys(), modalityCountDict.values())]
        #print(self.dirDicomNum)
        #self.firstDicom = next(iter(self.dicomDirs.values()))[0]
        #self.age = 10
        #self.dob = '19880916'
        #self.id = 77777777
        #self.surname = 'CHO'
        #self.name = 'KANGIK'
        #self.fullname = 'KangIkCho'
        #self.initial = 'KIC'
        #self.sex = 'M'
        #self.date = '20180111'
        #self.experimenter = 'kcho'
        self.firstDicom = 'dicom_tmp.IMA' # remove this later
        self.experimenter = 'kcho'
        self.koreanName = '김민수'
        self.note = 'ha'
        self.group = 'CHR'
        self.numberForGroup = '04'
        self.study = 'hoho'
        self.timeline = 'baseline'
        self.dx='hoho'
        self.folderName = self.group + self.numberForGroup + '_' + self.initial
        self.targetDir = abspath('TEST_backUp')

if __name__ == '__main__':
    shutil.rmtree('TEST')
    shutil.rmtree('TEST_backUp')
    os.mkdir('TEST_backUp')
    os.mkdir('TEST')
    os.mkdir('TEST/KANG_IK_CHO_77777777')
    backUpTo = 'TEST_backUp'
    DataBaseAddress = 'database.xlsx'
    spreadsheet = 'spreadsheet.xlsx'


    get_dicomDirs = lambda name,num: ['{}/{}/{}/{}.dcm'.format('TEST', 'KANG_IK_CHO_77777777', name, x) for x in np.arange(num)]
    dicomDirDict = {}
    for name, num in folder_names_count.items():
        dicomDirDict[join('TEST', 'KANG_IK_CHO_77777777', name)] = get_dicomDirs(name, num)

    for modality_raw_dir, dicoms in dicomDirDict.items():
        print(modality_raw_dir)
        os.mkdir(modality_raw_dir)
        for j in dicoms:
            with open(j, 'wb') as f:
                f.write(b'')

    log_file_in_hdd = join('TEST', "log.xlsx")
    log_df = copiedDirectoryCheck('TEST', log_file_in_hdd)
    inputDirs, log_df_updated = findNewDirs('TEST', log_df)
    log_df_updated.to_excel(log_file_in_hdd,'Sheet1')
    if inputDirs == []:
        sys.exit('Everything have been backed up !')


    subjectClassList = []
    for newDirectory in inputDirs:
        subjClass = subject(newDirectory, backUpTo)
        #checkFileNumbers(subjClass)
        subjectClassList.append(subjClass)

        executeCopy(subjClass)

        subjDf = saveLog(subjClass)
        print(subjDf)

        dbDf = processDB(DataBaseAddress)
        print(dbDf)

        newDf = pd.concat([dbDf, subjDf]).reset_index()
        newDf = newDf[[ u'koreanName',  
                        u'subjectName',
                        u'subjectInitial',
                        u'group',
                        u'sex',
                        u'age',
                        u'DOB',
                        u'scanDate',
                        u'timeline',
                        u'studyname',
                        u'patientNumber',
                        u'T1',
                        u'T2',
                        u'REST_LR',
                        u'REST_LR_SBRef',
                        u'REST_BLIP_LR',
                        u'REST_BLIP_RL',
                        u'DTI_LR_1000',
                        u'DTI_LR_2000',
                        u'DTI_LR_3000',
                        u'DTI_BLIP_LR',
                        u'DTI_BLIP_RL',
                        u'dx',
                        u'folderName',
                        u'backUpBy',
                        u'note']]
        print(newDf)
        print('-'*80)
        #please confirm here

        newDf.to_excel(DataBaseAddress, 'Sheet1')
        # os.chmod(DataBaseAddress, 0o2770)

        #updateSpreadSheet.main(False, DataBaseAddress, spreadsheet)#False
    #print('Completed\n')

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


