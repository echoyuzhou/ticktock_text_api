import json
import os
import sys


#the directory structure is as shown in dataset
#code specific to this dataset
#text between a block marked by [EVENTS] is one conversion and consecutive pair  of sentences can be used as question asnwer

def createdic(ln,nxln,dId,counter):
    newdic = {'question':ln,'answer':nxln,'docId':dId,'qsentId':counter,'asentId':counter+1}


def main():
    outdir = 'friendsJSON'
    for seasp, seas, episodes in os.walk('friendsCopyx'):
        for epi in episodes:
            f=open(os.path.join(seasp,epi))
            fo=open(os.path.join(outdir,os.path.join(seasp,epi)),'w')
            counter = 1
            epidic = []
            for ln in f:
                if ln != "[EVENT]":
                
                    if((counter % 2) == 1) and ((next(f)!= "[EVENT]") and next(f)!= ""):
                        newdic = createdic(ln,next(f),os.path.join(seasp,epi),counter)
                        epidic.append(newdic)
                    counter = counter+1

            json.dump(epidic,fo)


if __name__ == "__main__":
main()