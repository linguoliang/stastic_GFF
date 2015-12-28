__author__ = 'Guoliang Lin'
Softwarename = 'stasticGFF'
version = '2.0.6'
bugfixs = 'fixs discarding the last of segemt of each scaffold'
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

def f(a):
    if len(a)==9:
        return int(a[3])
    else:
        return int(repos(a[0:2]))


print('%s software version is %s' % (Softwarename, version))
print(bugfixs)
print('starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))
SegmentDict={}
TypeDict={}
Totalname=0
writeitem=[]
end=0
opts, args = getopt.getopt(sys.argv[1:], 'i:s:t:n:h', ['inputfile=','snp=','total=','name=','help'])
InputFileName = ''
oname=''
for o, a in opts:
    if o in ['-i', '--inputfile']:
        InputFileName = a
    elif o in ['-s','--snp']:
        snpfile=a
    elif o in ['-t','--total']:
        total=int(a)
    elif o in ['-n','--name']:
        oname=a
    elif o in ['-h', '--help']:
        help = True
with open(InputFileName, 'r') as InputFile:
    with open(snpfile,'r') as snp:
        with open(oname,'w') as outputfile:
            with open(oname+'_stastic','w') as typefile:
                InputFile.readline()
                for element in InputFile:
                    itemlist=element.split()
                    if SegmentDict.has_key(itemlist[0]):
                        SegmentDict[itemlist[0]].append(itemlist[1:])
                    else:
                        SegmentDict[itemlist[0]]=[itemlist[1:]]
                for element in snp:
                    itemlist=element.split()
                    if SegmentDict.has_key(itemlist[0]):
                        SegmentDict[itemlist[0]].append(itemlist)
                for keys in SegmentDict.keys():
                    SegmentDict[keys].sort(key=f)
                    typelist=''
                    number=0
                    end=0
                    writeitem=[]
                    for snplist in SegmentDict[keys]:
                        if len(snplist)==9:
                            if len(writeitem)!=0:
                                #print str(number)
                                writeitem.append(str(number))
                                writeitem.append(str(number*100/total))
                                writeitem.append(typelist)
                                if number!=0:
                                    outputfile.write(trim(str(writeitem)))
                            end=int(snplist[4])
                            #print end
                            writeitem=snplist
                            typelist=''
                            number=0
                        elif int(repos(snplist[0:2]))<end:
                            if TypeDict.has_key(snplist[-1]):
                                TypeDict[snplist[-1]]+=1
                            else:
                                TypeDict[snplist[-1]]=1
                            Totalname+=1
                            number=number+1
                            if typelist.find(snplist[-1])==-1:
                                typelist=typelist+','+snplist[-1]
                    if number>0:
                        writeitem.append(str(number))
                        writeitem.append(str(number*100/total))
                        writeitem.append(typelist)
                        outputfile.write(trim(str(writeitem)))
                for key in TypeDict.keys():
                    typefile.write(key+'\t'+str(TypeDict[key])+'\t'+str(Totalname)+'\t'+str(100.0*TypeDict[key]/Totalname)+'\n')
                    #     for x in range(0,len(SegmentDict[itemlist[0]])):
                    #         if iscontains(repos(itemlist[1:3]),SegmentDict[itemlist[0]][x][3:5]):
                    #             if len(SegmentDict[itemlist[0]][x])==9:
                    #                 SegmentDict[itemlist[0]][x].append(1)
                    #                 SegmentDict[itemlist[0]][x].append(itemlist[-1])
                    #             else:
                    #                 SegmentDict[itemlist[0]][x][-2]=SegmentDict[itemlist[0]][x][-2]+1
                    #                 SegmentDict[itemlist[0]][x][-1]=SegmentDict[itemlist[0]][x][-1]+';'+itemlist[-1]
                    #             break
print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))
