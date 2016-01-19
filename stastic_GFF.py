#coding=utf-8
__author__ = 'Guoliang Lin'
Softwarename = 'stasticGFF'
version = '3.0.1'
bugfixs = '     2015-12-18:fixs discarding the last of segemt of each scaffold\n' \
          '     2016-01-19:fixs overlap cuasing discarding some virations.'
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


print('%s software version is %s in 2016-01-19' % (Softwarename, version))
print(bugfixs)
print('starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))
SegmentDict={}
TypeDict={}
Totalname=0
writeitem=[]
end=0
opts, args = getopt.getopt(sys.argv[1:], 'i:s:t:n:j:h', ['inputfile=','snp=','total=','name=','help'])
"""
参数加法:
-i
"""
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
                with open(oname+'_fortrimreplicates','w') as typefile1:
                    InputFile.readline()
                    for element in snp:
                        itemlist=element.split()
                        if SegmentDict.has_key(itemlist[0]):
                            SegmentDict[itemlist[0]].append(itemlist)
                        else:
                            SegmentDict[itemlist[0]]=[itemlist]
                    for element in InputFile:
                        itemlist=element.split()
                        if SegmentDict.has_key(itemlist[0]):
                            SegmentDict[itemlist[0]].append(itemlist[1:])
                    for keys in SegmentDict.keys():
                        SegmentDict[keys].sort(key=f)
                        typelist=''
                        number=0
                        end=0
                        writeitem=[]
                        for snplist in SegmentDict[keys]:
                            if len(snplist)==9:
                                if int(snplist[3])>end:
                                    if len(writeitem)!=0:
                                        #print str(number)
                                        writeitem.append(str(number))
                                        writeitem.append(str(number*100/total))
                                        writeitem.append(typelist)
                                        if number!=0:
                                            outputfile.write(trim(str(writeitem)))
                                    end=int(snplist[4])
                                    writeitem=snplist
                                    typelist=''
                                    number=0
                                else:
                                    if end<int(snplist[4]):
                                        end=int(snplist[4])
                                    writeitem[8]+=snplist[-1]
                                    writeitem[4]=snplist[4]
                                    writeitem[2]+="+"
                            elif int(repos(snplist[0:2])) <= end:
                                if TypeDict.has_key(snplist[-1]):
                                    TypeDict[snplist[-1]]+=1
                                else:
                                    TypeDict[snplist[-1]]=1
                                Totalname+=1
                                number=number+1
                                typefile1.write(trim(keys+"_"+repos(snplist[0:2])+'\t'+str(snplist[2:])))
                                if typelist.find(snplist[-1])==-1:
                                    typelist=typelist+','+snplist[-1]
                        if number>0:
                            writeitem.append(str(number))
                            writeitem.append(str(number*100/total))
                            writeitem.append(typelist)
                            outputfile.write(trim(str(writeitem)))
                    for key in TypeDict.keys():
                        typefile.write(key+'\t'+str(TypeDict[key])+'\t'+str(100.0*TypeDict[key]/Totalname)+'\n')
print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))
