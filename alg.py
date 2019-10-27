# -*- coding: utf-8 -*-
import pandas as pd

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
    def __init__(self,M,choiceData,classData,res):
        #M : クラス定員
        #choice : 学生のアンケート結果
        #class : 講義表
        #res : 出力表
        self.M=M
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
        selIndex = len(choice2.columns)
        
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
                            class2.iloc[c,2]=1
                    
                    else :
                        tempres2=res2[res2.iloc[:,1]==tempclass]
                        tempres3=res2[res2.iloc[:,1]==tempclass][tempres2.iloc[:,2]==0]
                        m2 = len(res2[res2.iloc[:,1]==tempclass][tempres2.iloc[:,2]==1])
                        #m2=M-(今から取り出す人数)
                        tempid=tempres3.iloc[:,0].sample(n=M-m2)
                        for id in tempid:
                            res2.loc[(res2["id"]==id),"onoff"]=1
                        class2.iloc[c,2]=1
                if(sum(res2.iloc[:,2])==len(res2)):
                    break
        return(res2)
            
            
      


if __name__=="__main__":
    #Mはクラスの定員を指す。指定する必要がある。
    #定員が少ないと、遠くの順位が選ばれる学生が増える
    Txt = open("定員数.txt")
    M = Txt.read()
    Txt.close()
    M = int(M)
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
        
        tempclass=ChoiceAlg(M=M,choiceData=ChoiceFile,classData=ClassFile,res=res)
        
        AlgRes=tempclass.mainAlg()
        
        for cindex in range(len(ClassFile)):
            cc=ClassFile.iloc[cindex,0]
            writeData=AlgRes.loc[(AlgRes["class"]==cc),"id"]
            writeName=ClassFile.loc[(ClassFile["クラスキー"]==cc),"クラス名称"][cindex]+".csv"
            writeData.to_csv(writeName,encoding="Shift-JIS")
        writeData=AlgRes
        writeName="割り当て.csv"
        writeData.to_csv(writeName,columns=["id","class","rank"],encoding="Shift-JIS")