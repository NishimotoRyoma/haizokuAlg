# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class ExamineKey:
    #This class examine whether the column is the primary key or not.
    
    def __init__(self,Column):
        #Colum : Series type or index of Dataframe
        self.Column = Column

    def examineUnique(self):
        #examine whether the value is unique or not
        if len(self.Column)==pd.Series.nunique(self.Column):
            return(1)
        else : return(0)
    
    def examineNull(self):
        #examine whther the column has Null or not
        if sum(self.Column.isnull())==0:
            return(1)
        else : return(0)

   
class ChoiceAlg:
    #This class is the choice algorithm.
    def __init__(self,M,choiceData,classData,res,R):
        #M : クラス定員
        #choice : 学生のアンケート結果
        #class : 講義表
        #res : 出力表
        #R : 何位まで見るか
        self.M=M
        self.R=R
        self.choice=choiceData
        self.classData=classData
        self.res=res
    
    def returnM(self):
        return self.M
        
    def returnChoiceData(self):
        return self.choice
    
    def returnClassData(self):
        return self.classData
        
    def returnRes(self):
        return self.res
        
    def mainAlg(self):
        choice2=self.choice
        class2=self.classData
        res2=self.res
        #selIndex = len(choice2.columns)
        #選択肢の最後まで見るのではなく、R-1位までに収まるように修正した。
        selIndex=self.R
        
        for i in range(selIndex):
            if (i+1) == selIndex : break
            for s in range(len(res2)):
                if(res2.iloc[s,2]==0):
                    res2.iloc[s,1]=choice2[choice2.iloc[:,0]==res2.iloc[s,0]].iloc[0,i+1]
                    res2.iloc[s,3]=i+1
                    
            for c in range(len(class2)):
                tempclass=class2.iloc[c,0]
                if class2[class2.iloc[:,0]==tempclass].iloc[0,2]==0:
                    tempres=res2[res2.iloc[:,1]==tempclass]
                    m = len(tempres)
                    
                    if m <= self.M:
                        res2.loc[(res2["class"]==tempclass),"onoff"]=1
                        if m ==M:
                            class2.iloc[c,2]=1 #fullflagを1にする
                            if i==0:
                                class2.iloc[c,3]=1 #rank1fullflagを1にする
                    
                    else :
                        tempres2=res2[res2.iloc[:,1]==tempclass]
                        tempres3=res2[res2.iloc[:,1]==tempclass][tempres2.iloc[:,2]==0]
                        m2 = len(res2[res2.iloc[:,1]==tempclass][tempres2.iloc[:,2]==1])
                        #m2=M-(今から取り出す人数)
                        tempid=tempres3.iloc[:,0].sample(n=M-m2)
                        for id in tempid:
                            res2.loc[(res2["id"]==id),"onoff"]=1
                        class2.iloc[c,2]=1 #fullflagを1にする
                        if i==0:
                            class2.iloc[c,3]=1 #rank1fullflagを1にする
                if(sum(res2.iloc[:,2])==len(res2)):
                    break
        resList=[res2,class2]
        return(resList)
            
            
class ModifySwap:
    def __init__(self,choiceData,classData,res):
        self.choiceD = choiceData
        self.classD = classData
        self.res = res

    def returnChoiceData(self):
        return self.choiceD
    
    def returnClassData(self):
        return self.classD
        
    def returnRes(self):
        return self.res
        
    def swap(self,id1,id2):
        #指定したid同士の配属をひっくり返して、rankを更新する
        #onoffは触っていないので注意
        if not(self.res.loc[self.res["id"]==id1,"class"].empty):
            if not(self.res.loc[self.res["id"]==id2,"class"].empty):
                  index1=self.res.loc[self.res["id"]==id1,"class"].index[0]
                  index2=self.res.loc[self.res["id"]==id2,"class"].index[0]
                  
                  temp=self.res.loc[self.res["id"]==id1,"class"][index1]
                  temp2=self.res.loc[self.res["id"]==id2,"class"][index2]
                  self.res.loc[self.res["id"]==id1,"class"]=temp2
                  self.res.loc[self.res["id"]==id2,"class"]=temp
                  
                  tempc1=self.choiceD.loc[self.choiceD.iloc[:,0]==id1]
                  tempc2=self.choiceD.loc[self.choiceD.iloc[:,0]==id2]
                  
                  f1=0;f2=0
                  for i in range(len(tempc1.iloc[0])):
                      if tempc1.iloc[0,i]==temp2:
                          self.res.loc[self.res["id"]==id1,"rank"]=i
                          f1=1
                      if tempc2.iloc[0,i]==temp:
                          self.res.loc[self.res["id"]==id2,"rank"]=i
                          f2=1
                      if f1*f2==1: break

                
