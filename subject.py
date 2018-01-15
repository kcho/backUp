# -*- coding: utf-8 -*-
'''
# Back up data and forms a database from the MRI data
# Created by Kang Ik Kevin Cho
# Contributors: Dahye Stella Bae, Eunseo Cho
'''
from __future__ import division
import os
from os.path import basename, join, isdir, dirname, abspath
import dicom
import re
import pandas as pd
import getpass

from progressbar import AnimatedMarker,ProgressBar,Percentage,Bar


class dicomSubjectDir:
    def __init__(self, subjectDir):
        self.location = abspath(subjectDir)

        # Search for dicoms
        dicoms = []
        for root, dirs, files in os.walk(self.location):
            for oneFile in files:
                if re.search('(dcm|ima)', oneFile, re.IGNORECASE):
                    dicoms.append(join(root,oneFile))

        self.allDicomNum = len(dicoms)

        # Dicom directory names
        dicomDirs = set([dirname(x) for x in dicoms])
        self.dirs = dicomDirs
        self.modalityMapping = [modalityMapping(x) for x in self.dirs]

        # Dictionary
        dicomDirDict = {}
        for dicomDir in dicomDirs:
            dicom_under_dicomDir = [x for x in dicoms if x.startswith(dicomDir)]
            dicomDirDict[dicomDir] = dicom_under_dicomDir
        self.dicomDirs = dicomDirDict
        self.dirDicomNum = [(x,len(y)) for (x,y) in dicomDirDict.items()]
        self.modalityDicomNum = dict(zip(self.modalityMapping, [x[1] for x in self.dirDicomNum]))

        # Read first dicom
        #self.firstDicom = dicoms[0]
        self.firstDicom = 'dicom_tmp.IMA' # remove this later

class subject(dicomSubjectDir):
    def __init__(self, subjectDir):
        super().__init__(subjectDir)
        ds = dicom.read_file(self.firstDicom)
        self.age = re.search('^0(\d{2})Y',ds.PatientAge).group(1)
        self.dob = ds.PatientBirthDate
        self.id = ds.PatientID
        self.surname = ds.PatientName.family_name
        self.name = ds.PatientName.given_name

        try:
            self.fullname = ''.join([x[0].upper()+x[1:].lower() for x in [self.surname, self.name.split(' ')[0], self.name.split(' ')[1]]])
            self.initial = self.surname[0]+''.join([x[0] for x in self.name.split(' ')])
        except: #for one syllabel korean names
            self.fullname = ''.join([x[0].upper()+x[1:].lower() for x in [self.surname, self.name]])
            self.initial = self.surname[0]+self.name[0]
        
        self.sex = ds.PatientSex
        self.date = ds.StudyDate

class subject_extra(subject):
    def __init__(self, subjectDir):
        super().__init__(subjectDir)
        self.experimenter = getpass.getuser()
        print('Now collecting information for')
        print('==============================')
        print('\n\t'.join([self.location, self.fullname, self.initial, self.id, self.dob, 
                           self.date, self.sex, ', '.join(self.modalityMapping),
                           'by ' + self.experimenter]))
        print('==============================')
        self.koreanName = input('Korean name  ? eg. 김민수: ')
        self.note = input('Any note ? : ')
        self.group = input('Group ? : ')
        self.study = input('Study name ? : ')
        self.timeline = input('baseline or follow up ? eg) baseline, 6mfu, 1yfu, 2yfu : ')

class subject_full(subject_extra):
    def __init__(self, subjectDir, dbLoc):
        super().__init__(subjectDir)
        self.numberForGroup = maxGroupNum(join(dbLoc, self.group))

        # If follow up, grep the previous data
        if self.timeline != 'baseline':
            df = pd.ExcelFile(join(dbLoc,'database','database.xls')).parse(0)
           
            # Match using the hospital ID
            self.folderName = df.iloc[(df.timeline=='baseline') & (df.patientNumber == int(self.id)), 
                                      'folderName'].values.tolist()[0]

            print('\n\n\t\tNow Backing up to {}\n\n'.format(self.folderName)
            self.targetDir = join(dbLoc,
                                  self.group,
                                  self.folderName,
                                  self.timeline)
        else:
            self.folderName = self.group + self.numberForGroup + '_' + self.initial
            self.targetDir = join(dbLoc,
                                  self.group,
                                  self.folderName,
                                  self.timeline)    


def modalityMapping(directory):
    t1 = re.compile(r'^t1_\d{4}',re.IGNORECASE)
    t2 = re.compile(r'^t2_\d{4}',re.IGNORECASE)
    scout = re.compile(r'scout',re.IGNORECASE)
    rest = re.compile(r'rest\S*lr_sbref_\d{4}',re.IGNORECASE)
    restRef = re.compile(r'rest\S*lr(_sbref){2}',re.IGNORECASE)
    restBlipRL = re.compile(r'rest\S*blip_rl',re.IGNORECASE)
    restBlipLR = re.compile(r'rest\S*blip_lr',re.IGNORECASE)
    dti3 = re.compile(r'dti\S*B30',re.IGNORECASE)
    dti2 = re.compile(r'dti\S*B20',re.IGNORECASE)
    dti1 = re.compile(r'dti\S*B10',re.IGNORECASE)
    dtiBlipRL = re.compile(r'dti\S*rl_\d{4}',re.IGNORECASE)
    dtiBlipLR = re.compile(r'dti\S*lr_\d{4}',re.IGNORECASE)

    correct_modality_re_dict = {'T1':t1,
                                'T2':t2,
                                'SCOUT':scout,
                                'REST':rest,
                                'REST_REF':restRef,
                                'REST_BLIP_RL':restBlipRL,
                                'REST_BLIP_LR':restBlipLR,
                                'DTI_3000':dti3,
                                'DTI_2000':dti2,
                                'DTI_1000':dti1,
                                'DTI_BLIP_RL':dtiBlipRL,
                                'DTI_BLIP_LR'dtiBlipLR}

    for modality_name, re_compile correct_modality_re_dict.iter():
        basename = basename(directory)
        try:
            matchingSource = re_compile.search(basename).group(0)
            return modality_name
        except:
            pass
    return directory


def maxGroupNum(backUpTo):
    maxNumPattern=re.compile('\d+')

    mx = 0
    for string in maxNumPattern.findall(' '.join(os.listdir(backUpTo))):
        if int(string) > mx:
            mx = int(string)

    highest = mx +1
    highest_zero_padded = '{0:03d}'.format(highest)

    return highest_zero_padded
