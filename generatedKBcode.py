#path=class.pykb
# -*- coding: CP1251 -*-
import os
import copy

class Property(object):
    '''����, ���� ����� ���������� ��'����'''
    
    def __init__(self,subj,name,inverseName='',functional=False,symmetric=False,transitive=False):
        '''�����������'''
        self.subj=subj # ���'��� ����������
        self.name=name # ����� ����������
        self.inverseName=inverseName # ����� �������� ����������
        self.functional=functional # ���������� �������������
        self.symmetric=symmetric # ���������� ����������
        self.transitive=transitive # ���������� �����������
        self.set=set() # ������� ������� ����������
        self.subj.__setattr__(self.name,self) # ���������� ������� ���������� ��� ���'����
        
    def add(self,*args):
        '''�������� ��'��� ��� ������ ��'���� � �������'''
        for obj in args: # ��� ��� ��'���� � args
            if self.functional: # ���� ���������� �������������
                self.set.clear() # �������� �������
                
# ���������� � ����� ���������
#            if self.inverseName!='': # ���� � �������� ����������
#                # �������� ���� � �������� ���������� ��'����
#                obj.__dict__[self.inverseName].set.add(self.subj)
#                    
#            if self.symmetric: # ���� ���������� ����������
#                # �������� ���� � ��������� ���������� ��'����
#                obj.__dict__[self.name].set.add(self.subj)
            
            self.set.add(obj) # �������� ��'��� � �������
        
    def get(self, showTransitive=False):
            '''������� ������� ������� ����������
            (showTransitive=True - ����������� ����������)'''
            def getTransitive(subj,s=set()):
                '''������� ������� ������� ����������� ����������. ����������'''
                if hasattr(subj, self.name): # ���� subj �� ������� self.name 
                    # ��� ��� ��'���� � ���������� � ������ self.name
                    for obj in subj.__dict__[self.name].set:
                        if obj not in s: # ���� obj ���� � ������ s
                            s.add(obj) # �������� ��'��� � �������
                            s=getTransitive(obj,s) # �������
                return s # ������� �������
            # ���� ���������� ����������� � ���������� ����������
            if self.transitive and showTransitive:
                # ������� ������� ����������� ����������
                s=getTransitive(self.subj)
                s.discard(self.subj) # �������� self.subj � �������, ���� �
                return s
            # ������ ��������� ������� ������� ����������
            else: return self.set
KB={} # ������� ���� �����
programDir="D:\!My_doc\Python_projects\TreePyKB"
#path=Base\class.pykb
#open=1
#fg=purple
#bg=white

class X(object):
    '''������� ���� ������㳿'''
    def __init__(self): # �����������
        # �� ���������� ���������� ���������� ��� ��'���� �� ��������� ������� ��������
        Property(subj=self,name='And') # ���������� 'And'
        Property(subj=self,name='Or') # ���������� 'Or'
        Property(subj=self,name='Not',symmetric=True) # ���������� 'Not'
        Property(subj=self,name='SubClassOf',transitive=True) # ���������� 'SubClassOf'
        self.doc="" # ������
KB[r"""Base"""]=X; del X
#path=Base\�������\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    '''����, ���� ����� ��������� �� �������'''
    def __init__(self): # �����������
        KB[r"""Base"""].__init__(self)
        # ���������� '� ����������'
        Property(subj=self,name='isReference',inverseName='hasReference')
KB[r"""Base\�������"""]=X; del X
#path=Base\���������\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    '''����, ���� ����� ���������'''
    def __init__(self, xy=None, relative=None, xName='x', yName='y'):
        KB[r"""Base"""].__init__(self)
        # ���������� '� ���������'
        Property(subj=self,name='isDependence',inverseName='hasDependence')
        self.xy=xy # ��� � ������ [(x1,y1),(x2,y2),(x3,y3)]
        self.relative=relative # ������� ��������� (������, ������, � ���������)
        self.xName=xName; self.yName=yName # ����� ����
    def plot(self):
        '''���� ������ ���������'''
        from matplotlib import rcParams, pyplot # �������� matplotlib
        rcParams['text.usetex']=False
        rcParams['font.sans-serif'] = ['Arial']
        rcParams['font.serif'] = ['Arial'] # ����� ��� ����� ��������
        x,y=[p[0] for p in self.xy],[p[1] for p in self.xy] # �������� ���
        pyplot.plot(x,y,'b-') #�����
        pyplot.title(unicode('')) # ���������
        pyplot.xlabel(unicode(self.xName)) # ������ �� x
        pyplot.ylabel(unicode(self.yName)) # ������ �� y
        pyplot.grid(True) # ����
        pyplot.show() # �������� �������
    def interp(self,x,reverse=False):
        '''��������� �������� Y ������ �������������
        ���� reverse=True, �� ��������� �������� X'''
        # ���� reverse=True, ������� X � Y ������
        if reverse: data=[(p[1],p[0]) for p in self.xy]
        else: data=self.xy
        lines=[] # ������ ��� ���������
        p1=data[0] # ����� �����
        for p2 in data[1:]: # ��� ��� ����� ��� �����
            lines.append((p1,p2)) # �������� ��� � ��� ������ �����
            p1=p2
        results=[] # ������ ����������    
        for line in lines: # ��� ��� ��� ���������
            # ���������� ����� ��
            x1,y1,x2,y2=line[0][0],line[0][1],line[1][0],line[1][1]
            if x>=x1 and x<=x2 or x<=x1 and x>=x2: # ���� x � ����� [x1,x2]
                results.append((x-x1)*(y2-y1)/(x2-x1)+y1) # ������ ����� �������� x � ���
        return results
KB[r"""Base\���������"""]=X; del X
#path=Base\������\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    def __init__(self):
        KB[r"""Base"""].__init__(self)
        # ���������� '��������'
        Property(subj=self,name='parameter')

KB[r"""Base\������"""]=X; del X

#path=Base\������\���� 13877-96\class.pykb
#open=1
#fg=purple
#bg=white

class X(KB[r"""Base\������"""]):
    def __init__(self):
        KB[r"""Base\������"""].__init__(self)
    def create(self):
        "�� ������� ��������� ��������� ���� ��������� ��'���� KB"
        
        self.d={ # ������� ������������ ���������
        'd_n':"������� ������ ����� �����",
        'd2_n':"������� ������ ����� �����",
        'd1_n':"�������� ������ ����� �����",
        'r_n':"����� ������� ����� �����",
        'dn':"������ ����� �����",
        'd1n':"������ ��������� ������� �����",
        'l1n':"������� �����",
        'l2n':"������� ��������� ������� �����",
        'l3n':"������� ����� ��� ����� �� ����",
        'l4n':"������� ����� � ������",
        'r3n':"����� ��������� ��������� ������� �����",
        'd_m':"������� ������ ����� �����",
        'd2_m':"������� ������ ����� �����",
        'd1_m':"�������� ������ ����� �����",
        'dm':"������� ������ �����",
        'd1m':"�������� ������ ������ ������� �����",
        'lm':"������� �����",
        'd0':"������ ��� ������",
        'p_n':"���� ����� �����",
        'p_m':"���� ����� �����"
        }
        
        self.p={ # ������� ����� ���������
        'delta_ln':"�������� ��������� ������� �����",
        'material1':"����� �������� � �������� ��������",
        'material2':"����� �������� � �������� ��������",
        'bolt_load':"������ ���������� ����� �� ��� ������������ (��)",
        'sigma1':"���������� � �� ������ ��� ����� 1 (��)",
        'sigma2':"���������� � �� ������ ��� ����� 2 (��)"
        }

    def createAbaqusModel(self):
        """C������ ������ Abaqus.
        ������� ���������� ���� � ������ ��� �������� �� ������� Abaqus.
        ������ ������ � Abaqus"""
        import os,pickle,tempfile,subprocess
        path=os.path.join(os.getcwd(), self.name) # ���� �� ��������
        data={'d':self.d,'p':self.p,'path':path}
        name=os.path.join(tempfile.gettempdir(),"data4AbaqusScript.tmp")
        f=open(name, "wb") #������� �������� ���� ��� ������
        pickle.dump(data,f) #�������������� ��� � ����
        f.close() #������� ����

        print "Abaqus CAE started. Please wait"
        # ������ ������ � Abaqus �� ���� ����������
        subprocess.Popen(r'C:\SIMULIA\Abaqus\6.11-3\exec\abq6113.exe cae noGUI=gost13877_96AbaqusMain.py').communicate()
        #os.system(r'start /WAIT abaqus cae noGUI=gost13877_96Abaqus.py')
        print "Abaqus CAE finished"

    def createSWModel(self):
        "������� ������ SolidWorks"
        pass
    def runAbaqusModel(self):
        "��������� ������ Abaqus"
        pass
    def getAbaqusModelResults(self):
        "������� ���������� � ����� Abaqus"
        pass
KB[r"""Base\������\���� 13877-96"""]=X; del X

#path=Base\������\���� 13877-96\�� 19\class.pykb
#open=1
#fg=purple
#bg=white

class X(KB[r"""Base\������\���� 13877-96"""]):
    def __init__(self):
        KB[r"""Base\������\���� 13877-96"""].__init__(self)
    def create(self):
        "�� ������� ��������� ��������� ���� ��������� ��'���� KB"
        KB[r"""Base\������\���� 13877-96"""].create(self)
        
        d={
        'd_n':(27, -0.48, -0.376),
        'd2_n':(25.35, -0.204, -0.047),
        'd1_n':(24.25, 0, -0.415),
        'r_n':(0.28, 0, 0.08),
        'dn':(38.1, -0.25, 0.13),
        'd1n':(23.24, -0.13, 0.13),
        'l1n':(36.5, 0, 1.6),
        'l2n':(15, 0.2, 1),
        'l3n':(32, 0, 1.5),
        'l4n':(48, -1, 1.5),
        'r3n':(3, 0, 0.8),
        'd_m':(27, 0, 0.27),
        'd2_m':(25.35, 0, 0.202),
        'd1_m':(24.25, 0, 0.54),
        'dm':(41.3, -0.25, 0.13),
        'd1m':(27.43, 0, 0.25),
        'lm':(102, -1, 1),
        'd0':(19.1,-0.41,0.2),
        'p_n':(2.54,0,0),
        'p_m':(2.54,0,0)
        }
        
        for k in d:
            self.d[k]=[self.d[k]]+list(d[k])
         
        p={
        'delta_ln':0,
        'material1':"40fesafe",
        'material2':"40fesafe",
        'bolt_load':-0.1,
        'sigma1':1,
        'sigma2':170.0e+6
        }
        
        for k in p:
            self.p[k]=[self.p[k]]+[p[k]]
       