class DoSwap:
    def __init__(self,choiceData,classData,res,R):
        self.choiceD = choiceData
        self.classD = classData
        self.res = res
        self.R = R
    
    def returnChoiceData(self):
        return self.choiceD
    
    def returnClassData(self):
        return self.classD
        
    def returnRes(self):
        return self.res
                        
    def swapAlg(self,s):
        #sはTrue or False
        #Trueならば1位で割り当てられた学生との交換を行い
        #Falseならば2位以上で割り当てられた学生との交換を行う。
        if s:
            SubRes=self.res.loc[(self.res["onoff"]==1)&(self.res["rank"]==1)]
        else:
            SubRes=self.res.loc[(self.res["onoff"]==1)&(self.res["rank"]>1)]
        
        nokoriRes=self.res.loc[(self.res["onoff"]==0)]
      
        for g in range(len(nokoriRes)):
            
            
            #現状の確定を差し引いた定員を求めてfullflagを更新する
            crossSum=pd.crosstab(self.res.loc[(self.res["onoff"]==1),:]["onoff"],
                                self.res.loc[(self.res["onoff"]==1),:]["class"])
        
            for cindex in range(len(self.classD)):
                cc=self.classD.iloc[cindex,0]
                if(not(crossSum.iloc[0,crossSum.columns==cc].empty)):
                    self.classD.loc[cindex,"残枠"]=M-crossSum.iloc[0,crossSum.columns==cc][0]
            self.classD.loc[self.classD["残枠"]==0,"fullflag"]=1
            
            #まだ空いている講義を出力する
            akiclass=self.classD.loc[self.classD["fullflag"]==0]
            #残っている学生のidを出力する
            gid=nokoriRes.iloc[g,0]
            gchoice=self.choiceD.loc[self.choiceD.iloc[:,0]==gid].iloc[0,2:self.R]
            FinishFlag=0
            #残り学生の選択を一つずつ見ていき、穏便に交換できそうなら交換する
            for gc in range(len(gchoice)):                
                tempchoice=gchoice.iloc[gc]
                yasasiigakusei=SubRes.loc[SubRes["class"]==tempchoice]
                if len(yasasiigakusei)>0:
                    yasasiichoice=self.choiceD[self.choiceD.iloc[:,0].isin(yasasiigakusei["id"])]
                    yasasiityuusen=yasasiigakusei["id"].sample(len(yasasiigakusei["id"]))
                    #抽選順に学生のアンケート結果を確認していき、akiclassを2~(R-1)位に書いていた場合
                    #学生同士でswapする
                    for yg in range(len(yasasiityuusen)):
                        ygid=yasasiityuusen.iloc[yg]
                        #akiclassを選んでいるかを見ていく
                        for ac in range(len(akiclass.iloc[:,0])):
                            ackey=akiclass.iloc[ac,0]
                            #見つけたら交換する
                            if sum(yasasiichoice.loc[yasasiichoice.iloc[:,0]==ygid].iloc[0,2:self.R]==ackey)>0:
                                if FinishFlag==0:
                                    if sum(self.choiceD.loc[self.choiceD.iloc[:,0]==gid].iloc[0,1:self.R]==self.res.loc[self.res["id"]==ygid,"class"].iloc[0])==1:
                                        if sum(self.choiceD.loc[self.choiceD.iloc[:,0]==ygid].iloc[0,1:self.R]==ackey)==1:
                                            self.res.loc[self.res["id"]==gid,"class"]=ackey
                                            swapins1=ModifySwap(self.choiceD,self.classD,self.res)
                                            swapins1.swap(gid,ygid)
                                            self.res=swapins1.returnRes()
                                            self.res.loc[self.res["id"]==gid,"onoff"]=1
                                            FinishFlag=1
                    
            

