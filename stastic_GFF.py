__author__ = 'Guoliang Lin'
Softwarename = 'splitGFF'
version = '1.0.1'
bugfixs = ''
import sys, getopt
import time
def trim(y):
    y = y.replace("[", '')
    y = y.replace(']', '')
    y = y.replace("',", '\t')
    y = y.replace("'", '')
    y = y.replace('\\n', '')
    y = y.replace(' ', '')
    # y=y.replace(',','')
    y = y.strip()
    y = y + '\n'
    return y
def iscontains(x,seg):
    """


    :rtype : bool
    :param x:
    :param seg:
    :return:
    """
    if int(x)>int(seg[0]) and int(x)<int(seg[1]):
        return True
    else:
        return False

def repos(poslist):
    """


    :param poslist:
    :rtype : str
    """
    if poslist[0].find('.')==-1:
        return poslist[0]
    else:
        return poslist[1]

print('%s software version is %s' % (Softwarename, version))
print(bugfixs)
print('starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))
SegmentDict={}

opts, args = getopt.getopt(sys.argv[1:], 'i:s:t:h', ['inputfile=','snp=','total=','help'])
InputFileName = ''
for o, a in opts:
    if o in ['-i', '--inputfile']:
        InputFileName = a
    elif o in ['-s','--snp']:
        snp=a
    elif o in ['-t','--total']:
        total=int(a)
    elif o in ['-h', '--help']:
        help = True
with open(InputFileName, 'r') as InputFile:
    with open(snp,'r') as snp:
        with open(InputFileName+'.out','w') as outputfile:
            for element in InputFile:
                itemlist=element.split()
                if itemlist[0] in SegmentDict.keys():
                    SegmentDict[itemlist[0]].append(itemlist)
                else:
                    SegmentDict[itemlist[0]]=[itemlist]
            for element in snp:
                itemlist=element.split()
                if itemlist[0] in SegmentDict.keys():
                    for x in range(0,len(SegmentDict[itemlist[0]])):
                        if iscontains(repos(itemlist[1:3]),SegmentDict[itemlist[0]][x][3:5]):
                            if len(SegmentDict[itemlist[0]][x])==9:
                                SegmentDict[itemlist[0]][x].append(1)
                                SegmentDict[itemlist[0]][x].append(itemlist[-1])
                            else:
                                SegmentDict[itemlist[0]][x][-2]=SegmentDict[itemlist[0]][x][-2]+1
                                SegmentDict[itemlist[0]][x][-1]=SegmentDict[itemlist[0]][x][-1]+';'+itemlist[-1]
                            break;
            for scafford in SegmentDict.keys():
                for seglist in SegmentDict[scafford]:
                    if len(seglist)!=9:
                        seglist.insert(10,seglist[9]*100.0/total)
                        outputfile.write(trim(str(seglist)))
print('starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))