KB[r"""Base\������\���� 13877-96\�� 19"""]=X; del X

#path=Base\������\���� 13877-96\�� 22\class.pykb
#open=1
#fg=purple
#bg=white

#path=Base\��������\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    "���� ����� ������� ������"
    def __init__(self):
        KB[r"""Base"""].__init__(self)
    def create(self,doc,n,ei,es,v):
        "������� ��'���"
        self.doc=doc #������
        self.n=n #���������� �����
        self.ei=ei #���� ���������
        self.es=es #����� ���������
        self.v=v #����� ��������
    def min(self):
        "������� ��������� �����"
        return self.n+self.ei
    def max(self):
        "������� ������������ �����"
        return self.n+self.es

KB[r"""Base\��������"""]=X; del X

#path=Base\����\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    '''����, ���� ����� ���� (�������) � ������
    ���'���-��������-��'���'''
    def __init__(self): # �����������
        KB[r"""Base"""].__init__(self)
        # ���������� '�� ���������'
        Property(subj=self,name='hasReference',inverseName='isReference')
        # ���������� '�� ���������'
        Property(subj=self,name='hasDependence',inverseName='isDependence')
    def create(self,subjName,propName,objName):
        self.subjName=subjName # ����� ���'����
        self.propName=propName # ����� ��������� (����������)
        self.objName=objName # ����� ��'����
        # �������� �������� � ����������, ���� ����
        KB[self.subjName].__dict__[self.propName].add(KB[self.objName])

KB[r"""Base\����"""]=X; del X
#path=Base\������\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]): # ��������� ���� Base 
    '''����, ���� ����� ������'''
    def __init__(self): # �����������
        KB[r"""Base"""].__init__(self)
        # ����������� ���������� '� ��������'
        Property(subj=self,name='isCause',inverseName='isEffect',transitive=True)
        # ����������� ���������� '� ��������' 
        Property(subj=self,name='isEffect',inverseName='isCause',transitive=True)
KB[r"""Base\������"""]=X; del X

#path=Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������"""]=KB[r"""Base\�������"""]()

#path=Base\������\���� 13877-96\�� 19\bolt_load\class.pykb
#open=1
#fg=blue
#bg=white

#path=Base\������\���� 13877-96\�� 19\bolt_load\0.1\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\���� 13877-96\�� 19\bolt_load\0.1"""]=KB[r"""Base\������\���� 13877-96\�� 19"""]()

#path=Base\������\���� 13877-96\�� 19\bolt_load\0.1\delta_ln\class.pykb
#open=1
#fg=blue
#bg=white

#path=Base\������\���� 13877-96\�� 19\bolt_load\0.1\delta_ln\10\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\���� 13877-96\�� 19\bolt_load\0.1\delta_ln\10"""]=KB[r"""Base\������\���� 13877-96\�� 19"""]()

#path=Base\������\���������� ���������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ ������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\������ ������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ ������\�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\������ ������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ ������\�����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\������ ������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\������ �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\����������� �� ��������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\������ �����\����������� �� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\������� ������� ���������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\������� ������� ���������\�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\������� ������� ���������\����������� ������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\����������� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\������� ������� ���������\���������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\������� ����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\������ �����\������� ����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\������� ����\�����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\������ �����\������� ����\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\������ �����\��������� �� ��������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\������ �����\��������� �� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�������\� �������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�������\� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�������\� �������\��������� ������������ ������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�������\� �������\��������� ������������ ������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�������\� �������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�������\� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�������\� �������\� �������� ���������� �'�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

# ����:
KB[r"""Base\������\���������� ���������\�������\� �������\� �������� ���������� �'�������"""]=KB[r"""Base\����"""]()

#path=Base\������\���������� ���������\�������\����������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�������\���������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\³�������� ������� �� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\³�������� ������� �� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\³�������� ������� �� �����\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\³�������� ������� �� �����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\ĳ����� ��������� �������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\ĳ����� ��������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\ĳ����� ��������� �������\�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\ĳ����� ��������� �������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\ĳ����� ��������� �������\�����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\ĳ����� ��������� �������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\ĳ����� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\ĳ����� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\ĳ����� �����\�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\ĳ����� �����\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\ĳ����� �����\�������\� �������������� ���������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\ĳ����� �����\�������\� �������������� ���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� �����\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\������� �����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� ������� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\������� ������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� ������� �����\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\������� ������� �����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� ��������� �������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\������� ��������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� ��������� �������\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\������� ��������� �������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� ������������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\������� ������������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� ������������\����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\������� ������������\����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\���� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\���� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\���� �����\�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\���� �����\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\���� �����\�����������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\���� �����\�����������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\��� �������\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\��� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\��� �������\�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\��� �������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\��� �������\�����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\��� �������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\���������� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\���������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\���������� �����\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\���������� �����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\���������� �����\����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\���������� �����\����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\����� ������ �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\����� ������ �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\����� ������ �����\���������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\����� ������ �����\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\��������� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\��������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\��������� �����\�������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\��������� �����\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\��������� �����\�����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\��������� �����\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� �����\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\�����\������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� �����\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\������� �����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\�����\������� �����\����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\�����\������� �����\����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\���������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\������\���������� ���������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\���������\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\���������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\���������\������\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\���������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ���������\���������\������\������� ����\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\������\���������� ���������\���������\������\������� ����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\������������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\������������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\����\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\����\���� �� ���������\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\����\���� �� ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�����\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�����\����� �������-������\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�����\����� �������-������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�����\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�������� �������\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�������� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�'������� �����\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�'������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�'������� �����\���� �������\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1

KB[r"""Base\������\�����\�'������� �����\���� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�'������� ����� � ������\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�'������� ����� � ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�'������� ����� � ������\� ���������� ������\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�'������� ����� � ������\� ���������� ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�'������� ����� � ������\� ��������� ������\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�'������� ����� � ������\� ��������� ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�������� ��������\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�������� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\������������ ������������� ����������\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\������������ ������������� ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\����������\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�������� �����\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�����\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����\�����\� ��������������� ����\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1

KB[r"""Base\������\�����\�����\� ��������������� ����"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�����\��������\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1

KB[r"""Base\������\�����\�����\��������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�����\��������\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1

KB[r"""Base\������\�����\�����\��������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�������\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\������\�����\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\���������\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�����\����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\���������\�����\����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\�'��������� �������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\���������\�'��������� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�'��������� �������\����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\���������\�'��������� �������\����"""]=KB[r"""Base\������"""]()

#path=Base\������\������� �������� ��������� ��������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\���� ����������� ������� � ���������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\���� ����������� ������� � ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\���� ���������� �������㳿\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\���� ���������� �������㳿"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\���������� ������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\���������� ������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\���������� ���������������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\���������� ���������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\������ �� ��������-�������� � ���������� ����������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\������ �� ��������-�������� � ���������� ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\������ �� ���������� ����������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\������ �� ���������� ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\������ �� ���������� ����������� �������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\������ �� ���������� ����������� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\������ �� ����������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\������ �� ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\������ ��� ��������������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\������ ��� ��������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\��������� ������������ ���������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\��������� ������������ ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\��������� ���������� ����������� �����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\��������� ���������� ����������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\ϳ��� �������� � ������������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\ϳ��� �������� � ������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\������������ �����������������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\������������ �����������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������� �������� ��������� ��������\����������� ����� ���������� �����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������� �������� ��������� ��������\����������� ����� ���������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�������� ����������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\�������� ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������� ����������\�������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\�������� ����������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������� ����������\�������\���������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�������� ����������\�������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������� ����������\������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\�������� ����������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������� ����������\������\�� ������ �����������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�������� ����������\������\�� ������ �����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\�������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������������\�����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�������������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�������������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\��������\³��������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\��������\³��������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\��������� ��������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\��������\��������� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\����� � �������� ��������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\����� � �������� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\������������ ��������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\������������ ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\��������� �������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\��������� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\����� �������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\����� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\����� �������\�����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\����� �������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\����� �������\�������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\����� �������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����������� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\г����\����������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\г����\���\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\���"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������ ������� ������ ����� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������ ������� ������ ����� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\ʳ������ ������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\ʳ������ ������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\ʳ������ ������\�������������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\ʳ������ ������\�������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\ʳ������ ������\�����������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\ʳ������ ������\�����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����\������ ����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����\������ ����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����\����������� ����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����\����������� ����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\г����\������ �������� ��\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������ �������� ��"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������ �������� ��\˳��\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������ �������� ��\˳��"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������ �������� ��\�����\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������ �������� ��\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������ ������� ����� ����� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������ ������� ����� ����� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������� �����\�������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������� �����\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������� �����\��������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������� �����\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������� �����\��������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������� �����\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������� �����\ϳ�����\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������� �����\ϳ�����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�������� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�������� �����\����� ����� �����\class.pykb
#open=1
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\г����\�������� �����\����� ����� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\г����\�����������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�����������\��������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�����������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�����������\����������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�����������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�����������\������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�����������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\���������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\���������\��������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\���������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\���������\�������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\���������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������� ������� ����� ����� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������� ������� ����� ����� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\������� ������ ����� ����� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\������� ������ ����� ����� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�����\��� ������ ����� ����� �����\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�����\��� ������ ����� ����� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����� �������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����� �������\������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����� �������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����� �������\����������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����� �������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����� �������\����������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����� �������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����� �������\�������������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����� �������\�������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����� �������\��������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����� �������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\����� �������\������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\����� �������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�������� �������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�������� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�������� �������\������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�������� �������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\г����\�������� �������\����������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\г����\�������� �������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\������������ ������� ������� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\������������ ������� ������� �����"""]=KB[r"""Base\������"""]()

#92
#path=Base\������\������������ ��������\������������ ������� ������� �����\³��� ����� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\������������ ������� ������� �����\³��� ����� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\������������ ������� ������� �����\г���� ����� �������� � �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\������������ ������� ������� �����\г���� ����� �������� � �����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\����� ������� �����\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\����� ������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ��������\����� ������� �����\����������� �������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\����� ������� �����\����������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\����� ������� �����\����������\class.pykb
#open=1
#fg=blue
#bg=yellowgreen

KB[r"""Base\������\������������ ��������\����� ������� �����\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ��������\��������� ��������\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\������\������������ ��������\��������� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ���������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������������ ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ���������\���������� ������������ �� ������ �����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������ ���������\���������� ������������ �� ������ �����\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ���������\������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\������������ ���������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ���������\ϳ� �������� �����\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\������������ ���������\ϳ� �������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\������������ ���������\ϳ� �������� �����\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\������������ ���������\ϳ� �������� �����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\̳�����"""]=KB[r"""Base\������"""]()
#path=Base\������\̳�����\�� ��������� ������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\�� �������� ������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� �������� ������������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\�� ���������� ������������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� ���������� ������������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\�� ���������� ������������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� ���������� ������������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\�� ���������� ������������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� ���������� ������������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\�� ��������� ������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\�� ��������� ������������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\�� ��������� ������������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\̳�����\������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\̳�����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\����"""]=KB[r"""Base\������"""]()

#path=Base\������\����\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\����\����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����\����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\���������� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ������\����� ������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\���������� ������\����� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������� ������\��� ������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\���������� ������\��� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������ ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������ ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������ ������\�����\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������ ������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\�����볺� ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\�����볺� ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������ �����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������ �����"""]=KB[r"""Base\������"""]()

r"""http://ru.wikipedia.org/wiki/%D0%91%D0%B5%D1%81%D1%81%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D1%82%D0%B0%D0%BB%D1%8C"""

#path=Base\������\�������\��������� ���� �����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\��������� ���� �����"""]=KB[r"""Base\������"""]()
#142
#path=Base\������\�������\��������� ���� �����\������� ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\������� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\������� ������\1100-1400\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\������� ������\1100-1400"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\������� ������\1100-1600\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\������� ������\1100-1600"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\������� ������\1800-2100\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\������� ������\1800-2100"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\�� ������� ������� ������������ � ����������� ����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\�� ������� ������� ������������ � ����������� ����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\��������� �������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\��������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\�������� ������� ��������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\�������� ������� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\�����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\�����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\���������� ������� ������� ����������� ����� � ���������� ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\���������� ������� ������� ����������� ����� � ���������� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\�����07�16�6\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\�����07�16�6\������� �������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6\������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\�����1�15�4��3-�\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\�����1�15�4��3-�"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ���� �����\�����1�15�4��3-�\������� �������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ���� �����\�����1�15�4��3-�\������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������� � ����������� �����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������� � ����������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������� � ����������� �����\���������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������� � ����������� �����\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������� � ����������� �����\�������������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������� � ����������� �����\�������������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������� � ����������� �����\�����������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������� � ����������� �����\�����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������� ������ ���� �� �������� �����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������� ������ ���� �� �������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������� ���\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������� ���"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������� ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������� ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������� ������\������ ������ �����������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������� ������\������ ������ �����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\���������� ������� ����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\���������� ������� ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\���������� ������� ����������\�����\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\���������� ������� ����������\�����"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\���������� ������� ����������\�����\�������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\���������� ������� ����������\�����\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������ ��������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������ ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������ ��������\����\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������ ��������\����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������ ����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������ ����"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\��������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������"""]=KB[r"""Base\������"""]()

r"""http://ru.wikipedia.org/wiki/%D0%A5%D1%80%D1%83%D0%BF%D0%BA%D0%BE%D1%81%D1%82%D1%8C"""

#path=Base\������\�������\������� ����������� ���\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������� ����������� ���"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\�������� � ������������� ���������� � ����� �����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\�������� � ������������� ���������� � ����� �����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\�������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\ͳ���\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\ͳ���"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������ ����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������ ����"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\��������� ��������� ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\��������� ��������� ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\�������� �����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\�������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\�������� �������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\�������� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\�����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\�����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\�����������\������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\�����������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\�����������\������\�����\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\�����������\������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\�����������\������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\�����������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������ ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������ ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������ ��������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������ ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������ ��������\������������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������ ��������\������������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������ ��������\��������� �����\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������ ��������\��������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������ ��������\г�� ������� ���������� ����� � �����\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������ ��������\г�� ������� ���������� ����� � �����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������� ����\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������� ����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������� ����\���������������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������� ����\���������������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ��������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� ��������\����������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� ��������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������\� ������� ��������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������\� ������� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������\³�����\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������\³�����"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������\³�����\��������� ����������� �������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������\³�����\��������� ����������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������\³�����\���������� ���� ����������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������\³�����\���������� ���� ����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������\����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������\����������\������� ��� ���������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������\����������\������� ��� ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������\������������ ���������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������\������������ ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������\ճ���-������� �������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������������\ճ���-������� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������������\ճ���-������� �������\����������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������\ճ���-������� �������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\������������\ճ���-������� �������\����������\������� ������ ������������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\������������\ճ���-������� �������\����������\������� ������ ������������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\���������� ������� ��������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\���������� ������� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\������� ������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\������� ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\����������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\��������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\��������������\������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\��������� �� ������������ ���������\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\������\�������\��������� �� ������������ ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\�������\��������� �� ������������ ���������\������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\��������� �� ������������ ���������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\����������� ���\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\����������� ���"""]=KB[r"""Base\������"""]()

#path=Base\������\�������\����������� ���\�������\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\������\�������\����������� ���\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\³������\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\³������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\��������\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\�������\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������\�������������\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\������\�������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������\��������������\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\������\��������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������\�������\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������\������\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\������\������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\��������\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������������\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\������������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\������������\���������\class.pykb
#open=1
#fg=blue
#bg=gold2

KB[r"""Base\������\������������\������������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������\����\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\����\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\������\������������\����"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\�������\class.pykb
#open=0
#fg=blue
#bg=gold2

KB[r"""Base\������\������������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\������������\��������\class.pykb
#open=0
#fg=blue
#bg=gold2

KB[r"""Base\������\������������\��������"""]=KB[r"""Base\������"""]()

#path=Base\������\������������\��������\��������������� �����\class.pykb
#open=1
#fg=blue
#bg=gold2

KB[r"""Base\������\������������\��������\��������������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\�����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\�����\���������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������\�����\���������"""]=KB[r"""Base\������"""]()

r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#18"""
#path=Base\������\����������\����\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\����������\����"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\����\���������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������\����\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\��������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\����������\��������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\��������\���������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������\��������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\�������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\����������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\�������\�����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������\�������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\�������\�����\���������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������\�������\�����\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\��������\������������ ���-�����\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\������������ ���-�����"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\������������ ���-�����, ����\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\������������ ���-�����, ����"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\������������� �������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\������������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\���������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\��������\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\��������\���쳺�� � �������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\���쳺�� � �������������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\������������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\��������\������������"""]=KB[r"""Base\������"""]()
#path=Base\������\��������\̳���\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\̳���"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\ͳ������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\ͳ������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\�������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\������� ����������� � �������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\������� ����������� � �������������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\������� � ������ �������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\������� � ������ �������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\����'���\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\����'���"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\����������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\���������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\��������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\��������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\�����\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\��������� �� ��� ��������� ��������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\��������� �� ��� ��������� ��������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\��������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\��������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\�������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������\������� � �������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\��������\������� � �������������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\³� ���������������� ������������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\³� ���������������� ������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ ������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\������ ������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ ������\� ���������� ����� �����\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\������ ������\� ���������� ����� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ ������\� ������� ����� �����\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\������ ������\� ������� ����� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ ������\ϳ� �������� �����\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\������ ������\ϳ� �������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\�������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\�������\���������\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\�������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\��������� ����������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\��������� ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\��������� ����������\���������� ��� �����\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\��������� ����������\���������� ��� �����\���������\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\��������� ����������\��� �����\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\��������� ����������\��� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\��������� ����������\��� �����\���������\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\��������� ����������\��� �����\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\��������� ����������\��� �������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\��������� ����������\��� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\��������� ����������\��� �������\���������\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\��������� ����������\��� �������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\��������� ����������\����� �������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\��������� ����������\����� �������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\����������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\���������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\�������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\��������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\���������\class.pykb
#open=0
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\����\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\����\�������������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����\�������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\�������-���������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����\�������-���������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\����\�����������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\����\�����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\��������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\��������\������\class.pykb
#open=0
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\��������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\�������� �������������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\�������� �������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������� ����\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\������� ����"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������� ����\���������� ������ ����������\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������� ����\���������� ������ ����������\������\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\������� ����\���������� ������ ����������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\���������������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\���������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\���������������\����������\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\���������������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\�����������������\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\������\�����������\�����������������"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\�����������������\���������\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\������\�����������\�����������������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������� ��� ��������������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\����������� ��� ��������������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������� ��� ��������������\���������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������� ��� ��������������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\��������� �����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\��������� �����"""]=KB[r"""Base\������"""]()

#path=Base\������\�������� �'�������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\�������� �'�������"""]=KB[r"""Base\������"""]()

#path=Base\������\�������� �'�������\������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\�������� �'�������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\���������� ������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\����������\���������� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\��������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\����������\��������"""]=KB[r"""Base\������"""]()

#path=Base\������\����������\��������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\����������\��������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\������������ � �������� ����\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\������������ � �������� ����"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\���������� �������� ������� ��������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\���������� �������� ������� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�������� �����������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\�������� �����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�������� �����������\�������� �� ����������� �����\class.pykb
#open=1
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\�������� �����������\�������� �� ����������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�������� �����������\�������� �� ����� ��������\class.pykb
#open=1
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\�������� �����������\�������� �� ����� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�������� �����������\�������� �� �������� ������������\class.pykb
#open=1
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\�������� �����������\�������� �� �������� ������������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\������ ������������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\������ ������������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\������ ������������\�������������\class.pykb
#open=0
#fg=blue
#bg=burlywood1

KB[r"""Base\������\���������\������ ������������\�������������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\������ ������������\�������������\�������\class.pykb
#open=1
#fg=blue
#bg=burlywood1

KB[r"""Base\������\���������\������ ������������\�������������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\������ ������������\�������������\�����\class.pykb
#open=1
#fg=blue
#bg=burlywood1

KB[r"""Base\������\���������\������ ������������\�������������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\������ ������������\�����������\class.pykb
#open=0
#fg=blue
#bg=burlywood1

KB[r"""Base\������\���������\������ ������������\�����������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\�������� �����\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\�������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\�������� ��������� ������������ ������ �����\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\�������� ��������� ������������ ������ �����"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\������� ������������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\������� ������������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\���������� ���������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\���������� ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ��� �����������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\����� ��� �����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\��������� ��������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\��������� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\Գ������ ����� ��� �����������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\Գ������ ����� ��� �����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������ ��������������\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\������\���������\����� ������������ ��������������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\�������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\���������\�������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\����\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\���������\����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\���������\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\������\���������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\�����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\̳�������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\̳�������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\̳�������\-196\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\̳�������\-196"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\�����������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\�����������\150\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������\150"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ �����������\�����������\200\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������\200"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ �����������\�����������\300\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������\300"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ �����������\�����������\350-550\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������\350-550"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\�����������\400\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������\400"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\������ �����������\�����������\600\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������\600"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ �����������\�����������\900\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\�����������\900"""]=KB[r"""Base\������"""]()
#path=Base\������\�����������\������ �����������\������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����������\������ �����������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\����������� �� ���������� ����������� ������\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\�����������\����������� �� ���������� ����������� ������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����������\����������� �� ���������� ����������� ������\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�����������\����������� �� ���������� ����������� ������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\������\�����"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�� ����\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����\�� ����"""]=KB[r"""Base\������"""]()
#345
#path=Base\������\�����\�� ����\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�����\�� ����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�� ����\����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�����\�� ����\����"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�� �������� ����\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\������\�����\�� �������� ����"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�� �������� ����\������\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�����\�� �������� ����\������"""]=KB[r"""Base\������"""]()

#path=Base\������\�����\�� �������� ����\����\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\������\�����\�� �������� ����\����"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\���������� �������� � �����������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\���������� �������� � �����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\���������� ���������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\���������� ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\���������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\ʳ������ ��������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\ʳ������ ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\̳�������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\̳�������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\����������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\�������� ��������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\�������� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\������� ���������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\������� ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�����������\������� �����������\class.pykb
#open=0
#fg=blue
#bg=mistyrose

KB[r"""Base\������\���������\����� ������������\�����������\������� �����������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\����� ������������\�����������\������� �����������\������\class.pykb
#open=1
#fg=blue
#bg=mistyrose

KB[r"""Base\������\���������\����� ������������\�����������\������� �����������\������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\����� ������������\�����������\��������������� ���������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�����������\��������������� ���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\�������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\���������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\���������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\���������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\̳�������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\̳�������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\��������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\������������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\������������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\г�����\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\г�����"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\�������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\�������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\��������\����������\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\��������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\�������� �������������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\�������� �������������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\����������� ���� ��������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\����������� ���� ��������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\ϳ������������ �������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\ϳ������������ �������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\����� ������������\����������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\����� ������������\����������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\��������� ��������� ������ ����������� �����\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\��������� ��������� ������ ����������� �����"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\������ �������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\������ �������"""]=KB[r"""Base\������"""]()
#path=Base\������\���������\������ �������\���������\class.pykb
#open=1
#fg=blue
#bg=mistyrose

KB[r"""Base\������\���������\������ �������\���������"""]=KB[r"""Base\������"""]()

#path=Base\������\���������\���������� �������\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\������\���������\���������� �������"""]=KB[r"""Base\������"""]()

#path=Base\������\���� 13877-96\�� 19\bolt_load\0.1\delta_ln\10\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���� 13877-96\�� 19\bolt_load\0.1\delta_ln\10"""].create()
KB[r"""Base\������\���� 13877-96\�� 19\bolt_load\0.1\delta_ln\10"""].p['bolt_load'][1]=-0.1
KB[r"""Base\������\���� 13877-96\�� 19\bolt_load\0.1\delta_ln\10"""].p['delta_ln'][1]=10

#path=Base\������\���� 13877-96\�� 19\bolt_load\0.1\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���� 13877-96\�� 19\bolt_load\0.1"""].create()
KB[r"""Base\������\���� 13877-96\�� 19\bolt_load\0.1"""].p['bolt_load'][1]=-0.1
#path=Base\������\���������� ���������\������ ������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\������ ������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\�������\� �������"""])

#path=Base\������\���������� ���������\������ ������\�����\prop.pykb
#open=0
#fg=red
#bg=white
KB[r"""Base\������\���������� ���������\������ ������\�����"""].__dict__["isEffect"].add(KB[r"""Base\������\���������\���������� ���������"""])

KB[r"""Base\������\���������� ���������\������ ������\�����"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\������ ������\�������"""])

#path=Base\������\���������� ���������\������ �����\������� ������� ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����"""])

r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#17"""

KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

#path=Base\������\���������� ���������\������ �����\������� ������� ���������\����������� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\����������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\���������� ���������\������ �����\������� ������� ���������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\���������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\�������"""])

KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\���������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������"""])

#path=Base\������\���������� ���������\������ �����\������� ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\������ �����\������� ����"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����"""])

r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#17"""

KB[r"""Base\������\���������� ���������\������ �����\������� ����"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\������ �����\������� ����\�����"""])

#path=Base\������\���������� ���������\������ �����\��������� �� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\������ �����\��������� �� ��������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\������ �����\����������� �� ��������"""])

KB[r"""Base\������\���������� ���������\������ �����\��������� �� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\���������� ���������\������ �����\��������� �� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

#path=Base\������\���������� ���������\�������\� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�������\� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�������� �'�������"""])

#path=Base\������\���������� ���������\�������\� �������\��������� ������������ ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�������\� �������\��������� ������������ ������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\���������� ���������\�������\� �������\��������� ������������ ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])


KB[r"""Base\������\���������� ���������\�������\� �������\��������� ������������ ������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\������"""])

#path=Base\������\���������� ���������\�������\� �������\prop.pykb
#open=0
#fg=red
#bg=white

X=KB[r"""Base\������\���������� ���������\�������\� �������"""]
X.__dict__["isCause"].add(KB[r"""Base\������\�������� �'�������\������"""])


KB[r"""Base\������\���������� ���������\�������\� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\���������� ���������\�������\� �������"""].__dict__["isCause"].add(KB[r"""Base\������\���������\������ ������������\�������������\�������"""])

#path=Base\������\���������� ���������\�������\� �������\� �������� ���������� �'�������\prop.pykb
#open=0
#fg=red
#bg=white

# ���������� �����:
X=KB[r"""Base\������\���������� ���������\�������\� �������\� �������� ���������� �'�������"""]
X.create(
r"""Base\������\���������� ���������\�������\� �������""",
'isCause',
r"""Base\������\�������� �'�������\������"""
)

X.__dict__["hasReference"].add(KB[r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������"""])
del X

# ���������� �'������� ������������� �� ������� ������ �� ���������� �������
# ���������:
r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#9"""


#path=Base\������\���������� ���������\�������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\���������� ���������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\������"""])

#path=Base\������\���������� ���������\�������\���������\prop.pykb
#open=0
#fg=red
#bg=white
KB[r"""Base\������\���������� ���������\�������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\�������� �'�������\������"""])

#path=Base\������\���������� ���������\�����\³�������� ������� �� �����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\³�������� ������� �� �����\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����"""])

#path=Base\������\���������� ���������\�����\ĳ����� ��������� �������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\ĳ����� ��������� �������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

KB[r"""Base\������\���������� ���������\�����\ĳ����� ��������� �������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\���������� ���������\�����\ĳ����� ��������� �������\�������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\�����\ĳ����� ��������� �������\�����"""])

#path=Base\������\���������� ���������\�����\ĳ����� ��������� �������\�����\prop.pykb
#open=0
#fg=red
#bg=white

#path=Base\������\���������� ���������\�����\ĳ����� �����\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\ĳ����� �����\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����\���������"""])

#path=Base\������\���������� ���������\�����\ĳ����� �����\�������\� �������������� ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\ĳ����� �����\�������\� �������������� ���������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\���������� ���������\�����\������� �����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\������� �����\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#91

KB[r"""Base\������\���������� ���������\�����\������� �����\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����\���������"""])

#path=Base\������\���������� ���������\�����\������� ������� �����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\������� ������� �����\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\ϳ� �������� �����\������"""])
#132
#path=Base\������\���������� ���������\�����\������� ��������� �������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\������� ��������� �������\������"""].__dict__["isCause"].add(KB[r"""Base\������\���������\�����\����"""])

#path=Base\������\���������� ���������\�����\������� ������������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\������� ������������\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])
#137
#path=Base\������\���������� ���������\�����\���� �����\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\���� �����\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����\���������"""])

#path=Base\������\���������� ���������\�����\���� �����\�����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\���� �����\�����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\���������� ���������\�����\��� �������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\��� �������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����"""])

KB[r"""Base\������\���������� ���������\�����\��� �������\�������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\�����\��� �������\�����"""])

#path=Base\������\���������� ���������\�����\��� �������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\��� �������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])
#95

KB[r"""Base\������\���������� ���������\�����\��� �������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])

#path=Base\������\���������� ���������\�����\���������� �����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\���������� �����\������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])
#163
#path=Base\������\���������� ���������\�����\���������� �����\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\���������� �����\����"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\�����\���������� �����\������"""])

KB[r"""Base\������\���������� ���������\�����\���������� �����\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])

#path=Base\������\���������� ���������\�����\����� ������ �����\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\����� ������ �����\���������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������\������"""])


KB[r"""Base\������\���������� ���������\�����\����� ������ �����\���������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\������"""])

#path=Base\������\���������� ���������\�����\��������� �����\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\��������� �����\�������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\�����\��������� �����\�����"""])

KB[r"""Base\������\���������� ���������\�����\��������� �����\�������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ������\����� ������"""])

KB[r"""Base\������\���������� ���������\�����\��������� �����\�������"""].__dict__["isCause"].add(KB[r"""Base\������\����\������"""])

#path=Base\������\���������� ���������\�����\������� �����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\������� �����\������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

KB[r"""Base\������\���������� ���������\�����\������� �����\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

KB[r"""Base\������\���������� ���������\�����\������� �����\������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\�����\������� �����\����"""])

#path=Base\������\���������� ���������\�����\������� �����\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\�����\������� �����\����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ��������\г����\����� �������\������"""])
#161
#path=Base\������\���������� ���������\���������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\���������\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������"""])

KB[r"""Base\������\���������� ���������\���������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\���������� ���������\���������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������"""])

KB[r"""Base\������\���������� ���������\���������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\���������� ���������\���������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\���������\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\������"""])

KB[r"""Base\������\���������� ���������\���������\������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ���������\���������\������"""])

KB[r"""Base\������\���������� ���������\���������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������\���������"""])

#path=Base\������\���������� ���������\���������\������\������� ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ���������\���������\������\������� ����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\������"""])

KB[r"""Base\������\���������� ���������\���������\������\������� ����"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\��������\������"""])

KB[r"""Base\������\������������"""].__dict__["Not"].add(KB[r"""Base\������\������������\������"""])

#path=Base\������\������������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\���������������"""])

#path=Base\������\�����\����\���� �� ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\����\���� �� ���������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\����\���������"""])
r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#22"""
#path=Base\������\�����\�����\����� �������-������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�����\����� �������-������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])
#99
#path=Base\������\�����\�������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

KB[r"""Base\������\�����\�������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\������� �������� ��������� ��������\��������� ���������� ����������� �����"""])

#path=Base\������\�����\�'������� �����\���� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�'������� �����\���� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������\���������"""])

#path=Base\������\�����\�������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\����������� ��� ��������������\���������"""])

#path=Base\������\�����\������������ ������������� ����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\������������ ������������� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\������������\������������\���������"""])

#path=Base\������\�����\����������\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\������\�����\����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\����\���������"""])

#path=Base\������\�����\�������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����\���������"""])

r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#18"""
#path=Base\������\�����\�����\� ��������������� ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�����\� ��������������� ����"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\������ �����\������� ������� ���������\���������"""])
#169
#path=Base\������\�����\�����\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�����\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������\���������"""])

#path=Base\������\�����\�����\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�����\��������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����\���������"""])

#path=Base\������\���������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�������\�����"""])

KB[r"""Base\������\���������\�����"""].__dict__["Not"].add(KB[r"""Base\������\���������\�����\����"""])

#path=Base\������\���������\�'��������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�'��������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�������\�����\���������"""])

KB[r"""Base\������\���������\�'��������� �������"""].__dict__["Not"].add(KB[r"""Base\������\���������\�'��������� �������\����"""])

#path=Base\������\���������\�'��������� �������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�'��������� �������\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

KB[r"""Base\������\���������\�'��������� �������\����"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\���������\�'��������� �������\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������"""])

#path=Base\������\������� �������� ��������� ��������\���� ����������� ������� � ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\���� ����������� ������� � ���������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\������"""])

#path=Base\������\������� �������� ��������� ��������\���� ���������� �������㳿\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\���� ���������� �������㳿"""].__dict__["isCause"].add(KB[r"""Base\������\�������� ����������\������"""])

KB[r"""Base\������\������� �������� ��������� ��������\���� ���������� �������㳿"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\���������\������"""])

#path=Base\������\������� �������� ��������� ��������\���������� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\���������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������\���������"""])

#path=Base\������\������� �������� ��������� ��������\���������� ���������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\���������� ���������������"""].__dict__["isCause"].add(KB[r"""Base\������\������������"""])

#path=Base\������\������� �������� ��������� ��������\������ �� ��������-�������� � ���������� ����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\������ �� ��������-�������� � ���������� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\������� �������� ��������� ��������\������ �� ���������� ����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\������ �� ���������� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������\������"""])

#path=Base\������\������� �������� ��������� ��������\������ �� ���������� ����������� �������\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\������\������� �������� ��������� ��������\������ �� ���������� ����������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\����\���������"""])

#path=Base\������\������� �������� ��������� ��������\������ �� ����������\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\������\������� �������� ��������� ��������\������ �� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\��������\������"""])

#path=Base\������\������� �������� ��������� ��������\������ ��� ��������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\������ ��� ��������������"""].__dict__["isCause"].add(KB[r"""Base\������\����������� ��� ��������������\���������"""])

#path=Base\������\������� �������� ��������� ��������\��������� ������������ ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\��������� ������������ ���������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\������"""])

#path=Base\������\������� �������� ��������� ��������\ϳ��� �������� � ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\ϳ��� �������� � ������������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

KB[r"""Base\������\������� �������� ��������� ��������\ϳ��� �������� � ������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������\������"""])

#path=Base\������\������� �������� ��������� ��������\������������ �����������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\������������ �����������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������\���������"""])

#path=Base\������\������� �������� ��������� ��������\����������� ����� ���������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������� �������� ��������� ��������\����������� ����� ���������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����\���������"""])

#path=Base\������\�������� ����������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������� ����������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������� ����������\�������"""].__dict__["Not"].add(KB[r"""Base\������\�������� ����������\������"""])

#path=Base\������\�������� ����������\�������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������� ����������\�������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\�������� ����������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������� ����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\�������� ����������\������\�� ������ �����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������� ����������\������\�� ������ �����������"""].__dict__["And"].add(KB[r"""Base\������\�������� ����������\������"""])

KB[r"""Base\������\�������� ����������\������\�� ������ �����������"""].__dict__["And"].add(KB[r"""Base\������\�����������\������ �����������\������"""])

KB[r"""Base\������\�������� ����������\������\�� ������ �����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\�������������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������������\������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\��������"""])

KB[r"""Base\������\�������������\������"""].__dict__["Not"].add(KB[r"""Base\������\�������������\�����"""])

KB[r"""Base\������\�������������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\����"""])

KB[r"""Base\������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� �������� ����\����"""])

KB[r"""Base\������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������\���������"""])

KB[r"""Base\������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\������� �������� ��������� ��������\��������� ���������� ����������� �����"""])

#path=Base\������\��������\³��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\³��������"""].__dict__["Not"].add(KB[r"""Base\������\��������"""])

#path=Base\������\������������ ��������\����� � �������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\����� � �������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])
#91
#path=Base\������\������������ ��������\������������ ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\������������ ��������"""].__dict__["isCause"].add(KB[r"""Base\������\������������"""])

#path=Base\������\������������ ��������\��������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\��������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

KB[r"""Base\������\������������ ��������\��������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])
#142
#path=Base\������\������������ ��������\����� �������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\����� �������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����\���������"""])

#path=Base\������\������������ ��������\����� �������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\����� �������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����\���������"""])

#path=Base\������\������������ ��������\г����\����������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])
#94
#path=Base\������\������������ ��������\г����\���\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\���"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

KB[r"""Base\������\������������ ��������\г����\���"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#142
#path=Base\������\������������ ��������\г����\������ ������� ������ ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\������ ������� ������ ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\г����\����\������ ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����\������ ����"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])
#97
#path=Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����\����������� ����\��������� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])
#97
#path=Base\������\������������ ��������\г����\������ �������� ��\˳��\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\������ �������� ��\˳��"""].__dict__["Not"].add(KB[r"""Base\������\������������ ��������\г����\������ �������� ��\�����"""])

#path=Base\������\������������ ��������\г����\������ ������� ����� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\������ ������� ����� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\г����\�������� �����\����� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\�������� �����\����� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\г����\������� ������� ����� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\������� ������� ����� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\г����\������� ������ ����� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\������� ������ ����� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\г����\�����\��� ������ ����� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\�����\��� ������ ����� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\г����\����� �������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����� �������\������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\������������ ��������\г����\����� �������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����� �������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����"""])
#95
#path=Base\������\������������ ��������\г����\����� �������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����� �������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\������������ ��������\г����\����� �������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����� �������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����"""])

#path=Base\������\������������ ��������\г����\����� �������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\����� �������\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����"""])
#95

KB[r"""Base\������\������������ ��������\г����\����� �������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����\���������"""])

#path=Base\������\������������ ��������\г����\�������� �������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\г����\�������� �������\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������"""])

#path=Base\������\������������ ��������\������������ ������� ������� �����\³��� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\������������ ������� ������� �����\³��� ����� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\������������ ������� ������� �����\г���� ����� �������� � �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\������������ ������� ������� �����\г���� ����� �������� � �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\������������ ��������\����� ������� �����\����������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\����� ������� �����\����������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\ϳ� �������� �����\������"""])
#132
#path=Base\������\������������ ��������\����� ������� �����\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\����� ������� �����\����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])
#218
#path=Base\������\������������ ��������\��������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ��������\��������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����\���������"""])

#path=Base\������\������������ ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ���������"""].__dict__["Not"].add(KB[r"""Base\������\������������ ���������\������"""])

KB[r"""Base\������\������������ ���������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\������������ ���������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

KB[r"""Base\������\������������ ���������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

#path=Base\������\������������ ���������\���������� ������������ �� ������ �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������"""])

KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����"""].__dict__["Not"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ ������\� ������� ����� �����"""])

#path=Base\������\������������ ���������\ϳ� �������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������ ���������\ϳ� �������� �����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\������������ ���������"""])

KB[r"""Base\������\������������ ���������\ϳ� �������� �����"""].__dict__["Not"].add(KB[r"""Base\������\������������ ���������\ϳ� �������� �����\������"""])

KB[r"""Base\������\������������ ���������\ϳ� �������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ ������\ϳ� �������� �����"""])

#path=Base\������\̳�����\�� ��������� ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �������\���������"""])

KB[r"""Base\������\̳�����\�� ��������� ������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\̳�����\�� �������� ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� �������� ������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\̳�����\�� ���������� ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� ���������� ������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\̳�����\�� ���������� ������������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� ���������� ������������\������"""].__dict__["Not"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

#path=Base\������\̳�����\�� ���������� ������������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� ���������� ������������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������"""])

KB[r"""Base\������\̳�����\�� ���������� ������������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����"""])

#path=Base\������\̳�����\�� ��������� ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\̳�����\�� ��������� ������������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������\������"""].__dict__["Not"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\̳�����\�� ��������� ������������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\�� ��������� ������������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ ������"""])

#path=Base\������\̳�����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\̳�����\������"""].__dict__["Not"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\����\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����\����"""].__dict__["Not"].add(KB[r"""Base\������\����\������"""])

#path=Base\������\���������� ������\����� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������� ������\����� ������"""].__dict__["Not"].add(KB[r"""Base\������\���������� ������\��� ������"""])

KB[r"""Base\������\���������� ������\����� ������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\�������\������ ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������ ������"""].__dict__["isCause"].add(KB[r"""Base\������\����\����"""])

#path=Base\������\�������\������ ������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������ ������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\�������\�����볺� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\�����볺� ������"""].__dict__["isCause"].add(KB[r"""Base\������\����\����"""])

KB[r"""Base\������\�������\�����볺� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������"""])

KB[r"""Base\������\�������\�����볺� ������"""].__dict__["isCause"].add(KB[r"""Base\������\���������\����� ������������\�����������"""])

KB[r"""Base\������\�������\�����볺� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\������ ������\�����"""])

KB[r"""Base\������\�������\�����볺� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\����������"""])
#146

KB[r"""Base\������\�������\�����볺� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������\������"""])

#path=Base\������\�������\������������ �����\prop.pykb
#open=0
#fg=red
#bg=white

# �� ������������� ��� ������������ ��������� �������
r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#12"""

KB[r"""Base\������\�������\������������ �����"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�������� �����"""])
KB[r"""Base\������\�������\������������ �����"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�������� �������"""])

#path=Base\������\�������\��������� ���� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�����������\������"""])

KB[r"""Base\������\�������\��������� ���� �����"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\������ �����\��������� �� ��������"""])

KB[r"""Base\������\�������\��������� ���� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������\���������"""])

KB[r"""Base\������\�������\��������� ���� �����"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������\��������� ���� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\������"""])

KB[r"""Base\������\�������\��������� ���� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������� �������������"""])

KB[r"""Base\������\�������\��������� ���� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �������\���������"""])

#path=Base\������\�������\��������� ���� �����\������� ������\1100-1400\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\������� ������\1100-1400"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������\��������� ���� �����\������� ������\1100-1400"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\400"""])

#path=Base\������\�������\��������� ���� �����\������� ������\1100-1600\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\������� ������\1100-1600"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� �������� ������������"""])

#path=Base\������\�������\��������� ���� �����\������� ������\1800-2100\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\������� ������\1800-2100"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������"""])

#path=Base\������\�������\��������� ���� �����\�� ������� ������� ������������ � ����������� ����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\�� ������� ������� ������������ � ����������� ����������"""].__dict__["And"].add(KB[r"""Base\������\����������\��������"""])

KB[r"""Base\������\�������\��������� ���� �����\�� ������� ������� ������������ � ����������� ����������"""].__dict__["And"].add(KB[r"""Base\������\���������\������ ������������\�������������\�������"""])

KB[r"""Base\������\�������\��������� ���� �����\�� ������� ������� ������������ � ����������� ����������"""].__dict__["And"].add(KB[r"""Base\������\�������\������� ������ ���� �� �������� �����"""])

KB[r"""Base\������\�������\��������� ���� �����\�� ������� ������� ������������ � ����������� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������� �������������"""])
#137
#path=Base\������\�������\��������� ���� �����\��������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\��������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\�������\��������� ���� �����\�������� ������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\�������� ������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\�������\��������� ���� �����\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\�������\��������� ���� �����\�����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\�����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������\��������� ���� �����\�����������"""].__dict__["isCause"].add(KB[r"""Base\������\���������\����� ������������\�����������\������� �����������\������"""])

#path=Base\������\�������\��������� ���� �����\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\�������\��������� ���� �����\���������� ������� ������� ����������� ����� � ���������� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\���������� ������� ������� ����������� ����� � ���������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\�������\��������� ���� �����\�����07�16�6\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\̳�������\-196"""])

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�����������\������"""])

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������������\������"""])

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�������\��������� ���� �����"""])

#path=Base\������\�������\��������� ���� �����\�����07�16�6\������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\�����07�16�6\������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������\������"""])
#143
#path=Base\������\�������\��������� ���� �����\�����1�15�4��3-�\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\�����1�15�4��3-�"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������\��������� ���� �����\�����1�15�4��3-�"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������������\������"""])

KB[r"""Base\������\�������\��������� ���� �����\�����1�15�4��3-�"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�������\��������� ���� �����"""])

#path=Base\������\�������\��������� ���� �����\�����1�15�4��3-�\������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ���� �����\�����1�15�4��3-�\������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������\������"""])

#path=Base\������\�������\������� � ����������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� � ����������� �����"""].__dict__["Not"].add(KB[r"""Base\������\�������\������� � ����������� �����\���������"""])

#path=Base\������\�������\������� � ����������� �����\�������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� � ����������� �����\�������������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\�������\������� � ����������� �����\�����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� � ����������� �����\�����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������\������� � ����������� �����\�����������"""].__dict__["Not"].add(KB[r"""Base\������\�������\������� � ����������� �����\�������������"""])

#path=Base\������\�������\������� ������ ���� �� �������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� ������ ���� �� �������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������� �������������"""])

#path=Base\������\�������\������������� ���\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������� ���"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

#path=Base\������\�������\������� ������\������ ������ �����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� ������\������ ������ �����������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������"""])

KB[r"""Base\������\�������\������� ������\������ ������ �����������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\������ �����\��������� �� ��������"""])
#167

KB[r"""Base\������\�������\������� ������\������ ������ �����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

#path=Base\������\�������\���������� ������� ����������\�����\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\���������� ������� ����������\�����\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������\���������"""])

#path=Base\������\�������\������������ ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������ ��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������\������"""])

#path=Base\������\�������\������������ ��������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������ ��������\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\�������\������������ ��������\����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�������\������������ ��������"""])

#path=Base\������\�������\������ ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������ ����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������\���������"""])

#path=Base\������\�������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����"""])

#path=Base\������\�������\������� ����������� ���\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� ����������� ���"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

#path=Base\������\�������\�������� � ������������� ���������� � ����� �����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\�������� � ������������� ���������� � ����� �����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

KB[r"""Base\������\�������\�������� � ������������� ���������� � ����� �����������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�����������\������"""])

#path=Base\������\�������\ͳ���\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\ͳ���"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������������\������"""])

#path=Base\������\�������\������������ ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������ ����"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�����������\������"""])

KB[r"""Base\������\�������\������������ ����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �������\���������"""])

#path=Base\������\�������\��������� ��������� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ��������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������"""])
#137

KB[r"""Base\������\�������\��������� ��������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

#path=Base\������\�������\�������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\�������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������"""])

#path=Base\������\�������\�������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\�������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������"""])

#path=Base\������\�������\�����������\������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\�����������\������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\�������\�����������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\�����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������"""])
#139

KB[r"""Base\������\�������\�����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

KB[r"""Base\������\�������\�����������\������"""].__dict__["Not"].add(KB[r"""Base\������\�������\�����������\������"""])

#path=Base\������\�������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\������������ ��������"""])

KB[r"""Base\������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\����������� ���\�������"""])

KB[r"""Base\������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\���������������\����������"""])
#147

KB[r"""Base\������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\������������"""])

#path=Base\������\�������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������"""])

KB[r"""Base\������\�������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������"""])

#path=Base\������\�������\������������ ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������ ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������\������"""])

#path=Base\������\�������\������������ ��������\������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������ ��������\������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

#path=Base\������\�������\������������ ��������\��������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������ ��������\��������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])
#95
#path=Base\������\�������\������������ ��������\г�� ������� ���������� ����� � �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������ ��������\г�� ������� ���������� ����� � �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])
#137
#path=Base\������\�������\������� ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� ����"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�����������\������"""])

#path=Base\������\�������\������� ����\���������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� ����\���������������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\�������\��������� ��������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� ��������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\�������\������������\� ������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������\� ������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\������� � ����������� �����\���������"""])

#path=Base\������\�������\������������\³�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������\³�����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�������\������������"""])

#path=Base\������\�������\������������\³�����\��������� ����������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������\³�����\��������� ����������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\������ �����\����������� �� ��������"""])

#path=Base\������\�������\������������\³�����\���������� ���� ����������\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\������\�������\������������\³�����\���������� ���� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������"""])

#136
#path=Base\������\�������\������������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������\����������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�������\������������"""])

#path=Base\������\�������\������������\����������\������� ��� ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������\����������\������� ��� ���������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������"""])

#136
#path=Base\������\�������\������������\ճ���-������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������\ճ���-������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�������\������������\ճ���-������� �������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�������\������������"""])

#path=Base\������\�������\������������\ճ���-������� �������\����������\������� ������ ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������������\ճ���-������� �������\����������\������� ������ ������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����"""])
#255
#path=Base\������\�������\���������� ������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\���������� ������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������"""])

KB[r"""Base\������\�������\���������� ������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������"""])

#path=Base\������\�������\������� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�����������\������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\����\����"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\350-550"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\������ �����\����������� �� ��������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������\������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������� ����������\�������\���������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\������������ ��������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

#146

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� �������� ����\������"""])

KB[r"""Base\������\�������\������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����\���������"""])



#path=Base\������\�������\��������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

KB[r"""Base\������\�������\��������������"""].__dict__["Not"].add(KB[r"""Base\������\�������\��������������\������"""])

#path=Base\������\�������\��������� �� ������������ ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������\��������� �� ������������ ���������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������"""])

KB[r"""Base\������\�������\��������� �� ������������ ���������"""].__dict__["Not"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������\������"""])

#path=Base\������\������������\³������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\³������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������"""])

#path=Base\������\������������\��������\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\������\������������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�����"""])

KB[r"""Base\������\������������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ ������"""])

KB[r"""Base\������\������������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\������������\������"""])

#path=Base\������\������������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\����"""])

KB[r"""Base\������\������������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �������"""])

#path=Base\������\������������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\��������"""])

#path=Base\������\������������\������\�������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\������\�������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������\���������"""])

KB[r"""Base\������\������������\������\�������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])

KB[r"""Base\������\������������\������\�������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\������������\������"""])

#path=Base\������\������������\������\��������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\������\��������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������"""])

KB[r"""Base\������\������������\������\��������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\������������\������"""])

#path=Base\������\������������\������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\�������"""])

KB[r"""Base\������\������������\������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])

KB[r"""Base\������\������������\������\�������"""].__dict__["Not"].add(KB[r"""Base\������\������������\������\������"""])

KB[r"""Base\������\������������\������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\����� �������"""])

#path=Base\������\������������\������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\������������"""].__dict__["isCause"].add(KB[r"""Base\������\������������\������\�������"""])

KB[r"""Base\������\������������\������������"""].__dict__["Not"].add(KB[r"""Base\������\������������\������������\���������"""])

#path=Base\������\������������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\����"""].__dict__["isCause"].add(KB[r"""Base\������\����������\��������"""])

#path=Base\������\������������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\³� ���������������� ������������"""])

#path=Base\������\������������\�������\prop.pykb
#open=1
#fg=red
#bg=white
KB[r"""Base\������\������������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ ������"""])

#path=Base\������\������������\��������\��������������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\������������\��������\��������������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])
#174
#path=Base\������\����������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ ������"""])

#path=Base\������\����������\�����\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������\�����\���������"""].__dict__["Not"].add(KB[r"""Base\������\����������\�����"""])

#path=Base\������\����������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �������"""])

KB[r"""Base\������\����������\����"""].__dict__["Not"].add(KB[r"""Base\������\����������\����\���������"""])

#path=Base\������\����������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������\��������"""].__dict__["Not"].add(KB[r"""Base\������\����������\��������\���������"""])

#path=Base\������\����������\�������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������\�������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

KB[r"""Base\������\����������\�������\�����"""].__dict__["Not"].add(KB[r"""Base\������\����������\�������\�����\���������"""])

#path=Base\������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������\���������"""])

#path=Base\������\��������\������������ ���-�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\������������ ���-�����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\600"""])

r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#13"""
#path=Base\������\��������\������������ ���-�����, ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\������������ ���-�����, ����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\600"""])

#path=Base\������\��������\������������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\������������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� ��������� ������"""])
#137
#path=Base\������\��������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\������� �������� ��������� ��������\������ �� ���������� ����������� �������"""])

#path=Base\������\��������\���쳺�� � �������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\���쳺�� � �������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\200"""])

KB[r"""Base\������\��������\���쳺�� � �������������"""].__dict__["isCause"].add(KB[r"""Base\������\��������\������������� �������"""])
#137

KB[r"""Base\������\��������\���쳺�� � �������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\����"""])

#path=Base\������\��������\������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������\������"""])

#path=Base\������\��������\̳���\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\̳���"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\600"""])

KB[r"""Base\������\��������\̳���"""].__dict__["isCause"].add(KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""])

#path=Base\������\��������\ͳ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\ͳ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\900"""])

KB[r"""Base\������\��������\ͳ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""])

#path=Base\������\��������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\200"""])

KB[r"""Base\������\��������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�������� ����������\������"""])

KB[r"""Base\������\��������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""])

#path=Base\������\��������\������� ����������� � �������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\������� ����������� � �������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\200"""])

#path=Base\������\��������\������� � ������ �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\������� � ������ �������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\200"""])

#path=Base\������\��������\����'���\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\����'���"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\150"""])

KB[r"""Base\������\��������\����'���"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\����"""])

#path=Base\������\��������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])
#255
#path=Base\������\��������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\��������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\����"""])
#345

#path=Base\������\��������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\600"""])

KB[r"""Base\������\��������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\����"""])

#path=Base\������\��������\��������� �� ��� ��������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\��������� �� ��� ��������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� ��������� ������"""])
#137
#path=Base\������\��������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\200"""])

KB[r"""Base\������\��������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\��������\��������� �� ��� ��������� ��������"""])
#137
#path=Base\������\��������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\200"""])

KB[r"""Base\������\��������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\��������\������������� �������"""])
#137

KB[r"""Base\������\��������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""])

#path=Base\������\��������\������� � �������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������\������� � �������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ �����������\�����������\300"""])

#path=Base\������\�����������\³� ���������������� ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\³� ���������������� ������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\������ ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������ ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������"""])

KB[r"""Base\������\�����������\������ ������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\������ ������\� ���������� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������ ������\� ���������� ����� �����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\������ ������"""])

#path=Base\������\�����������\������ ������\� ������� ����� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������ ������\� ������� ����� �����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\������ ������"""])

#path=Base\������\�����������\������ ������\ϳ� �������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������ ������\ϳ� �������� �����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\������ ������"""])

#path=Base\������\�����������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\��������"""])

KB[r"""Base\������\�����������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\����"""])

KB[r"""Base\������\�����������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\������"""])

KB[r"""Base\������\�����������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� �������� ����\������"""])

KB[r"""Base\������\�����������\�������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\�������\���������"""])

KB[r"""Base\������\�����������\�������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\��������� ����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\��������� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\�����������\��������� ����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������"""])

KB[r"""Base\������\�����������\��������� ����������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\��������� ����������\���������� ��� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����"""].__dict__["Not"].add(KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����\���������"""])

KB[r"""Base\������\�����������\��������� ����������\���������� ��� �����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\��������� ����������"""])

#path=Base\������\�����������\��������� ����������\��� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\��������� ����������\��� �����"""].__dict__["Not"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����\���������"""])

KB[r"""Base\������\�����������\��������� ����������\��� �����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\��������� ����������"""])

#path=Base\������\�����������\��������� ����������\��� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\��������� ����������\��� �������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\��������� ����������\��� �������\���������"""])

KB[r"""Base\������\�����������\��������� ����������\��� �������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\��������� ����������"""])

#path=Base\������\�����������\��������� ����������\����� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\��������� ����������\����� �������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\��������� ����������"""])

#path=Base\������\�����������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����"""].__dict__["isCause"].add(KB[r"""Base\������\������������\������"""])

KB[r"""Base\������\�����������\����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])

KB[r"""Base\������\�����������\����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\����\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\����������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\����\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\���������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\����\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\�������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\����\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\��������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\����\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\���������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\����\�������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\�������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\����\�������-���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\�������-���������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\����\�����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����\�����������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\�����������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\����"""])

KB[r"""Base\������\�����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������"""])

KB[r"""Base\������\�����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\�����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\������������\������"""])

KB[r"""Base\������\�����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\������"""])

KB[r"""Base\������\�����������\��������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\��������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\��������\������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\��������"""])

#path=Base\������\�����������\�������� �������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\�������� �������������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

KB[r"""Base\������\�����������\�������� �������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����"""])

KB[r"""Base\������\�����������\�������� �������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\������� ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������� ����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\������� ����\���������� ������ ����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������\������� ����"""])

#path=Base\������\�����������\������� ����\���������� ������ ����������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������� ����\���������� ������ ����������\������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

#path=Base\������\�����������\���������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\���������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\���������������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\���������������\����������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\���������������"""])

#path=Base\������\�����������\�����������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\�����������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������\��� �����"""])

KB[r"""Base\������\�����������\�����������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\�����������"""])

#path=Base\������\�����������\�����������������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\�����������������\���������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\�����������������"""])

#path=Base\������\����������� ��� ��������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������� ��� ��������������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������"""])

KB[r"""Base\������\����������� ��� ��������������"""].__dict__["Not"].add(KB[r"""Base\������\����������� ��� ��������������\���������"""])

#path=Base\������\��������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\��������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\��������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������\������"""])

#path=Base\������\�������� �'�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�������� �'�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������"""])

KB[r"""Base\������\�������� �'�������"""].__dict__["Not"].add(KB[r"""Base\������\�������� �'�������\������"""])

#path=Base\������\����������\���������� ������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������\���������� ������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������\������"""])

#path=Base\������\����������\��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������"""])

KB[r"""Base\������\����������\��������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������� �������������"""])

KB[r"""Base\������\����������\��������"""].__dict__["Not"].add(KB[r"""Base\������\����������\��������\������"""])

#path=Base\������\���������\������������ � �������� ����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\������������ � �������� ����"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\�������\� �������"""])

#path=Base\������\���������\���������� �������� ������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\���������� �������� ������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\���������\�������� �����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�������� �����������"""].__dict__["isCause"].add(KB[r"""Base\������\���������\������ ������������\�����������"""])

#path=Base\������\���������\�������� �����������\�������� �� ����������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�������� �����������\�������� �� ����������� �����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\���������\�������� �����������"""])

#path=Base\������\���������\�������� �����������\�������� �� ����� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�������� �����������\�������� �� ����� ��������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\���������\�������� �����������"""])

#path=Base\������\���������\�������� �����������\�������� �� �������� ������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�������� �����������\�������� �� �������� ������������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\���������\�������� �����������"""])

#path=Base\������\���������\������ ������������\�������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\������ ������������\�������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������ ������"""])

#path=Base\������\���������\������ ������������\�������������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\������ ������������\�������������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\���������\������ ������������\�������������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\������������"""])

KB[r"""Base\������\���������\������ ������������\�������������\�������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\��������� ����������"""])

KB[r"""Base\������\���������\������ ������������\�������������\�������"""].__dict__["Not"].add(KB[r"""Base\������\���������\������ ������������\�������������\�����"""])

#path=Base\������\���������\������ ������������\�������������\�����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\������ ������������\�������������\�����"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������"""])

#path=Base\������\���������\������ ������������\�����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\������ ������������\�����������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\���������\������ ������������\�����������"""].__dict__["Not"].add(KB[r"""Base\������\���������\������ ������������\�������������"""])

#path=Base\������\���������\�������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�������������\�����"""])

KB[r"""Base\������\���������\�������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\�����\�� ����\����"""])

#path=Base\������\���������\�������� ��������� ������������ ������ �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�������� ��������� ������������ ������ �����"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������\���������� ������������ �� ������ �����\������"""])

#path=Base\������\���������\���������� ���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\���������� ���������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\�������\� �������\��������� ������������ ������"""])

#path=Base\������\���������\����� ��� �����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����� ��� �����������"""].__dict__["isCause"].add(KB[r"""Base\������\���������\������ ������������\�������������\�������"""])

#path=Base\������\���������\��������� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\��������� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\������ �����\������� ����\�����"""])

#path=Base\������\���������\Գ������ ����� ��� �����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\Գ������ ����� ��� �����������"""].__dict__["isCause"].add(KB[r"""Base\������\����������\��������\���������"""])
r"""Base\�������\�.�.������, �.�.���������. ��������� � ��������� ����������\�.�.������, �.�.���������. ��������� � ��������� ����������.djvu#21"""
#path=Base\������\���������\����� ������������ ��������������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����� ������������ ��������������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\����"""])

#path=Base\������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�����������������\���������"""])

#path=Base\������\���������\�������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\�������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\���������"""])

#path=Base\������\���������\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����"""].__dict__["SubClassOf"].add(KB[r"""Base\������\���������"""])

#path=Base\������\���������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\���������"""].__dict__["SubClassOf"].add(KB[r"""Base\������\���������"""])

#path=Base\������\�����������\������ �����������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\����������"""])

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\������������\������������"""])

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������� �� ������������ ���������"""])

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["Not"].add(KB[r"""Base\������\�����������\������ �����������\������"""])

#path=Base\������\�����������\������ �����������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\��������������"""])

KB[r"""Base\������\�����������\������ �����������\������"""].__dict__["isCause"].add(KB[r"""Base\������\�������\�����������\������"""])
#171
#path=Base\������\�����������\����������� �� ���������� ����������� ������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����������\����������� �� ���������� ����������� ������\������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])

#path=Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""].__dict__["Not"].add(KB[r"""Base\������\�����\���� ����������� ����� �� ��� ��������� �������������\����������"""])

#path=Base\������\�����\�� ����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�� ����\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\�����\�� ����\������"""].__dict__["isCause"].add(KB[r"""Base\������\�������������\������"""])

KB[r"""Base\������\�����\�� ����\������"""].__dict__["Not"].add(KB[r"""Base\������\�����\�� ����\����"""])

#path=Base\������\�����\�� ����\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�� ����\����"""].__dict__["isCause"].add(KB[r"""Base\������\�������������\�����"""])

#path=Base\������\�����\�� �������� ����\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�� �������� ����\������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\�������"""])

KB[r"""Base\������\�����\�� �������� ����\������"""].__dict__["isCause"].add(KB[r"""Base\������\�������������\������"""])

KB[r"""Base\������\�����\�� �������� ����\������"""].__dict__["Not"].add(KB[r"""Base\������\�����\�� �������� ����\����"""])

#path=Base\������\�����\�� �������� ����\����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\�����\�� �������� ����\����"""].__dict__["isCause"].add(KB[r"""Base\������\�������������\�����"""])

#path=Base\������\���������\����� ������������\�����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����� ������������\�����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������\������"""])

KB[r"""Base\������\���������\����� ������������\�����������"""].__dict__["isCause"].add(KB[r"""Base\������\�������� ����������\������"""])

#path=Base\������\���������\����� ������������\�����������\������� �����������\������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����� ������������\�����������\������� �����������\������"""].__dict__["Not"].add(KB[r"""Base\������\���������\����� ������������\�����������\������� �����������"""])

#path=Base\������\���������\����� ������������\����������� ���� ��������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����� ������������\����������� ���� ��������"""].__dict__["isCause"].add(KB[r"""Base\������\�������� ����������\������"""])
#237
#path=Base\������\���������\����� ������������\ϳ������������ �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����� ������������\ϳ������������ �������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������\������"""])

#path=Base\������\���������\����� ������������\����������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\����� ������������\����������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������\������"""])

#path=Base\������\���������\��������� ��������� ������ ����������� �����\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\��������� ��������� ������ ����������� �����"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ��������� ������������\������"""])
#238
#path=Base\������\���������\������ �������\���������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\������ �������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\�������� ����������\������"""])

KB[r"""Base\������\���������\������ �������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\���������� ���������\������ ������\�����"""])

KB[r"""Base\������\���������\������ �������\���������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����"""])

#path=Base\������\���������\���������� �������\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\������\���������\���������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\̳�����\�� ���������� ������������\������"""])

KB[r"""Base\������\���������\���������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\�����������\������� ����\���������� ������ ����������"""])

KB[r"""Base\������\���������\���������� �������"""].__dict__["isCause"].add(KB[r"""Base\������\������������ ���������"""])


#path=Reasoner\class.pykb
#open=1
#fg=darkgreen
#bg=white

# ������� ��������� 

def allFactsSet(showTransitive=True):
    '''������� ������� ��� ����� (�����) ���� �����.
    ����� � ������ ������� (���'���, ��������, ��'���)'''
    factsSet=set() # ������� �����
    for k in KB.values(): # ��� ��� ��������
        if k.__class__.__name__==r"""Base\������""": # ���� �� ������
            for p in k.__dict__: # ��� ��� ��������
                if k.__dict__[p].__class__.__name__=='Property': # ���� ������� ����������
                    for obj in k.__dict__[p].get(showTransitive): # ��� ��� ������� ����������
                        factsSet.add((k,p,obj)) # �������� ���� � ������� �����
    return factsSet


for k,v in KB.iteritems():
    v.name=k # ��� ��� ��'���� � KB ���� ������� name � �������� ���� �������� ����� � KB
    v.codes={} # ���������� codes - ������� �������� ����
    if v.__class__.__name__=='type': # ���� �� ����
        v.__name__=k # ��� ��� ����� � KB �������� __name__ �������� ����� � KB


assertedFacts=allFactsSet(False) # ������ �����
print len(assertedFacts)
import csv
writer = csv.writer(open("assertedFacts.csv", "wb"),delimiter = ';') # ������� csv ����
for x in assertedFacts:
    writer.writerow([x[0].name,x[1],x[2].name]) # �������� � ���� csv


while True: # ���� ��� ������������ ������
    beforeFacts=allFactsSet() # ������� ����� ��
    print str(len(beforeFacts))+' facts. Iteration for apply rules...'

    # ������ ��������� ��� ��������� � ����������� ������������
    for k in KB.values(): # ��� ��� ��������
        for p,pv in k.__dict__.iteritems(): # ��� ��� ��������
            if pv.__class__.__name__=='Property': # ���� ������� ����������
                for obj in pv.get(True): # ��� ��� ������� ����������
                    
                    if pv.inverseName!='': # ���� � �������� ����������
                        # �������� ���� � �������� ���������� ��'����
                        obj.__dict__[pv.inverseName].add(pv.subj)
                            
                    if pv.symmetric: # ���� ���������� ����������
                        # �������� ���� � ��������� ���������� ��'����
                        obj.__dict__[pv.name].add(pv.subj)

                        
    # ������� ���������:
    # SubClassOf(?x, ?y) & isCause(?y, ?p) -> isCause(?x, ?p)
    # SubClassOf(?x, ?y) & isEffect(?y, ?p) -> isEffect(?x, ?p)
    for k in KB.values(): # ��� ��� ��������
        if k.__class__.__name__==r"""Base\������""": # ���� �� ������
            for bk in k.SubClassOf.get(True): # ��� ��� ������� �������� (�����)
                for x in bk.isCause.get(True):
                    k.isCause.add(x)
                for x in bk.isEffect.get(True):
                    k.isEffect.add(x)
                    
    # ������� ���������:
    # Not(?x, ?nx) & isCause(?nx, ?ny) & Not(?y, ?ny) -> isCause(?x, ?y) 
    # Not(?x, ?nx) & isEffect(?nx, ?ny) & Not(?y, ?ny) -> isEffect(?x, ?y) 
    for k in KB.values(): # ��� ��� ��������
        if k.__class__.__name__==r"""Base\������""": # ���� �� ������
            for nk in k.Not.get(): # ��� ��� ���������� ��������
                for e in nk.isCause.get(True): # ��� ��� ������� �����������
                    for ne in e.Not.get(): # ��� ��� ���������� ������� �����������
                        k.isCause.add(ne) # ������� � �� ��������
                for e in nk.isEffect.get(True): # ��� ��� ������ �����������
                    for ne in e.Not.get(): # ��� ��� ���������� ������ �����������
                        k.isEffect.add(ne) # ������� � �� ��������    

    afterFacts=allFactsSet() # ������� ����� ����
    # ��������� ����, ���� ������� ����� �� � ���� ������������ ������ ����
    if beforeFacts==afterFacts: break


allFacts=allFactsSet()  # �� �����               
print len(allFacts) 
import csv
writer = csv.writer(open("allFacts.csv", "wb"),delimiter = ';') # ������� csv ����
for x in allFacts:
    writer.writerow([x[0].name,x[1],x[2].name]) # �������� � ���� csv


# ��� ��� ������� KB �������� ���������� codes ����� ��������� ����  
for k in KB: # ��� ��� ������ � KB
    if k.startswith("Base\\"):
        for fl in os.listdir(k): # ��� ��� ����� � �������
            path = os.path.join(k, fl) # ������ ����
            if os.path.splitext(path)[1]=='.pykb': # ���� ���� '.pykb'
                f=open(path,'r') # �������
                s=f.read() # ������
                KB[k].codes[fl]=s # �������� ����� ��������� ����
                f.close() # �������


#path=Query\class.pykb
#open=1
#fg=brown
#bg=white

# ���� ������ �� ���� �����
# ������ ������������ � ������ ��� ���� ������ #fg=brown

#path=Query\GenerateHTML.pykb
#open=0
#fg=brown
#bg=white

import sys
sys.path.append(programDir)
import MakeCode

for k in KB: # ��� ��� ������ � KB
    if k.startswith(r"""Base\������"""):
        for pykbFile in KB[k].codes: # ��� ������� pykb ����� � ������� k
            MakeCode.genHTML(k+'\\'+pykbFile) # ���������� HTML ���   