if __name__=="__main__":
    #Mはクラスの定員を指す。指定する必要がある。
    #定員が少ないと、遠くの順位が選ばれる学生が増える
    Txt = open("定員数.txt")
    M = Txt.read()
    Txt.close()
    M = int(M)
    
    Txt2 = open("順位.txt")
    R = Txt2.read()
    Txt2.close()
    R=int(R)
    R=R+1
    
    ClassFile = pd.read_csv("class.csv")
    ChoiceFile = pd.read_csv("choice.csv")
    
    E1 = ExamineKey(ClassFile.iloc[:,0])
    E2 = ExamineKey(ChoiceFile.iloc[:,0])
    if E1.examineUnique()==0:
        print("Error : クラスキーは一意でなければいけません。")
    if E1.examineNull()==0:
        print("Error : クラスキーに欠損値があってはいけません。")
    if E2.examineUnique()==0:
        print("Error : 学籍番号は一意でなければいけません。")
    if E2.examineNull()==0:
        print("Error : 学籍番号に欠損値があってはいけません。")
    
    if E1.examineUnique()*E1.examineNull()*E2.examineUnique()*E2.examineNull()>0:
        #primary keyに問題がなければ処理を実行する
        #ClassFileにfullflagを追加する
        #fullflagには定員に達した場合に1,そうじゃない場合は0を与えるフラグ
        ClassFile["fullflag"] =0
        ClassFile["rank1fullflag"]=0
        
        #出力される表としてresを与える
        #resについて
        #id : choiceから得られる学籍番号
        #class : 配属されるclass
        #onoff : 配属が決定した場合は1,そうじゃない場合は0となるフラグ
        #rank : 配置された選択肢の順位
        res = pd.DataFrame({"id" : ChoiceFile.iloc[:,0],
                            "class" : ChoiceFile.iloc[:,1]},columns=["id","class"])
        res["onoff"]=0
        res["rank"]=1
        
        tempclass=ChoiceAlg(M=M,R=R,choiceData=ChoiceFile,classData=ClassFile,res=res)
        AlgResList=tempclass.mainAlg()
        AlgRes=AlgResList[0]
        AlgCla=AlgResList[1]
        
        #現状の確定を差し引いた定員を求める
        AlgCla["残枠"]=M
        crossSum=pd.crosstab(AlgRes.loc[(AlgRes["onoff"]==1),:]["onoff"],
                                AlgRes.loc[(AlgRes["onoff"]==1),:]["class"])
        
        for cindex in range(len(AlgCla)):
            cc=AlgCla.iloc[cindex,0]
            if(not(crossSum.iloc[0,crossSum.columns==cc].empty)):
                AlgCla.loc[cindex,"残枠"]=M-crossSum.iloc[0,crossSum.columns==cc][0]

        Swap1=DoSwap(ChoiceFile,AlgCla,AlgRes,R)
        Swap1.swapAlg(False)
        Swa1Res=Swap1.returnRes() 
        Swa1Cla=Swap1.returnClassData()
        Swap2=DoSwap(ChoiceFile,Swa1Cla,Swa1Res,R)
        Swap2.swapAlg(True)
        Swa2Res=Swap2.returnRes() 
        Swa2Cla=Swap2.returnClassData()
        
        
        #もしこの交換でも割り振れない学生がいた場合(ほとんどあり得ないが)
        if not(Swa2Res.loc[Swa2Res["onoff"]==0].empty):
            muriID=Swa2Res.loc[Swa2Res["onoff"]==0,"id"]
            for muri in range(len(muriID)):
                murichoice=ChoiceFile.loc[ChoiceFile.iloc[:,0]==muriID.iloc[muri]]
                murichoiceSeq=murichoice.iloc[0,R:len(murichoice.iloc[0])]
                for muriseq in range(len(murichoiceSeq)):
                    kouho=murichoiceSeq.iloc[muriseq]
                    ####修正 #####
                    if sum(Swa2Cla.iloc[:,0]==kouho)!=1:
                        Swa2Res.loc[Swa2Res["id"]==muriID.iloc[muri],"onoff"]=-1
                    ##############
                    else:
                        if Swa2Cla.loc[Swa2Cla.iloc[:,0]==kouho,"fullflag"].iloc[0]==0:
                            if Swa2Res.loc[Swa2Res["id"]==muriID.iloc[muri],"onoff"].iloc[0]==0:
                                Swa2Res.loc[Swa2Res["id"]==muriID.iloc[muri],"class"]=kouho
                                #例外であることを示すためにonoff=-1としておく
                                Swa2Res.loc[Swa2Res["id"]==muriID.iloc[muri],"onoff"]=-1

                    
                    
        
        FCla=Swa2Cla
        FRes=Swa2Res
        
        #出力データの作成
        for cindex in range(len(FCla)):
            cc=FCla.iloc[cindex,0]
            writeData=FRes.loc[(FRes["class"]==cc),"id"]
            writeName=FCla.loc[(FCla["クラスキー"]==cc),"クラス名称"][cindex]+".csv"
            
            #writeData.to_csv(writeName,encoding="utf-8")
            writeData.to_csv(writeName,encoding="Shift-JIS")
        writeData=FRes
        writeName="割り当て.csv"
        #writeData.to_csv(writeName,columns=["id","class","rank"],encoding="utf-8")
        writeData.to_csv(writeName,columns=["id","class","rank"],encoding="Shift-JIS")
        
        if not(FRes.loc[FRes["onoff"]!=1].empty):
            writeName="例外処理学生につき要確認.csv"
            writeData=FRes.loc[FRes["onoff"]==-1]
            #writeData.to_csv(writeName,columns=["id","class","rank"],encoding="utf-8")
            writeData.to_csv(writeName,columns=["id","class","onoff","rank"],encoding="Shift-JIS")
