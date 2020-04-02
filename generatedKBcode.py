#path=class.pykb
# -*- coding: CP1251 -*-
import os
import copy

class Property(object):
    '''Клас, який описує властивість об'єкта'''
    
    def __init__(self,subj,name,inverseName='',functional=False,symmetric=False,transitive=False):
        '''Конструктор'''
        self.subj=subj # суб'єкт властивості
        self.name=name # назва властивості
        self.inverseName=inverseName # назва інверсної властивості
        self.functional=functional # властивість функціональна
        self.symmetric=symmetric # властивість симетрична
        self.transitive=transitive # властивість транзитивна
        self.set=set() # множина значень властивості
        self.subj.__setattr__(self.name,self) # установити атрибут властивості для суб'єкта
        
    def add(self,*args):
        '''Добавляє об'єкт або кортеж об'єктів в множину'''
        for obj in args: # для всіх об'єктів в args
            if self.functional: # якщо властивість функціональна
                self.set.clear() # очистити множину
                
# реалізовано в машині виведення
#            if self.inverseName!='': # якщо є інверсна властивість
#                # добавити його в інверсну властивість об'єкта
#                obj.__dict__[self.inverseName].set.add(self.subj)
#                    
#            if self.symmetric: # якщо властивість симетрична
#                # добавити його в аналогічну властивість об'єкта
#                obj.__dict__[self.name].set.add(self.subj)
            
            self.set.add(obj) # добавити об'єкт в множину
        
    def get(self, showTransitive=False):
            '''Повертає множину значень властивості
            (showTransitive=True - транзитивної властивості)'''
            def getTransitive(subj,s=set()):
                '''Повертає множину значень транзитивної властивості. Рекурсивна'''
                if hasattr(subj, self.name): # якщо subj має атрибут self.name 
                    # для усіх об'єктів в властивості з назвою self.name
                    for obj in subj.__dict__[self.name].set:
                        if obj not in s: # якщо obj немає в множині s
                            s.add(obj) # добавити об'єкт в множину
                            s=getTransitive(obj,s) # рекурсія
                return s # повертає множину
            # якщо властивість транзитивна і показувати транзитивні
            if self.transitive and showTransitive:
                # множина значень транзитивної властивості
                s=getTransitive(self.subj)
                s.discard(self.subj) # вилучити self.subj з множини, якщо є
                return s
            # інакше повернути множину значень властивості
            else: return self.set
KB={} # словник бази знань
programDir="D:\!My_doc\Python_projects\TreePyKB"
#path=Base\class.pykb
#open=1
#fg=purple
#bg=white

class X(object):
    '''Базовий клас онтології'''
    def __init__(self): # конструктор
        # ці властивості дозволяють створювати нові об'єкти за допомогою логічних операцій
        Property(subj=self,name='And') # властивість 'And'
        Property(subj=self,name='Or') # властивість 'Or'
        Property(subj=self,name='Not',symmetric=True) # властивість 'Not'
        Property(subj=self,name='SubClassOf',transitive=True) # властивість 'SubClassOf'
        self.doc="" # довідка
KB[r"""Base"""]=X; del X
#path=Base\Джерело\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    '''Клас, який описує посилання на джерело'''
    def __init__(self): # конструктор
        KB[r"""Base"""].__init__(self)
        # властивість 'є посиланням'
        Property(subj=self,name='isReference',inverseName='hasReference')
KB[r"""Base\Джерело"""]=X; del X
#path=Base\Залежність\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    '''Клас, який описує залежність'''
    def __init__(self, xy=None, relative=None, xName='x', yName='y'):
        KB[r"""Base"""].__init__(self)
        # властивість 'є залежністю'
        Property(subj=self,name='isDependence',inverseName='hasDependence')
        self.xy=xy # дані у вигляді [(x1,y1),(x2,y2),(x3,y3)]
        self.relative=relative # відносна залежність (збільшує, зменшує, є екстремум)
        self.xName=xName; self.yName=yName # назви осей
    def plot(self):
        '''Рисує графік залежності'''
        from matplotlib import rcParams, pyplot # бібліотека matplotlib
        rcParams['text.usetex']=False
        rcParams['font.sans-serif'] = ['Arial']
        rcParams['font.serif'] = ['Arial'] # шрифт для вводу кирилиці
        x,y=[p[0] for p in self.xy],[p[1] for p in self.xy] # розділити дані
        pyplot.plot(x,y,'b-') #крива
        pyplot.title(unicode('')) # заголовок
        pyplot.xlabel(unicode(self.xName)) # надпис осі x
        pyplot.ylabel(unicode(self.yName)) # надпис осі y
        pyplot.grid(True) # сітка
        pyplot.show() # показати рисунок
    def interp(self,x,reverse=False):
        '''Знаходить значення Y лінійною інтерполяцією
        якщо reverse=True, то знаходить значення X'''
        # якщо reverse=True, поміняти X і Y місцями
        if reverse: data=[(p[1],p[0]) for p in self.xy]
        else: data=self.xy
        lines=[] # список ліній залежності
        p1=data[0] # перша точка
        for p2 in data[1:]: # для усіх точок крім першої
            lines.append((p1,p2)) # створити лінію з пар сусідніх точок
            p1=p2
        results=[] # список результатів    
        for line in lines: # для всіх ліній залежності
            # координати точок лінії
            x1,y1,x2,y2=line[0][0],line[0][1],line[1][0],line[1][1]
            if x>=x1 and x<=x2 or x<=x1 and x>=x2: # якщо x в межах [x1,x2]
                results.append((x-x1)*(y2-y1)/(x2-x1)+y1) # знайти точку перетину x з лінією
        return results
KB[r"""Base\Залежність"""]=X; del X
#path=Base\Модель\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    def __init__(self):
        KB[r"""Base"""].__init__(self)
        # властивість 'параметр'
        Property(subj=self,name='parameter')

KB[r"""Base\Модель"""]=X; del X

#path=Base\Модель\ГОСТ 13877-96\class.pykb
#open=1
#fg=purple
#bg=white

class X(KB[r"""Base\Модель"""]):
    def __init__(self):
        KB[r"""Base\Модель"""].__init__(self)
    def create(self):
        "цю функцію необхідно викликати після створення об'єктів KB"
        
        self.d={ # словник геометричних параметрів
        'd_n':"зовнішній діаметр різьби ніпеля",
        'd2_n':"середній діаметр різьби ніпеля",
        'd1_n':"внутрішній діаметр різьби ніпеля",
        'r_n':"радіус западин різьби ніпеля",
        'dn':"діаметр бурта ніпеля",
        'd1n':"діаметр зарізьбової канавки ніпеля",
        'l1n':"довжина ніпеля",
        'l2n':"довжина зарізьбової канавки ніпеля",
        'l3n':"довжина ніпеля без фаски на різьбі",
        'l4n':"довжина ніпеля з буртом",
        'r3n':"радіус скруглень зарізьбової канавки ніпеля",
        'd_m':"зовнішній діаметр різьби муфти",
        'd2_m':"середній діаметр різьби муфти",
        'd1_m':"внутрішній діаметр різьби муфти",
        'dm':"зовнішній діаметр муфти",
        'd1m':"внутрішній діаметр опорної поверхні муфти",
        'lm':"довжина муфти",
        'd0':"діаметр тіла штанги",
        'p_n':"крок різьби ніпеля",
        'p_m':"крок різьби муфти"
        }
        
        self.p={ # словник інших параметрів
        'delta_ln':"величина збільшення довжини ніпеля",
        'material1':"назва матеріалу з бібліотеки матеріалів",
        'material2':"назва матеріалу з бібліотеки матеріалів",
        'bolt_load':"осьова деформація муфти під час згвинчування (мм)",
        'sigma1':"напруження в тілі штанги для кроку 1 (Па)",
        'sigma2':"напруження в тілі штанги для кроку 2 (Па)"
        }

    def createAbaqusModel(self):
        """Cтворює модель Abaqus.
        Створює тимчасовий файл з даними для передачі їх скрипту Abaqus.
        Виконує скрипт в Abaqus"""
        import os,pickle,tempfile,subprocess
        path=os.path.join(os.getcwd(), self.name) # шлях до каталогу
        data={'d':self.d,'p':self.p,'path':path}
        name=os.path.join(tempfile.gettempdir(),"data4AbaqusScript.tmp")
        f=open(name, "wb") #відкрити бінариний файл для запису
        pickle.dump(data,f) #законсервувати дані у файлі
        f.close() #закрити файл

        print "Abaqus CAE started. Please wait"
        # виконує скрипт в Abaqus та чекає завершення
        subprocess.Popen(r'C:\SIMULIA\Abaqus\6.11-3\exec\abq6113.exe cae noGUI=gost13877_96AbaqusMain.py').communicate()
        #os.system(r'start /WAIT abaqus cae noGUI=gost13877_96Abaqus.py')
        print "Abaqus CAE finished"

    def createSWModel(self):
        "створює модель SolidWorks"
        pass
    def runAbaqusModel(self):
        "розраховує модель Abaqus"
        pass
    def getAbaqusModelResults(self):
        "повертає результати з моделі Abaqus"
        pass
KB[r"""Base\Модель\ГОСТ 13877-96"""]=X; del X

#path=Base\Модель\ГОСТ 13877-96\ШН 19\class.pykb
#open=1
#fg=purple
#bg=white

class X(KB[r"""Base\Модель\ГОСТ 13877-96"""]):
    def __init__(self):
        KB[r"""Base\Модель\ГОСТ 13877-96"""].__init__(self)
    def create(self):
        "цю функцію необхідно викликати після створення об'єктів KB"
        KB[r"""Base\Модель\ГОСТ 13877-96"""].create(self)
        
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
       
KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19"""]=X; del X

#path=Base\Модель\ГОСТ 13877-96\ШН 22\class.pykb
#open=1
#fg=purple
#bg=white

#path=Base\Параметр\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    "Клас описує поняття розміру"
    def __init__(self):
        KB[r"""Base"""].__init__(self)
    def create(self,doc,n,ei,es,v):
        "створює об'єкт"
        self.doc=doc #довідка
        self.n=n #номінальний розмір
        self.ei=ei #нижнє відхилення
        self.es=es #верхнє відхилення
        self.v=v #дійсне значення
    def min(self):
        "повертає мінімальний розмір"
        return self.n+self.ei
    def max(self):
        "повертає максимальний розмір"
        return self.n+self.es

KB[r"""Base\Параметр"""]=X; del X

#path=Base\Факт\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]):
    '''Клас, який описує факт (триплет) у вигляді
    суб'єкт-предикат-об'єкт'''
    def __init__(self): # конструктор
        KB[r"""Base"""].__init__(self)
        # властивість 'має посилання'
        Property(subj=self,name='hasReference',inverseName='isReference')
        # властивість 'має залежність'
        Property(subj=self,name='hasDependence',inverseName='isDependence')
    def create(self,subjName,propName,objName):
        self.subjName=subjName # назва суб'єкта
        self.propName=propName # назва предиката (властивість)
        self.objName=objName # назва об'єкта
        # добавити значення в властивість, якщо немає
        KB[self.subjName].__dict__[self.propName].add(KB[self.objName])

KB[r"""Base\Факт"""]=X; del X
#path=Base\Фактор\class.pykb
#open=0
#fg=purple
#bg=white

class X(KB[r"""Base"""]): # успадковує клас Base 
    '''Клас, який описує фактор'''
    def __init__(self): # конструктор
        KB[r"""Base"""].__init__(self)
        # транзитивна властивість 'є причиною'
        Property(subj=self,name='isCause',inverseName='isEffect',transitive=True)
        # транзитивна властивість 'є наслідком' 
        Property(subj=self,name='isEffect',inverseName='isCause',transitive=True)
KB[r"""Base\Фактор"""]=X; del X

#path=Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения"""]=KB[r"""Base\Джерело"""]()

#path=Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\class.pykb
#open=1
#fg=blue
#bg=white

#path=Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1"""]=KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19"""]()

#path=Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\delta_ln\class.pykb
#open=1
#fg=blue
#bg=white

#path=Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\delta_ln\10\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\delta_ln\10"""]=KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19"""]()

#path=Base\Фактор\Геометричні параметри\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск розміру\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск розміру\Великий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск розміру\Малий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру\Малий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Допуск форми"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Нечутливість до перекосу\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Нечутливість до перекосу"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Великий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Високоміцних сталей\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Високоміцних сталей"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Зменшення\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей\Малий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей\Малий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Посадка\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Посадка"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Посадка\З зазором\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Посадка\З зазором\Зменшення діаметральних зазорів\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором\Зменшення діаметральних зазорів"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Посадка\З натягом\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Посадка\З натягом"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Посадка\З натягом\Є причиною нерухомості з'єднання\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

# факт:
KB[r"""Base\Фактор\Геометричні параметри\Посадка\З натягом\Є причиною нерухомості з'єднання"""]=KB[r"""Base\Факт"""]()

#path=Base\Фактор\Геометричні параметри\Посадка\Оптимальна\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Посадка\Оптимальна"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Посадка\Перехідна\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Посадка\Перехідна"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Відношення діаметру до кроку\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Відношення діаметру до кроку"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Відношення діаметру до кроку\Велике\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Відношення діаметру до кроку\Велике"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Великий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Малий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Малий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий\З концентратором напружень\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий\З концентратором напружень"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина гайки\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина гайки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина гайки\Велика\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина гайки\Велика"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина головки болта\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина головки болта"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина головки болта\Велика\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина головки болта\Велика"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина зарізьбової канавки\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина зарізьбової канавки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина зарізьбової канавки\Велика\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина зарізьбової канавки\Велика"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина згвинчування\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина згвинчування"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина згвинчування\Мала\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина згвинчування\Мала"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Крок різьби\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Крок різьби"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Великий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Оптимальний\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Оптимальний"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Кут профілю\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Великий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Малий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Малий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Перекриття витків"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Велике\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Велике"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Мале\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Мале"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Радіус впадин різьби\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Радіус впадин різьби"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Радіус впадин різьби\Збільшення\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Радіус впадин різьби\Збільшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Великий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Малий\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Малий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\class.pykb
#open=0
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Велика\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Велика"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Мала\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Мала"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Шорсткість\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1
KB[r"""Base\Фактор\Геометричні параметри\Шорсткість"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Шорсткість\Висока\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Висока"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Шорсткість\Низька\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Геометричні параметри\Шорсткість\Низька\Леговані сталі\class.pykb
#open=1
#fg=blue
#bg=darkolivegreen1

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька\Леговані сталі"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Герметичність\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Герметичність"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Герметичність\Низька\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Герметичність\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Деталі\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Болт\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Болт"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Болт\Болт під розвертку\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Болт\Болт під розвертку"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Гайка\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Гайка"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Гайка\Гайка розтягу-стиску\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Гайка\Гайка розтягу-стиску"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Гвинт\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Гвинт"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Гвинтова вставка\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Гвинтова вставка"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\З'єднувані деталі\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\З'єднувані деталі"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\З'єднувані деталі\Мала кількість\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1

KB[r"""Base\Фактор\Деталі\З'єднувані деталі\Мала кількість"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Деталі\З'єднувані деталі з різьбою\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\З'єднувані деталі з різьбою"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\З'єднувані деталі з різьбою\З внутрішньою різьбою\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\З'єднувані деталі з різьбою\З внутрішньою різьбою"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\З'єднувані деталі з різьбою\З зовнішньою різьбою\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\З'єднувані деталі з різьбою\З зовнішньою різьбою"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Захисний ковпачок\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Захисний ковпачок"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Компенсатори температурних деформацій\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Компенсатори температурних деформацій"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Протектори\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Протектори"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Сферична шайба\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Сферична шайба"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Шайба\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Шайба"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Деталі\Шайба\З низьковуглецевої сталі\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1

KB[r"""Base\Фактор\Деталі\Шайба\З низьковуглецевої сталі"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Деталі\Шайба\Пружинна\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1

KB[r"""Base\Фактор\Деталі\Шайба\Пружинна"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Деталі\Шайба\Сферична\class.pykb
#open=1
#fg=blue
#bg=darkseagreen1

KB[r"""Base\Фактор\Деталі\Шайба\Сферична"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Деталі\Шпилька\class.pykb
#open=0
#fg=blue
#bg=darkseagreen1
KB[r"""Base\Фактор\Деталі\Шпилька"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Жорсткість\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Жорсткість"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Жорсткість\Болта\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Жорсткість\Болта"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Жорсткість\Болта\Мала\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Жорсткість\Болта\Мала"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Жорсткість\З'єднуваних деталей\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Жорсткість\З'єднуваних деталей\Мала\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей\Мала"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Загальні напрямки підвищення надійності\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальних допусків і шорсткості\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальних допусків і шорсткості"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальної технології\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальної технології"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Запобігання заїдань\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Запобігання заїдань"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Запобігання розгерметизації\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Запобігання розгерметизації"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійно-втомного і статичного руйнування\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійно-втомного і статичного руйнування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійного руйнування\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійного руйнування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від механічного спрацювання деталей\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від механічного спрацювання деталей"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від середовища\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від середовища"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист при транспортуванні\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист при транспортуванні"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Зменшення концентрації напружень\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Зменшення концентрації напружень"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Зменшення механічного спрацювання витків\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Зменшення механічного спрацювання витків"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Підбір матеріалів і термообробки\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Підбір матеріалів і термообробки"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Попередження самовідгвинчування\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Попередження самовідгвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Загальні напрямки підвищення надійності\Центрування різьби запобігання згину\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Центрування різьби запобігання згину"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Залишкові напруження\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Залишкові напруження"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Залишкові напруження\Розтягу\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Залишкові напруження\Розтягу"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Залишкові напруження\Розтягу\Чутливість\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Залишкові напруження\Розтягу\Чутливість"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Залишкові напруження\Стиску\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Залишкові напруження\Стиску"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Залишкові напруження\Стиску\За високої температури\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Залишкові напруження\Стиску\За високої температури"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Згвинчуваність\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Згвинчуваність"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Згвинчуваність\Добра\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Згвинчуваність\Добра"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Згвинчуваність\Погана\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Згвинчуваність\Погана"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Змащення\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Змащення"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Змащення\Відсутність\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Змащення\Відсутність"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Змащення\Дисульфід молібдена\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Змащення\Дисульфід молібдена"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Гайка з осьовими прорізями\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Гайка з осьовими прорізями"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Герметизуючі елементи\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Герметизуючі елементи"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Зарізьбова канавка\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Зарізьбова канавка"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Опорні поверхні\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Опорні поверхні"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Опорні поверхні\Конічні\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Опорні поверхні\Конічні"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Опорні поверхні\Сферичні\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Опорні поверхні\Сферичні"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Асиметрична різьба\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Асиметрична різьба"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Різьба\Збіг\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Збіг"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Змінний середній діаметр різьби гайки\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Змінний середній діаметр різьби гайки"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Кількість заходів\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Кількість заходів"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Кількість заходів\Багатозахідна\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Кількість заходів\Багатозахідна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Кількість заходів\Однозахідна\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Кількість заходів\Однозахідна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\Змінний крок\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок\Змінний крок"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Збільшення кроку гайки\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Збільшення кроку гайки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Зменшення кроку болта\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Зменшення кроку болта"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\Ліва\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\Ліва"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\Права\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\Права"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Обтиск останніх витків різьби муфти\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Обтиск останніх витків різьби муфти"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Дюймова\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Дюймова"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Метрична\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Метрична"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Модульна\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Модульна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Пітчева\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Одиниця кроку\Пітчева"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Податливі витки\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Податливі витки"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Податливі витки\Перші витки гайки\class.pykb
#open=1
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Податливі витки\Перші витки гайки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Різьба\Призначення\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Призначення"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Призначення\Кріпильна\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Призначення\Кріпильна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Призначення\Спеціальна\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Призначення\Спеціальна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Призначення\Ходова\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Призначення\Ходова"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Розміщення\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Розміщення"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Розміщення\Внутрішня\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Розміщення\Внутрішня"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Розміщення\Зовнішня\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Розміщення\Зовнішня"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Розтиск останніх витків різьби ніпеля\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Розтиск останніх витків різьби ніпеля"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Розтиск перших витків різьби муфти\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Розтиск перших витків різьби муфти"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Фаски\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Фаски"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Фаски\Зріз перших витків різьби муфти\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Фаски\Зріз перших витків різьби муфти"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Кругла\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Кругла"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Прямокутна\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Прямокутна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Спеціальна\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Спеціальна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Трапецеїдальна\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Трапецеїдальна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Трикутна\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Трикутна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Упорна\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Упорна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні\Конічна\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні\Конічна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні\Циліндрична\class.pykb
#open=1
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні\Циліндрична"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта"""]=KB[r"""Base\Фактор"""]()

#92
#path=Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Вільні витки болта\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Вільні витки болта"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Різьба болта утоплена в гайку\class.pykb
#open=0
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Різьба болта утоплена в гайку"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Форма головки болта\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Форма головки болта"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Конструкційні елементи\Форма головки болта\Двухрадіусна галтель\class.pykb
#open=1
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Форма головки болта\Двухрадіусна галтель"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Форма головки болта\Оптимальна\class.pykb
#open=1
#fg=blue
#bg=yellowgreen

KB[r"""Base\Фактор\Конструкційні елементи\Форма головки болта\Оптимальна"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Конструкційні елементи\Центруючі елементи\class.pykb
#open=0
#fg=blue
#bg=yellowgreen
KB[r"""Base\Фактор\Конструкційні елементи\Центруючі елементи"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Концентрація напружень\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Концентрація напружень"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Концентрація напружень\Низька\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Концентрація напружень\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Концентрація напружень\Під головкою болта\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Концентрація напружень\Під головкою болта\Низька\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Міцність"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Міцність\За зрізуючого навантаження\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За зрізуючого навантаження"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\За осьового навантаження\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За осьового навантаження"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\За статичного навантаження\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За статичного навантаження"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\За статичного навантаження\Висока\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За статичного навантаження\Висока"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\За статичного навантаження\Низька\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\За циклічного навантаження\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За циклічного навантаження"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\За циклічного навантаження\Висока\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\За циклічного навантаження\Низька\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Міцність\Низька\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Міцність\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Маса\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Маса"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Маса\Велика\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Маса\Велика"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Маса\Мала\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Маса\Мала"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Масштабний фактор\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Масштабний фактор"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Масштабний фактор\Великі розміри\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Масштабний фактор\Великі розміри"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Масштабний фактор\Малі розміри\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Масштабний фактор\Малі розміри"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Алюмінієві сплави\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Алюмінієві сплави"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Алюмінієві сплави\Гайки\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Алюмінієві сплави\Гайки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Бериллієві сплави\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Бериллієві сплави"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Бесемерівська сталь\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Бесемерівська сталь"""]=KB[r"""Base\Фактор"""]()

r"""http://ru.wikipedia.org/wiki/%D0%91%D0%B5%D1%81%D1%81%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F_%D1%81%D1%82%D0%B0%D0%BB%D1%8C"""

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""]=KB[r"""Base\Фактор"""]()
#142
#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1400\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1400"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1600\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1600"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1800-2100\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1800-2100"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\За високих моментів згвинчування і агресивного середовища\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\За високих моментів згвинчування і агресивного середовища"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Зарізьбова канавка\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Зарізьбова канавка"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Зниження водневої крихкості\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Зниження водневої крихкості"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Кадміювання\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Кадміювання"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Накатування\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Накатування"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Полірування\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Полірування"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Спеціальна термічна обробка високоміцних болтів з легованних сталей\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Спеціальна термічна обробка високоміцних болтів з легованних сталей"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6\Обробка холодом\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6\Обробка холодом"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш\Обробка холодом\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш\Обробка холодом"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Вуглець у поверхневих шарах\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Зменшення\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Неоптимальний\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Неоптимальний"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Оптимальний\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Оптимальний"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Вуглець фосфор азот на границях зерен\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Вуглець фосфор азот на границях зерен"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Газонасочений шар\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Газонасочений шар"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Жароміцні сплави\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Жароміцні сплави"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Жароміцні сплави\Висока робоча температура\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Жароміцні сплави\Висока робоча температура"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Коефіцієнт лінійного розширення\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Коефіцієнт лінійного розширення"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Коефіцієнт лінійного розширення\Гайки\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Коефіцієнт лінійного розширення\Гайки"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Коефіцієнт лінійного розширення\Гайки\Великий\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Коефіцієнт лінійного розширення\Гайки\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Корозійностійкі матеріали\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Корозійностійкі матеріали\Сталі\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали\Сталі"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Кремнієві сталі\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Кремнієві сталі"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Крихкість\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Крихкість"""]=KB[r"""Base\Фактор"""]()

r"""http://ru.wikipedia.org/wiki/%D0%A5%D1%80%D1%83%D0%BF%D0%BA%D0%BE%D1%81%D1%82%D1%8C"""

#path=Base\Фактор\Матеріал\Крихкий поверхневий шар\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Крихкий поверхневий шар"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Матеріали з метастабільною структурою і малою пластичністю\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Матеріали з метастабільною структурою і малою пластичністю"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Молібден\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Молібден"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Ніобій\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Ніобій"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Надвисокоміцні сталі\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Надвисокоміцні сталі"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Насичення атомарним воднем\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Насичення атомарним воднем"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Наявність азоту\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Наявність азоту"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Наявність фосфору\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Наявність фосфору"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Пластичність\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Пластичність"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Пластичність\Висока\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Пластичність\Висока"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Пластичність\Висока\Гайки\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Пластичність\Висока\Гайки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Пластичність\Низька\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Пластмасси\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Пластмасси"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Повзучість\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Повзучість"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Протекторний захист\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Протекторний захист"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Співвідношення матеріалів\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Співвідношення матеріалів"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Співвідношення матеріалів\Неоптимальне\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Співвідношення матеріалів\Неоптимальне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Співвідношення матеріалів\Пластична гайка\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Співвідношення матеріалів\Пластична гайка"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Співвідношення матеріалів\Різні механічні властивості болта і гайки\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Співвідношення матеріалів\Різні механічні властивості болта і гайки"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Старіння сталі\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Старіння сталі"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Старіння сталі\Низьковуглецевої\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Старіння сталі\Низьковуглецевої"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Структура матеріалу\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Структура матеріалу"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Структура матеріалу\Покращення\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Структура матеріалу\Покращення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Термообробка\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Термообробка"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Термообробка\В захисній атмосфері\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Термообробка\В захисній атмосфері"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Термообробка\Відпуск\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Термообробка\Відпуск"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Термообробка\Відпуск\Збільшення температури відпуску\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Термообробка\Відпуск\Збільшення температури відпуску"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Термообробка\Відпуск\Недостатній після гартування\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Термообробка\Відпуск\Недостатній після гартування"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Термообробка\Гартування\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Термообробка\Гартування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Термообробка\Гартування\Перегрів при гартуванні\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Термообробка\Гартування\Перегрів при гартуванні"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Термообробка\Термообробка заготовок\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Термообробка\Термообробка заготовок"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\Азотування\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\Азотування"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\Азотування\Високий момент згвинчування\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\Азотування\Високий момент згвинчування"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Технологічні дефекти матеріалів\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Технологічні дефекти матеріалів"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Титанові сплави\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Титанові сплави"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Токсичність\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Токсичність"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Холодноламкість\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Холодноламкість"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Холодноламкість\Низька\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Холодноламкість\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Чутливість до концентрації напружень\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1
KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Матеріал\Чутливість до концентрації напружень\Низька\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Электричний опір\class.pykb
#open=0
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Электричний опір"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Матеріал\Электричний опір\Великий\class.pykb
#open=1
#fg=blue
#bg=lightsteelblue1

KB[r"""Base\Фактор\Матеріал\Электричний опір\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Навантаження\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Вібрація\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Вібрація"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Згинаюче\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Згинаюче"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Зрізаюче\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Зрізаюче"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Крутне\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Крутне"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Крутне\Догвинчування\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Крутне\Догвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Крутне\Розгвинчування\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Крутне\Розгвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Осьове\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Осьове"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Осьове\Розтягу\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Осьове\Розтягу"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Осьове\Стиску\class.pykb
#open=1
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Осьове\Стиску"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Статичне\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Статичне"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Температурне\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Температурне"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Температурне\Зменшення\class.pykb
#open=1
#fg=blue
#bg=gold2

KB[r"""Base\Фактор\Навантаження\Температурне\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Навантаження\Тиск\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Тиск"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Удар\class.pykb
#open=0
#fg=blue
#bg=gold2
KB[r"""Base\Фактор\Навантаження\Удар"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Циклічне\class.pykb
#open=0
#fg=blue
#bg=gold2

KB[r"""Base\Фактор\Навантаження\Циклічне"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Навантаження\Швидкісне\class.pykb
#open=0
#fg=blue
#bg=gold2

KB[r"""Base\Фактор\Навантаження\Швидкісне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Навантаження\Швидкісне\Низьковуглецева сталь\class.pykb
#open=1
#fg=blue
#bg=gold2

KB[r"""Base\Фактор\Навантаження\Швидкісне\Низьковуглецева сталь"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Згину\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Згину"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Згину\Зменшення\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""]=KB[r"""Base\Фактор"""]()

r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#18"""
#path=Base\Фактор\Напруження\Зрізу\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Зрізу"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Зрізу\Зменшення\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Зрізу\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Кручення\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Кручення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Кручення\Зменшення\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Кручення\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Розтягу\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Розтягу"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Розтягу\Болта\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Розтягу\Болта"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Напруження\Розтягу\Болта\Зменшення\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Напруження\Розтягу\Болта\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Покриття"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Покриття\Багатошарове мідь-нікель\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Багатошарове мідь-нікель"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Багатошарове мідь-нікель, хром\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Багатошарове мідь-нікель, хром"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Електрохімічна обробка\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Електрохімічна обробка"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Зносостійкі\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Покриття\Зносостійкі"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Покриття\Кадмієве з хроматуванням\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Кадмієве з хроматуванням"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Корозійностійкі\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Покриття\Корозійностійкі"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Покриття\Мідне\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Мідне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Нікелеве\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Нікелеве"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Оксидне\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Оксидне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Оксидне анодізаційне з хроматуванням\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Оксидне анодізаційне з хроматуванням"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Оксидне з кислих розчинів\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Оксидне з кислих розчинів"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Олов'яне\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Олов'яне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Оптимальне\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Оптимальне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Пластичне\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Пластичне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Свинцеве\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Свинцеве"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Срібне\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Срібне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Травлення під час нанесення покриттів\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Травлення під час нанесення покриттів"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Фосфатне\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Фосфатне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Цинкове\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Цинкове"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Покриття\Цинкове з хроматуванням\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Покриття\Цинкове з хроматуванням"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Від високошвидкісного навантаження\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Від високошвидкісного навантаження"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Втомна тріщина\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Втомна тріщина\В останньому витку муфти\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\В останньому витку муфти"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Втомна тріщина\В першому витку ніпеля\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\В першому витку ніпеля"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Втомна тріщина\Під головкою болта\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\Під головкою болта"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Заїдання\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Заїдання"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Заїдання\Зменшення\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Заїдання\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Залишкова деформація\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки\Зменшення\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\Зменшення\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\Зменшення\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Залишкова деформація\Обрив стержня\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Обрив стержня"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\Абразивний\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос\Абразивний"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\Адгезійний\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос\Адгезійний"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\Втомний\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос\Втомний"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\Ерозійний\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос\Ерозійний"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\Зменшення\class.pykb
#open=0
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Знос\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Знос\Механохімічний\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос\Механохімічний"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\Фретинг-корозійний\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос\Фретинг-корозійний"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Знос\Фретинговий\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Знос\Фретинговий"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Корозійна\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Корозійна"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Корозійна\Низька\class.pykb
#open=0
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Корозійне розтріскування\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Крихкий злам\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Крихкий злам"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\class.pykb
#open=1
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Розгерметизація\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Розгерметизація"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Розгерметизація\Запобігання\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Розгерметизація\Запобігання"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження\Самовідгвинчування\class.pykb
#open=0
#fg=blue
#bg=lightpink
KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення\class.pykb
#open=1
#fg=blue
#bg=lightpink

KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження при транспортуванні\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Пошкодження при транспортуванні"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Пошкодження при транспортуванні\Зменшення\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Пошкодження при транспортуванні\Зменшення"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Розкриття стику\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Розкриття стику"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Рухомість з'єднання\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Рухомість з'єднання"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Рухомість з'єднання\Низька\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Рухомість з'єднання\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Середовище\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Середовище"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Середовище\Інгібіторний захист\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Середовище\Інгібіторний захист"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Середовище\Корозійне\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Середовище\Корозійне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Середовище\Корозійне\Захист\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Середовище\Корозійне\Захист"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Складання\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Згвинчування в нагрітому стані\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Згвинчування в нагрітому стані"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Контргайка затянута великим моментом\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Контргайка затянута великим моментом"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Контроль затягування\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Контроль затягування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Контроль затягування\Контроль за видовженням болта\class.pykb
#open=1
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Контроль затягування\Контроль за видовженням болта"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Контроль затягування\Контроль за кутом повороту\class.pykb
#open=1
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Контроль затягування\Контроль за кутом повороту"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Контроль затягування\Контроль за моментом згвинчування\class.pykb
#open=1
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Контроль затягування\Контроль за моментом згвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Момент згвинчування\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Момент згвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Момент згвинчування\Неоптимальний\class.pykb
#open=0
#fg=blue
#bg=burlywood1

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий\class.pykb
#open=1
#fg=blue
#bg=burlywood1

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Малий\class.pykb
#open=1
#fg=blue
#bg=burlywood1

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Малий"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Складання\Момент згвинчування\Оптимальний\class.pykb
#open=0
#fg=blue
#bg=burlywood1

KB[r"""Base\Фактор\Складання\Момент згвинчування\Оптимальний"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Складання\Очищення різьби\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Очищення різьби"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Попереднє пластичне деформування перших витків\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Попереднє пластичне деформування перших витків"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Правила згвинчування\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Правила згвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Селекційне складання\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Селекційне складання"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Тертя при згвинчуванні\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Тертя при згвинчуванні"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Уникнення перекосів\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Уникнення перекосів"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Фіксація болта при згвинчуванні\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Фіксація болта при згвинчуванні"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Складання\Часте згвинчування розгвинчування\class.pykb
#open=0
#fg=blue
#bg=burlywood1
KB[r"""Base\Фактор\Складання\Часте згвинчування розгвинчування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Стопоріння\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Стопоріння"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Стопоріння\Жорстке\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Стопоріння\Жорстке"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Стопоріння\Клеєм\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Стопоріння\Клеєм"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Стопоріння\Фрикційне\class.pykb
#open=1
#fg=blue
#bg=white
KB[r"""Base\Фактор\Стопоріння\Фрикційне"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Температура"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\Висока\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\Мінімальна\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Мінімальна"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\Мінімальна\-196\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Мінімальна\-196"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\Максимальна\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\Максимальна\150\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\150"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Температура\Робоча температура\Максимальна\200\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\200"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Температура\Робоча температура\Максимальна\300\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\300"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Температура\Робоча температура\Максимальна\350-550\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\350-550"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\Максимальна\400\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\400"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Робоча температура\Максимальна\600\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\600"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Температура\Робоча температура\Максимальна\900\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\900"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Температура\Робоча температура\Низька\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Температура за залишкових напруженнях стиску\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Температура\Температура за залишкових напруженнях стиску"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Температура\Температура за залишкових напруженнях стиску\Висока\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Температура\Температура за залишкових напруженнях стиску\Висока"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\class.pykb
#open=0
#fg=blue
#bg=white
KB[r"""Base\Фактор\Тертя"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Зменшується\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Зменшується"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\На різьбі\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\На різьбі"""]=KB[r"""Base\Фактор"""]()
#345
#path=Base\Фактор\Тертя\На різьбі\Велике\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\На різьбі\Велике"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\На різьбі\Мале\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\На упорному бурті\class.pykb
#open=0
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\На упорному бурті"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\На упорному бурті\Велике\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\На упорному бурті\Велике"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Тертя\На упорному бурті\Мале\class.pykb
#open=1
#fg=blue
#bg=white

KB[r"""Base\Фактор\Тертя\На упорному бурті\Мале"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Технологія\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Комбіноване нарізання і обкатування\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Комбіноване нарізання і обкатування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Аксіальними головками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Аксіальними головками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Головками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Головками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Кількома роликами\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Кількома роликами"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Мітчиками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Мітчиками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Планетарне\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Планетарне"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Плоскими плашками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Плоскими плашками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Роликом сегментом\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Роликом сегментом"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента\class.pykb
#open=0
#fg=blue
#bg=mistyrose

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента\Низька\class.pykb
#open=1
#fg=blue
#bg=mistyrose

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента\Низька"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Тангенціальними головками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Тангенціальними головками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Вихрове\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Вихрове"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Головками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Головками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Гребінками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Гребінками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Мітчиками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Мітчиками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Плашками\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Плашками"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Протягування\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Протягування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Різцями\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Різцями"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Фрезами\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Фрезами"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання\Шліфкругами\class.pykb
#open=1
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання\Шліфкругами"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Нарізання багатозахідне\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Нарізання багатозахідне"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Обкатування після нарізання\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Обкатування після нарізання"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Піскоструминна обробка\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Піскоструминна обробка"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Метод виготовлення\Полірування\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Метод виготовлення\Полірування"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Попередній статичний розтяг високоміцних болтів\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Попередній статичний розтяг високоміцних болтів"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Режими обробки\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Режими обробки"""]=KB[r"""Base\Фактор"""]()
#path=Base\Фактор\Технологія\Режими обробки\Оптимальні\class.pykb
#open=1
#fg=blue
#bg=mistyrose

KB[r"""Base\Фактор\Технологія\Режими обробки\Оптимальні"""]=KB[r"""Base\Фактор"""]()

#path=Base\Фактор\Технологія\Технологічні дефекти\class.pykb
#open=0
#fg=blue
#bg=mistyrose
KB[r"""Base\Фактор\Технологія\Технологічні дефекти"""]=KB[r"""Base\Фактор"""]()

#path=Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\delta_ln\10\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\delta_ln\10"""].create()
KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\delta_ln\10"""].p['bolt_load'][1]=-0.1
KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\delta_ln\10"""].p['delta_ln'][1]=10

#path=Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1"""].create()
KB[r"""Base\Модель\ГОСТ 13877-96\ШН 19\bolt_load\0.1"""].p['bolt_load'][1]=-0.1
#path=Base\Фактор\Геометричні параметри\Допуск розміру\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором"""])

#path=Base\Фактор\Геометричні параметри\Допуск розміру\Малий\prop.pykb
#open=0
#fg=red
#bg=white
KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру\Малий"""].__dict__["isEffect"].add(KB[r"""Base\Фактор\Складання\Селекційне складання"""])

KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру\Малий"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру\Великий"""])

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину"""])

r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#17"""

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Високоміцних сталей\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Високоміцних сталей"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Зменшення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Зменшення"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Великий"""])

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Зменшення"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь"""])

#path=Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину"""])

r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#17"""

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей\Малий"""])

#path=Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Нечутливість до перекосу"""])

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""])

#path=Base\Фактор\Геометричні параметри\Посадка\З зазором\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Рухомість з'єднання"""])

#path=Base\Фактор\Геометричні параметри\Посадка\З зазором\Зменшення діаметральних зазорів\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором\Зменшення діаметральних зазорів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором\Зменшення діаметральних зазорів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])


KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором\Зменшення діаметральних зазорів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

#path=Base\Фактор\Геометричні параметри\Посадка\З натягом\prop.pykb
#open=0
#fg=red
#bg=white

X=KB[r"""Base\Фактор\Геометричні параметри\Посадка\З натягом"""]
X.__dict__["isCause"].add(KB[r"""Base\Фактор\Рухомість з'єднання\Низька"""])


KB[r"""Base\Фактор\Геометричні параметри\Посадка\З натягом"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Геометричні параметри\Посадка\З натягом"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""])

#path=Base\Фактор\Геометричні параметри\Посадка\З натягом\Є причиною нерухомості з'єднання\prop.pykb
#open=0
#fg=red
#bg=white

# властивості факту:
X=KB[r"""Base\Фактор\Геометричні параметри\Посадка\З натягом\Є причиною нерухомості з'єднання"""]
X.create(
r"""Base\Фактор\Геометричні параметри\Посадка\З натягом""",
'isCause',
r"""Base\Фактор\Рухомість з'єднання\Низька"""
)

X.__dict__["hasReference"].add(KB[r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения"""])
del X

# Нерухомість з'єднання забезпечується за рахунок натягу по середньому діаметру
# посилання:
r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#9"""


#path=Base\Фактор\Геометричні параметри\Посадка\Оптимальна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Посадка\Оптимальна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Геометричні параметри\Посадка\Оптимальна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

#path=Base\Фактор\Геометричні параметри\Посадка\Перехідна\prop.pykb
#open=0
#fg=red
#bg=white
KB[r"""Base\Фактор\Геометричні параметри\Посадка\Перехідна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Рухомість з'єднання\Низька"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Відношення діаметру до кроку\Велике\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Відношення діаметру до кроку\Велике"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Висока"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Великий"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Малий"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр зарізьбової канавки\Малий\prop.pykb
#open=0
#fg=red
#bg=white

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\Зменшення"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий\З концентратором напружень\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Діаметр різьби\Великий\З концентратором напружень"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина гайки\Велика\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина гайки\Велика"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#91

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина гайки\Велика"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\Зменшення"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина головки болта\Велика\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина головки болта\Велика"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта\Низька"""])
#132
#path=Base\Фактор\Геометричні параметри\Розмір\Довжина зарізьбової канавки\Велика\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина зарізьбової канавки\Велика"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Жорсткість\Болта\Мала"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Довжина згвинчування\Мала\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Довжина згвинчування\Мала"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])
#137
#path=Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\Зменшення"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Оптимальний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Крок різьби\Оптимальний"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Великий"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Малий"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Малий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Малий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])
#95

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Кут профілю\Малий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Велике\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Велике"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])
#163
#path=Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Мале\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Мале"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Велике"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Перекриття витків\Мале"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Радіус впадин різьби\Збільшення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Радіус впадин різьби\Збільшення"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке"""])


KB[r"""Base\Фактор\Геометричні параметри\Розмір\Радіус впадин різьби\Збільшення"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Великий"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Малий"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Масштабний фактор\Великі розміри"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Типорозмір різьби\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Маса\Велика"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Велика\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Велика"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Велика"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Велика"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Мала"""])

#path=Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Мала\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Розмір\Товщина гайки\Мала"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Упорна"""])
#161
#path=Base\Фактор\Геометричні параметри\Шорсткість\Висока\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень"""])

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна"""])

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Геометричні параметри\Шорсткість\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька"""].__dict__["Not"].add(KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Висока"""])

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""])

#path=Base\Фактор\Геометричні параметри\Шорсткість\Низька\Леговані сталі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька\Леговані сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька\Леговані сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

#path=Base\Фактор\Герметичність\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Герметичність"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Середовище\Корозійне\Захист"""])

KB[r"""Base\Фактор\Герметичність"""].__dict__["Not"].add(KB[r"""Base\Фактор\Герметичність\Низька"""])

#path=Base\Фактор\Герметичність\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Герметичність\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Розгерметизація"""])

#path=Base\Фактор\Деталі\Болт\Болт під розвертку\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Болт\Болт під розвертку"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Зрізу\Зменшення"""])
r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#22"""
#path=Base\Фактор\Деталі\Гайка\Гайка розтягу-стиску\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Гайка\Гайка розтягу-стиску"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])
#99
#path=Base\Фактор\Деталі\Гвинтова вставка\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Гвинтова вставка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

KB[r"""Base\Фактор\Деталі\Гвинтова вставка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Зменшення механічного спрацювання витків"""])

#path=Base\Фактор\Деталі\З'єднувані деталі\Мала кількість\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\З'єднувані деталі\Мала кількість"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""])

#path=Base\Фактор\Деталі\Захисний ковпачок\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Захисний ковпачок"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження при транспортуванні\Зменшення"""])

#path=Base\Фактор\Деталі\Компенсатори температурних деформацій\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Компенсатори температурних деформацій"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Навантаження\Температурне\Зменшення"""])

#path=Base\Фактор\Деталі\Протектори\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\Фактор\Деталі\Протектори"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Знос\Зменшення"""])

#path=Base\Фактор\Деталі\Сферична шайба\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Сферична шайба"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""])

r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#18"""
#path=Base\Фактор\Деталі\Шайба\З низьковуглецевої сталі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Шайба\З низьковуглецевої сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос опорних поверхонь\Зменшення"""])
#169
#path=Base\Фактор\Деталі\Шайба\Пружинна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Шайба\Пружинна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""])

#path=Base\Фактор\Деталі\Шайба\Сферична\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Деталі\Шайба\Сферична"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""])

#path=Base\Фактор\Жорсткість\Болта\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Жорсткість\Болта"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Розтягу\Болта"""])

KB[r"""Base\Фактор\Жорсткість\Болта"""].__dict__["Not"].add(KB[r"""Base\Фактор\Жорсткість\Болта\Мала"""])

#path=Base\Фактор\Жорсткість\З'єднуваних деталей\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Розтягу\Болта\Зменшення"""])

KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей"""].__dict__["Not"].add(KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей\Мала"""])

#path=Base\Фактор\Жорсткість\З'єднуваних деталей\Мала\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей\Мала"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей\Мала"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Жорсткість\З'єднуваних деталей\Мала"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальних допусків і шорсткості\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальних допусків і шорсткості"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальної технології\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальної технології"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Залишкові напруження\Стиску"""])

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Вибір оптимальної технології"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Шорсткість\Низька"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Запобігання заїдань\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Запобігання заїдань"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання\Зменшення"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Запобігання розгерметизації\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Запобігання розгерметизації"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійно-втомного і статичного руйнування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійно-втомного і статичного руйнування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійного руйнування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від корозійного руйнування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від механічного спрацювання деталей\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від механічного спрацювання деталей"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Знос\Зменшення"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист від середовища\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від середовища"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Середовище\Корозійне\Захист"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Захист при транспортуванні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист при транспортуванні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження при транспортуванні\Зменшення"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Зменшення концентрації напружень\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Зменшення концентрації напружень"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Підбір матеріалів і термообробки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Підбір матеріалів і термообробки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Підбір матеріалів і термообробки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Попередження самовідгвинчування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Попередження самовідгвинчування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""])

#path=Base\Фактор\Загальні напрямки підвищення надійності\Центрування різьби запобігання згину\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Центрування різьби запобігання згину"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""])

#path=Base\Фактор\Залишкові напруження\Розтягу\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Залишкові напруження\Розтягу"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Залишкові напруження\Розтягу"""].__dict__["Not"].add(KB[r"""Base\Фактор\Залишкові напруження\Стиску"""])

#path=Base\Фактор\Залишкові напруження\Розтягу\Чутливість\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Залишкові напруження\Розтягу\Чутливість"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Залишкові напруження\Стиску\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Залишкові напруження\Стиску"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

#path=Base\Фактор\Залишкові напруження\Стиску\За високої температури\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Залишкові напруження\Стиску\За високої температури"""].__dict__["And"].add(KB[r"""Base\Фактор\Залишкові напруження\Стиску"""])

KB[r"""Base\Фактор\Залишкові напруження\Стиску\За високої температури"""].__dict__["And"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""])

KB[r"""Base\Фактор\Залишкові напруження\Стиску\За високої температури"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Згвинчуваність\Погана\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Згвинчуваність\Погана"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Кручення"""])

KB[r"""Base\Фактор\Згвинчуваність\Погана"""].__dict__["Not"].add(KB[r"""Base\Фактор\Згвинчуваність\Добра"""])

KB[r"""Base\Фактор\Згвинчуваність\Погана"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Змащення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Змащення"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""])

KB[r"""Base\Фактор\Змащення"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На упорному бурті\Мале"""])

KB[r"""Base\Фактор\Змащення"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання\Зменшення"""])

KB[r"""Base\Фактор\Змащення"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Зменшення механічного спрацювання витків"""])

#path=Base\Фактор\Змащення\Відсутність\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Змащення\Відсутність"""].__dict__["Not"].add(KB[r"""Base\Фактор\Змащення"""])

#path=Base\Фактор\Конструкційні елементи\Гайка з осьовими прорізями\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Гайка з осьовими прорізями"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])
#91
#path=Base\Фактор\Конструкційні елементи\Герметизуючі елементи\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Герметизуючі елементи"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність"""])

#path=Base\Фактор\Конструкційні елементи\Зарізьбова канавка\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Зарізьбова канавка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""])

KB[r"""Base\Фактор\Конструкційні елементи\Зарізьбова канавка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])
#142
#path=Base\Фактор\Конструкційні елементи\Опорні поверхні\Конічні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Опорні поверхні\Конічні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""])

#path=Base\Фактор\Конструкційні елементи\Опорні поверхні\Сферичні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Опорні поверхні\Сферичні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Асиметрична різьба\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Асиметрична різьба"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])
#94
#path=Base\Фактор\Конструкційні елементи\Різьба\Збіг\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Збіг"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Висока"""])

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Збіг"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#142
#path=Base\Фактор\Конструкційні елементи\Різьба\Змінний середній діаметр різьби гайки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Змінний середній діаметр різьби гайки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\Змінний крок\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок\Змінний крок"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Збільшення кроку гайки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Збільшення кроку гайки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])
#97
#path=Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Зменшення кроку болта\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Крок\Неоднаковий крок\Зменшення кроку болта"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])
#97
#path=Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\Ліва\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\Ліва"""].__dict__["Not"].add(KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Напрям гвинтової лінії\Права"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Обтиск останніх витків різьби муфти\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Обтиск останніх витків різьби муфти"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Податливі витки\Перші витки гайки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Податливі витки\Перші витки гайки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Розтиск останніх витків різьби ніпеля\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Розтиск останніх витків різьби ніпеля"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Розтиск перших витків різьби муфти\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Розтиск перших витків різьби муфти"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Фаски\Зріз перших витків різьби муфти\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Фаски\Зріз перших витків різьби муфти"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Кругла\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Кругла"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Прямокутна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Прямокутна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби"""])
#95
#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Спеціальна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Спеціальна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Трикутна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Трикутна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Упорна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Упорна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби"""])
#95

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Форма профілю\Упорна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки\Зменшення"""])

#path=Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні\Конічна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Різьба\Характер поверхні\Конічна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність"""])

#path=Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Вільні витки болта\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Вільні витки болта"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Різьба болта утоплена в гайку\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Розташування різьбової частини болта\Різьба болта утоплена в гайку"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Конструкційні елементи\Форма головки болта\Двухрадіусна галтель\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Форма головки болта\Двухрадіусна галтель"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта\Низька"""])
#132
#path=Base\Фактор\Конструкційні елементи\Форма головки болта\Оптимальна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Форма головки болта\Оптимальна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])
#218
#path=Base\Фактор\Конструкційні елементи\Центруючі елементи\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Конструкційні елементи\Центруючі елементи"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""])

#path=Base\Фактор\Концентрація напружень\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Концентрація напружень"""].__dict__["Not"].add(KB[r"""Base\Фактор\Концентрація напружень\Низька"""])

KB[r"""Base\Фактор\Концентрація напружень"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Концентрація напружень"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""])

KB[r"""Base\Фактор\Концентрація напружень"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

#path=Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень"""])

KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби"""].__dict__["Not"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\В першому витку ніпеля"""])

#path=Base\Фактор\Концентрація напружень\Під головкою болта\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Концентрація напружень"""])

KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта"""].__dict__["Not"].add(KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта\Низька"""])

KB[r"""Base\Фактор\Концентрація напружень\Під головкою болта"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\Під головкою болта"""])

#path=Base\Фактор\Міцність\За зрізуючого навантаження\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За зрізуючого навантаження"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\Зменшення"""])

KB[r"""Base\Фактор\Міцність\За зрізуючого навантаження"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Міцність\За осьового навантаження\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За осьового навантаження"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Міцність\За статичного навантаження\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За статичного навантаження"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Міцність\За статичного навантаження\Висока\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За статичного навантаження\Висока"""].__dict__["Not"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""])

#path=Base\Фактор\Міцність\За статичного навантаження\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""])

KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам"""])

#path=Base\Фактор\Міцність\За циклічного навантаження\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За циклічного навантаження"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Міцність\За циклічного навантаження\Висока\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""].__dict__["Not"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Міцність\За циклічного навантаження\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

#path=Base\Фактор\Міцність\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Міцність\Низька"""].__dict__["Not"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Маса\Мала\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Маса\Мала"""].__dict__["Not"].add(KB[r"""Base\Фактор\Маса\Велика"""])

#path=Base\Фактор\Масштабний фактор\Великі розміри\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Масштабний фактор\Великі розміри"""].__dict__["Not"].add(KB[r"""Base\Фактор\Масштабний фактор\Малі розміри"""])

KB[r"""Base\Фактор\Масштабний фактор\Великі розміри"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Матеріал\Алюмінієві сплави\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Алюмінієві сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Маса\Мала"""])

#path=Base\Фактор\Матеріал\Алюмінієві сплави\Гайки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Алюмінієві сплави\Гайки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Матеріал\Бериллієві сплави\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Бериллієві сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Маса\Мала"""])

KB[r"""Base\Фактор\Матеріал\Бериллієві сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""])

KB[r"""Base\Фактор\Матеріал\Бериллієві сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування"""])

KB[r"""Base\Фактор\Матеріал\Бериллієві сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Алюмінієві сплави\Гайки"""])

KB[r"""Base\Фактор\Матеріал\Бериллієві сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Токсичність"""])
#146

KB[r"""Base\Фактор\Матеріал\Бериллієві сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""])

#path=Base\Фактор\Матеріал\Бесемерівська сталь\prop.pykb
#open=0
#fg=red
#bg=white

# не рекомендується для виготовлення кріпильних деталей
r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#12"""

KB[r"""Base\Фактор\Матеріал\Бесемерівська сталь"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Наявність азоту"""])
KB[r"""Base\Фактор\Матеріал\Бесемерівська сталь"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Наявність фосфору"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\Зменшення"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1400\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1400"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1400"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\400"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1600\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1100-1600"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За осьового навантаження"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1800-2100\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Границя міцності\1800-2100"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За зрізуючого навантаження"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\За високих моментів згвинчування і агресивного середовища\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\За високих моментів згвинчування і агресивного середовища"""].__dict__["And"].add(KB[r"""Base\Фактор\Середовище\Корозійне"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\За високих моментів згвинчування і агресивного середовища"""].__dict__["And"].add(KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\За високих моментів згвинчування і агресивного середовища"""].__dict__["And"].add(KB[r"""Base\Фактор\Матеріал\Вуглець фосфор азот на границях зерен"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\За високих моментів згвинчування і агресивного середовища"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""])
#137
#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Зарізьбова канавка\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Зарізьбова канавка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Зниження водневої крихкості\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Зниження водневої крихкості"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Кадміювання\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Кадміювання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Накатування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Накатування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Накатування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента\Низька"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Полірування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Полірування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Спеціальна термічна обробка високоміцних болтів з легованних сталей\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Спеціальна термічна обробка високоміцних болтів з легованних сталей"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Мінімальна\-196"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Висока"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Холодноламкість\Низька"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6\Обробка холодом\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь07Х16Н6\Обробка холодом"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень\Низька"""])
#143
#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Холодноламкість\Низька"""])

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів"""])

#path=Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш\Обробка холодом\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Високоміцні сталі болтів\Сталь1Х15Н4АМ3-Ш\Обробка холодом"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень\Низька"""])

#path=Base\Фактор\Матеріал\Вуглець у поверхневих шарах\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах"""].__dict__["Not"].add(KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Зменшення"""])

#path=Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Неоптимальний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Неоптимальний"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Оптимальний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Оптимальний"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Оптимальний"""].__dict__["Not"].add(KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Неоптимальний"""])

#path=Base\Фактор\Матеріал\Вуглець фосфор азот на границях зерен\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Вуглець фосфор азот на границях зерен"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""])

#path=Base\Фактор\Матеріал\Газонасочений шар\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Газонасочений шар"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

#path=Base\Фактор\Матеріал\Жароміцні сплави\Висока робоча температура\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Жароміцні сплави\Висока робоча температура"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""])

KB[r"""Base\Фактор\Матеріал\Жароміцні сплави\Висока робоча температура"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Чутливість до перекосу"""])
#167

KB[r"""Base\Фактор\Матеріал\Жароміцні сплави\Висока робоча температура"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

#path=Base\Фактор\Матеріал\Коефіцієнт лінійного розширення\Гайки\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Коефіцієнт лінійного розширення\Гайки\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання\Зменшення"""])

#path=Base\Фактор\Матеріал\Корозійностійкі матеріали\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""])

#path=Base\Фактор\Матеріал\Корозійностійкі матеріали\Сталі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали\Сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали\Сталі"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали"""])

#path=Base\Фактор\Матеріал\Кремнієві сталі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Кремнієві сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання\Зменшення"""])

#path=Base\Фактор\Матеріал\Крихкість\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Крихкість"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам"""])

#path=Base\Фактор\Матеріал\Крихкий поверхневий шар\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Крихкий поверхневий шар"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

#path=Base\Фактор\Матеріал\Матеріали з метастабільною структурою і малою пластичністю\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Матеріали з метастабільною структурою і малою пластичністю"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

KB[r"""Base\Фактор\Матеріал\Матеріали з метастабільною структурою і малою пластичністю"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""])

#path=Base\Фактор\Матеріал\Ніобій\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Ніобій"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Холодноламкість\Низька"""])

#path=Base\Фактор\Матеріал\Надвисокоміцні сталі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Надвисокоміцні сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""])

KB[r"""Base\Фактор\Матеріал\Надвисокоміцні сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\Зменшення"""])

#path=Base\Фактор\Матеріал\Насичення атомарним воднем\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Насичення атомарним воднем"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Крихкість"""])
#137

KB[r"""Base\Фактор\Матеріал\Насичення атомарним воднем"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

#path=Base\Фактор\Матеріал\Наявність азоту\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Наявність азоту"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Крихкість"""])

#path=Base\Фактор\Матеріал\Наявність фосфору\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Наявність фосфору"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Крихкість"""])

#path=Base\Фактор\Матеріал\Пластичність\Висока\Гайки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Пластичність\Висока\Гайки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Матеріал\Пластичність\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""])
#139

KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""].__dict__["Not"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Висока"""])

#path=Base\Фактор\Матеріал\Пластмасси\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Пластмасси"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали"""])

KB[r"""Base\Фактор\Матеріал\Пластмасси"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Электричний опір\Великий"""])

KB[r"""Base\Фактор\Матеріал\Пластмасси"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Розгерметизація\Запобігання"""])
#147

KB[r"""Base\Фактор\Матеріал\Пластмасси"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність"""])

#path=Base\Фактор\Матеріал\Повзучість\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Повзучість"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

KB[r"""Base\Фактор\Матеріал\Повзучість"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""])

#path=Base\Фактор\Матеріал\Протекторний захист\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Протекторний захист"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""])

#path=Base\Фактор\Матеріал\Співвідношення матеріалів\Неоптимальне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Співвідношення матеріалів\Неоптимальне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

#path=Base\Фактор\Матеріал\Співвідношення матеріалів\Пластична гайка\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Співвідношення матеріалів\Пластична гайка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])
#95
#path=Base\Фактор\Матеріал\Співвідношення матеріалів\Різні механічні властивості болта і гайки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Співвідношення матеріалів\Різні механічні властивості болта і гайки"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])
#137
#path=Base\Фактор\Матеріал\Старіння сталі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Старіння сталі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""])

#path=Base\Фактор\Матеріал\Старіння сталі\Низьковуглецевої\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Старіння сталі\Низьковуглецевої"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Матеріал\Структура матеріалу\Покращення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Структура матеріалу\Покращення"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

#path=Base\Фактор\Матеріал\Термообробка\В захисній атмосфері\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Термообробка\В захисній атмосфері"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Вуглець у поверхневих шарах\Зменшення"""])

#path=Base\Фактор\Матеріал\Термообробка\Відпуск\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Термообробка\Відпуск"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Матеріал\Термообробка"""])

#path=Base\Фактор\Матеріал\Термообробка\Відпуск\Збільшення температури відпуску\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Термообробка\Відпуск\Збільшення температури відпуску"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Нечутливість до перекосу"""])

#path=Base\Фактор\Матеріал\Термообробка\Відпуск\Недостатній після гартування\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\Фактор\Матеріал\Термообробка\Відпуск\Недостатній після гартування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Крихкість"""])

#136
#path=Base\Фактор\Матеріал\Термообробка\Гартування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Термообробка\Гартування"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Матеріал\Термообробка"""])

#path=Base\Фактор\Матеріал\Термообробка\Гартування\Перегрів при гартуванні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Термообробка\Гартування\Перегрів при гартуванні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Крихкість"""])

#136
#path=Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Матеріал\Термообробка"""])

#path=Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\Азотування\Високий момент згвинчування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Термообробка\Хіміко-термічна обробка\Азотування\Високий момент згвинчування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам"""])
#255
#path=Base\Фактор\Матеріал\Технологічні дефекти матеріалів\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Технологічні дефекти матеріалів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Крихкість"""])

KB[r"""Base\Фактор\Матеріал\Технологічні дефекти матеріалів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень"""])

#path=Base\Фактор\Матеріал\Титанові сплави\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Маса\Мала"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\350-550"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За зрізуючого навантаження"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Нечутливість до перекосу"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Залишкові напруження\Розтягу\Чутливість"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Корозійностійкі матеріали"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

#146

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Велике"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На упорному бурті\Велике"""])

KB[r"""Base\Фактор\Матеріал\Титанові сплави"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\Зменшення"""])



#path=Base\Фактор\Матеріал\Холодноламкість\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Холодноламкість"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""])

KB[r"""Base\Фактор\Матеріал\Холодноламкість"""].__dict__["Not"].add(KB[r"""Base\Фактор\Матеріал\Холодноламкість\Низька"""])

#path=Base\Фактор\Матеріал\Чутливість до концентрації напружень\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень"""])

KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""].__dict__["Not"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень\Низька"""])

#path=Base\Фактор\Навантаження\Вібрація\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Вібрація"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

#path=Base\Фактор\Навантаження\Згинаюче\prop.pykb
#open=0
#fg=red
#bg=white


KB[r"""Base\Фактор\Навантаження\Згинаюче"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Згину"""])

KB[r"""Base\Фактор\Навантаження\Згинаюче"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

KB[r"""Base\Фактор\Навантаження\Згинаюче"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність\Низька"""])

#path=Base\Фактор\Навантаження\Зрізаюче\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Зрізаюче"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Зрізу"""])

KB[r"""Base\Фактор\Навантаження\Зрізаюче"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня"""])

#path=Base\Фактор\Навантаження\Крутне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Крутне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Кручення"""])

#path=Base\Фактор\Навантаження\Крутне\Догвинчування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Крутне\Догвинчування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""])

KB[r"""Base\Фактор\Навантаження\Крутне\Догвинчування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])

KB[r"""Base\Фактор\Навантаження\Крутне\Догвинчування"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Навантаження\Крутне"""])

#path=Base\Фактор\Навантаження\Крутне\Розгвинчування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Крутне\Розгвинчування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

KB[r"""Base\Фактор\Навантаження\Крутне\Розгвинчування"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Навантаження\Крутне"""])

#path=Base\Фактор\Навантаження\Осьове\Розтягу\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Осьове\Розтягу"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Розтягу"""])

KB[r"""Base\Фактор\Навантаження\Осьове\Розтягу"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])

KB[r"""Base\Фактор\Навантаження\Осьове\Розтягу"""].__dict__["Not"].add(KB[r"""Base\Фактор\Навантаження\Осьове\Стиску"""])

KB[r"""Base\Фактор\Навантаження\Осьове\Розтягу"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Обрив стержня"""])

#path=Base\Фактор\Навантаження\Температурне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Температурне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Навантаження\Осьове\Розтягу"""])

KB[r"""Base\Фактор\Навантаження\Температурне"""].__dict__["Not"].add(KB[r"""Base\Фактор\Навантаження\Температурне\Зменшення"""])

#path=Base\Фактор\Навантаження\Тиск\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Тиск"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Середовище\Корозійне"""])

#path=Base\Фактор\Навантаження\Удар\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Удар"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Від високошвидкісного навантаження"""])

#path=Base\Фактор\Навантаження\Циклічне\prop.pykb
#open=1
#fg=red
#bg=white
KB[r"""Base\Фактор\Навантаження\Циклічне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

#path=Base\Фактор\Навантаження\Швидкісне\Низьковуглецева сталь\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Навантаження\Швидкісне\Низьковуглецева сталь"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])
#174
#path=Base\Фактор\Напруження\Згину\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Напруження\Згину"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

#path=Base\Фактор\Напруження\Згину\Зменшення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Напруження\Згину\Зменшення"""].__dict__["Not"].add(KB[r"""Base\Фактор\Напруження\Згину"""])

#path=Base\Фактор\Напруження\Зрізу\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Напруження\Зрізу"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня"""])

KB[r"""Base\Фактор\Напруження\Зрізу"""].__dict__["Not"].add(KB[r"""Base\Фактор\Напруження\Зрізу\Зменшення"""])

#path=Base\Фактор\Напруження\Кручення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Напруження\Кручення"""].__dict__["Not"].add(KB[r"""Base\Фактор\Напруження\Кручення\Зменшення"""])

#path=Base\Фактор\Напруження\Розтягу\Болта\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Напруження\Розтягу\Болта"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

KB[r"""Base\Фактор\Напруження\Розтягу\Болта"""].__dict__["Not"].add(KB[r"""Base\Фактор\Напруження\Розтягу\Болта\Зменшення"""])

#path=Base\Фактор\Покриття\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання\Зменшення"""])

#path=Base\Фактор\Покриття\Багатошарове мідь-нікель\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Багатошарове мідь-нікель"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\600"""])

r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#13"""
#path=Base\Фактор\Покриття\Багатошарове мідь-нікель, хром\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Багатошарове мідь-нікель, хром"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\600"""])

#path=Base\Фактор\Покриття\Електрохімічна обробка\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Електрохімічна обробка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Насичення атомарним воднем"""])
#137
#path=Base\Фактор\Покриття\Зносостійкі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Зносостійкі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Загальні напрямки підвищення надійності\Захист від механічного спрацювання деталей"""])

#path=Base\Фактор\Покриття\Кадмієве з хроматуванням\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Кадмієве з хроматуванням"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\200"""])

KB[r"""Base\Фактор\Покриття\Кадмієве з хроматуванням"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Покриття\Електрохімічна обробка"""])
#137

KB[r"""Base\Фактор\Покриття\Кадмієве з хроматуванням"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""])

#path=Base\Фактор\Покриття\Корозійностійкі\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Корозійностійкі"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""])

#path=Base\Фактор\Покриття\Мідне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Мідне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\600"""])

KB[r"""Base\Фактор\Покриття\Мідне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується"""])

#path=Base\Фактор\Покриття\Нікелеве\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Нікелеве"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\900"""])

KB[r"""Base\Фактор\Покриття\Нікелеве"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується"""])

#path=Base\Фактор\Покриття\Оксидне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Оксидне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\200"""])

KB[r"""Base\Фактор\Покриття\Оксидне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Залишкові напруження\Стиску"""])

KB[r"""Base\Фактор\Покриття\Оксидне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується"""])

#path=Base\Фактор\Покриття\Оксидне анодізаційне з хроматуванням\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Оксидне анодізаційне з хроматуванням"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\200"""])

#path=Base\Фактор\Покриття\Оксидне з кислих розчинів\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Оксидне з кислих розчинів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\200"""])

#path=Base\Фактор\Покриття\Олов'яне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Олов'яне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\150"""])

KB[r"""Base\Фактор\Покриття\Олов'яне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""])

#path=Base\Фактор\Покриття\Оптимальне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Оптимальне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])
#255
#path=Base\Фактор\Покриття\Пластичне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Пластичне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Покриття\Свинцеве\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Свинцеве"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""])
#345

#path=Base\Фактор\Покриття\Срібне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Срібне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\600"""])

KB[r"""Base\Фактор\Покриття\Срібне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""])

#path=Base\Фактор\Покриття\Травлення під час нанесення покриттів\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Травлення під час нанесення покриттів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Насичення атомарним воднем"""])
#137
#path=Base\Фактор\Покриття\Фосфатне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Фосфатне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\200"""])

KB[r"""Base\Фактор\Покриття\Фосфатне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Покриття\Травлення під час нанесення покриттів"""])
#137
#path=Base\Фактор\Покриття\Цинкове\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Цинкове"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\200"""])

KB[r"""Base\Фактор\Покриття\Цинкове"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Покриття\Електрохімічна обробка"""])
#137

KB[r"""Base\Фактор\Покриття\Цинкове"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується"""])

#path=Base\Фактор\Покриття\Цинкове з хроматуванням\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Покриття\Цинкове з хроматуванням"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Максимальна\300"""])

#path=Base\Фактор\Пошкодження\Від високошвидкісного навантаження\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Від високошвидкісного навантаження"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Втомна тріщина\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна"""])

KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Втомна тріщина\В останньому витку муфти\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\В останньому витку муфти"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

#path=Base\Фактор\Пошкодження\Втомна тріщина\В першому витку ніпеля\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\В першому витку ніпеля"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

#path=Base\Фактор\Пошкодження\Втомна тріщина\Під головкою болта\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Втомна тріщина\Під головкою болта"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

#path=Base\Фактор\Пошкодження\Заїдання\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Заїдання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Кручення"""])

KB[r"""Base\Фактор\Пошкодження\Заїдання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

KB[r"""Base\Фактор\Пошкодження\Заїдання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Велике"""])

KB[r"""Base\Фактор\Пошкодження\Заїдання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На упорному бурті\Велике"""])

KB[r"""Base\Фактор\Пошкодження\Заїдання"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання\Зменшення"""])

KB[r"""Base\Фактор\Пошкодження\Заїдання"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Залишкова деформація\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки\Зменшення"""])

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Деформація тіла гайки"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""])

#path=Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків\Зменшення"""])

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""])

#path=Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня\Зменшення"""])

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз стержня"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""])

#path=Base\Фактор\Пошкодження\Залишкова деформація\Обрив стержня\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Обрив стержня"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""])

#path=Base\Фактор\Пошкодження\Знос\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність\Низька"""])

KB[r"""Base\Фактор\Пошкодження\Знос"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])

KB[r"""Base\Фактор\Пошкодження\Знос"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Знос\Абразивний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Абразивний"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Знос\Адгезійний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Адгезійний"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Знос\Втомний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Втомний"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Знос\Ерозійний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Ерозійний"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Знос\Зменшення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Зменшення"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Знос\Механохімічний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Механохімічний"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Знос\Фретинг-корозійний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Фретинг-корозійний"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Знос\Фретинговий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Знос\Фретинговий"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Пошкодження\Корозійна\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Корозійна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

KB[r"""Base\Фактор\Пошкодження\Корозійна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень"""])

KB[r"""Base\Фактор\Пошкодження\Корозійна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Пошкодження\Корозійна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність\Низька"""])

KB[r"""Base\Фактор\Пошкодження\Корозійна"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\Низька"""])

KB[r"""Base\Фактор\Пошкодження\Корозійна"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Корозійна\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна"""])

#path=Base\Фактор\Пошкодження\Корозійне розтріскування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""])

KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам"""])

KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Крихкий злам\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Крихкий злам"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам"""])

#path=Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

#path=Base\Фактор\Пошкодження\Розгерметизація\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Розгерметизація"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Розгерметизація\Запобігання\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Розгерметизація\Запобігання"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Розгерметизація"""])

#path=Base\Фактор\Пошкодження\Самовідгвинчування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація\Зріз витків"""])

KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Пошкодження"""])

#path=Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

#path=Base\Фактор\Пошкодження при транспортуванні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Пошкодження при транспортуванні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень"""])

KB[r"""Base\Фактор\Пошкодження при транспортуванні"""].__dict__["Not"].add(KB[r"""Base\Фактор\Пошкодження при транспортуванні\Зменшення"""])

#path=Base\Фактор\Розкриття стику\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Розкриття стику"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Розкриття стику"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність\Низька"""])

#path=Base\Фактор\Рухомість з'єднання\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Рухомість з'єднання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

KB[r"""Base\Фактор\Рухомість з'єднання"""].__dict__["Not"].add(KB[r"""Base\Фактор\Рухомість з'єднання\Низька"""])

#path=Base\Фактор\Середовище\Інгібіторний захист\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Середовище\Інгібіторний захист"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна\Низька"""])

#path=Base\Фактор\Середовище\Корозійне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Середовище\Корозійне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Середовище\Корозійне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійна"""])

KB[r"""Base\Фактор\Середовище\Корозійне"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Корозійне розтріскування"""])

KB[r"""Base\Фактор\Середовище\Корозійне"""].__dict__["Not"].add(KB[r"""Base\Фактор\Середовище\Корозійне\Захист"""])

#path=Base\Фактор\Складання\Згвинчування в нагрітому стані\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Згвинчування в нагрітому стані"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Посадка\З натягом"""])

#path=Base\Фактор\Складання\Контргайка затянута великим моментом\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Контргайка затянута великим моментом"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Складання\Контроль затягування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Контроль затягування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Складання\Момент згвинчування\Оптимальний"""])

#path=Base\Фактор\Складання\Контроль затягування\Контроль за видовженням болта\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Контроль затягування\Контроль за видовженням болта"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Складання\Контроль затягування"""])

#path=Base\Фактор\Складання\Контроль затягування\Контроль за кутом повороту\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Контроль затягування\Контроль за кутом повороту"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Складання\Контроль затягування"""])

#path=Base\Фактор\Складання\Контроль затягування\Контроль за моментом згвинчування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Контроль затягування\Контроль за моментом згвинчування"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Складання\Контроль затягування"""])

#path=Base\Фактор\Складання\Момент згвинчування\Неоптимальний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Втомна тріщина"""])

#path=Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Герметичність"""])

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Залишкова деформація"""])

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""].__dict__["Not"].add(KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Малий"""])

#path=Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Малий\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Малий"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування"""])

#path=Base\Фактор\Складання\Момент згвинчування\Оптимальний\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Момент згвинчування\Оптимальний"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])

KB[r"""Base\Фактор\Складання\Момент згвинчування\Оптимальний"""].__dict__["Not"].add(KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний"""])

#path=Base\Фактор\Складання\Очищення різьби\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Очищення різьби"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Згвинчуваність\Добра"""])

KB[r"""Base\Фактор\Складання\Очищення різьби"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""])

#path=Base\Фактор\Складання\Попереднє пластичне деформування перших витків\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Попереднє пластичне деформування перших витків"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень\Нерівномірне навантаження по виткам різьби\Низьке"""])

#path=Base\Фактор\Складання\Селекційне складання\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Селекційне складання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Посадка\З зазором\Зменшення діаметральних зазорів"""])

#path=Base\Фактор\Складання\Тертя при згвинчуванні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Тертя при згвинчуванні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Складання\Момент згвинчування\Неоптимальний\Великий"""])

#path=Base\Фактор\Складання\Уникнення перекосів\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Уникнення перекосів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск форми\Перекос осей\Малий"""])

#path=Base\Фактор\Складання\Фіксація болта при згвинчуванні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Фіксація болта при згвинчуванні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Напруження\Кручення\Зменшення"""])
r"""Base\Джерело\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения\И.А.Биргер, Г.Б.Иосилевич. Резьбовые и фланцевые соединения.djvu#21"""
#path=Base\Фактор\Складання\Часте згвинчування розгвинчування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Складання\Часте згвинчування розгвинчування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Знос"""])

#path=Base\Фактор\Стопоріння\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Стопоріння"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Самовідгвинчування\Зменшення"""])

#path=Base\Фактор\Стопоріння\Жорстке\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Стопоріння\Жорстке"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Стопоріння"""])

#path=Base\Фактор\Стопоріння\Клеєм\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Стопоріння\Клеєм"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Стопоріння"""])

#path=Base\Фактор\Стопоріння\Фрикційне\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Стопоріння\Фрикційне"""].__dict__["SubClassOf"].add(KB[r"""Base\Фактор\Стопоріння"""])

#path=Base\Фактор\Температура\Робоча температура\Висока\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Повзучість"""])

KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Навантаження\Температурне"""])

KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Чутливість до концентрації напружень"""])

KB[r"""Base\Фактор\Температура\Робоча температура\Висока"""].__dict__["Not"].add(KB[r"""Base\Фактор\Температура\Робоча температура\Низька"""])

#path=Base\Фактор\Температура\Робоча температура\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Температура\Робоча температура\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Холодноламкість"""])

KB[r"""Base\Фактор\Температура\Робоча температура\Низька"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Матеріал\Пластичність\Низька"""])
#171
#path=Base\Фактор\Температура\Температура за залишкових напруженнях стиску\Висока\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Температура\Температура за залишкових напруженнях стиску\Висока"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Низька"""])

#path=Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Збільшується"""].__dict__["Not"].add(KB[r"""Base\Фактор\Тертя\Зміна коефіцієнта тертя під час повторних згвинчуваннях\Зменшується"""])

#path=Base\Фактор\Тертя\На різьбі\Велике\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Тертя\На різьбі\Велике"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Тертя\На різьбі\Велике"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Згвинчуваність\Погана"""])

KB[r"""Base\Фактор\Тертя\На різьбі\Велике"""].__dict__["Not"].add(KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""])

#path=Base\Фактор\Тертя\На різьбі\Мале\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Тертя\На різьбі\Мале"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Згвинчуваність\Добра"""])

#path=Base\Фактор\Тертя\На упорному бурті\Велике\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Тертя\На упорному бурті\Велике"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Заїдання"""])

KB[r"""Base\Фактор\Тертя\На упорному бурті\Велике"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Згвинчуваність\Погана"""])

KB[r"""Base\Фактор\Тертя\На упорному бурті\Велике"""].__dict__["Not"].add(KB[r"""Base\Фактор\Тертя\На упорному бурті\Мале"""])

#path=Base\Фактор\Тертя\На упорному бурті\Мале\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Тертя\На упорному бурті\Мале"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Згвинчуваність\Добра"""])

#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке"""])

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Залишкові напруження\Стиску"""])

#path=Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента\Низька\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента\Низька"""].__dict__["Not"].add(KB[r"""Base\Фактор\Технологія\Метод виготовлення\Накатування\Стійкість інструмента"""])

#path=Base\Фактор\Технологія\Метод виготовлення\Обкатування після нарізання\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Обкатування після нарізання"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Залишкові напруження\Стиску"""])
#237
#path=Base\Фактор\Технологія\Метод виготовлення\Піскоструминна обробка\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Піскоструминна обробка"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке"""])

#path=Base\Фактор\Технологія\Метод виготовлення\Полірування\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Метод виготовлення\Полірування"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування\Низьке"""])

#path=Base\Фактор\Технологія\Попередній статичний розтяг високоміцних болтів\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Попередній статичний розтяг високоміцних болтів"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За циклічного навантаження\Висока"""])
#238
#path=Base\Фактор\Технологія\Режими обробки\Оптимальні\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Режими обробки\Оптимальні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Залишкові напруження\Стиску"""])

KB[r"""Base\Фактор\Технологія\Режими обробки\Оптимальні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Геометричні параметри\Допуск розміру\Малий"""])

KB[r"""Base\Фактор\Технологія\Режими обробки\Оптимальні"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність"""])

#path=Base\Фактор\Технологія\Технологічні дефекти\prop.pykb
#open=0
#fg=red
#bg=white

KB[r"""Base\Фактор\Технологія\Технологічні дефекти"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Міцність\За статичного навантаження\Низька"""])

KB[r"""Base\Фактор\Технологія\Технологічні дефекти"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Пошкодження\Крихкий злам\Уповільнене крихке руйнування"""])

KB[r"""Base\Фактор\Технологія\Технологічні дефекти"""].__dict__["isCause"].add(KB[r"""Base\Фактор\Концентрація напружень"""])


#path=Reasoner\class.pykb
#open=1
#fg=darkgreen
#bg=white

# правила виведення 

def allFactsSet(showTransitive=True):
    '''Повертає множину всіх фактів (аксіом) бази знань.
    Факти у вигляді кортежу (суб'єкт, предикат, об'єкт)'''
    factsSet=set() # множина фактів
    for k in KB.values(): # для усіх концептів
        if k.__class__.__name__==r"""Base\Фактор""": # якщо це фактор
            for p in k.__dict__: # для усіх атрибутів
                if k.__dict__[p].__class__.__name__=='Property': # якщо атрибут властивість
                    for obj in k.__dict__[p].get(showTransitive): # для усіх значень властивості
                        factsSet.add((k,p,obj)) # добавити факт в множину фактів
    return factsSet


for k,v in KB.iteritems():
    v.name=k # для всіх об'єктів в KB задає атрибут name і присвоює йому значення ключа в KB
    v.codes={} # властивість codes - словник вихідних кодів
    if v.__class__.__name__=='type': # якщо це клас
        v.__name__=k # для всіх класів в KB присвоює __name__ значення ключа в KB


assertedFacts=allFactsSet(False) # введені факти
print len(assertedFacts)
import csv
writer = csv.writer(open("assertedFacts.csv", "wb"),delimiter = ';') # відкрити csv файл
for x in assertedFacts:
    writer.writerow([x[0].name,x[1],x[2].name]) # записати в файл csv


while True: # цикл для застосування правил
    beforeFacts=allFactsSet() # кількість фактів до
    print str(len(beforeFacts))+' facts. Iteration for apply rules...'

    # логічне виведення для інверсних і симетричних властивостей
    for k in KB.values(): # для усіх концептів
        for p,pv in k.__dict__.iteritems(): # для усіх атрибутів
            if pv.__class__.__name__=='Property': # якщо атрибут властивість
                for obj in pv.get(True): # для усіх значень властивості
                    
                    if pv.inverseName!='': # якщо є інверсна властивість
                        # добавити його в інверсну властивість об'єкта
                        obj.__dict__[pv.inverseName].add(pv.subj)
                            
                    if pv.symmetric: # якщо властивість симетрична
                        # добавити його в аналогічну властивість об'єкта
                        obj.__dict__[pv.name].add(pv.subj)

                        
    # правила виведення:
    # SubClassOf(?x, ?y) & isCause(?y, ?p) -> isCause(?x, ?p)
    # SubClassOf(?x, ?y) & isEffect(?y, ?p) -> isEffect(?x, ?p)
    for k in KB.values(): # для усіх концептів
        if k.__class__.__name__==r"""Base\Фактор""": # якщо це фактор
            for bk in k.SubClassOf.get(True): # для усіх базових концептів (класів)
                for x in bk.isCause.get(True):
                    k.isCause.add(x)
                for x in bk.isEffect.get(True):
                    k.isEffect.add(x)
                    
    # правила виведення:
    # Not(?x, ?nx) & isCause(?nx, ?ny) & Not(?y, ?ny) -> isCause(?x, ?y) 
    # Not(?x, ?nx) & isEffect(?nx, ?ny) & Not(?y, ?ny) -> isEffect(?x, ?y) 
    for k in KB.values(): # для усіх концептів
        if k.__class__.__name__==r"""Base\Фактор""": # якщо це фактор
            for nk in k.Not.get(): # для усіх заперечень концепту
                for e in nk.isCause.get(True): # для усіх наслідків заперечення
                    for ne in e.Not.get(): # для усіх заперечень наслідків заперечення
                        k.isCause.add(ne) # концепт є їх причиною
                for e in nk.isEffect.get(True): # для усіх причин заперечення
                    for ne in e.Not.get(): # для усіх заперечень причин заперечення
                        k.isEffect.add(ne) # концепт є їх наслідком    

    afterFacts=allFactsSet() # кількість фактів після
    # перервати цикл, якщо кількість фактів до і після застосування правил рівна
    if beforeFacts==afterFacts: break


allFacts=allFactsSet()  # усі факти               
print len(allFacts) 
import csv
writer = csv.writer(open("allFacts.csv", "wb"),delimiter = ';') # відкрити csv файл
for x in allFacts:
    writer.writerow([x[0].name,x[1],x[2].name]) # записати в файл csv


# для усіх значень KB присвоює властивості codes текст вихідного коду  
for k in KB: # для усіх ключів у KB
    if k.startswith("Base\\"):
        for fl in os.listdir(k): # для усіх файлів в каталозі
            path = os.path.join(k, fl) # повний шлях
            if os.path.splitext(path)[1]=='.pykb': # якщо файл '.pykb'
                f=open(path,'r') # відкрити
                s=f.read() # читати
                KB[k].codes[fl]=s # присвоїти текст вихідного коду
                f.close() # закрити


#path=Query\class.pykb
#open=1
#fg=brown
#bg=white

# блок запитів до бази знань
# будуть виконуватись ті запити для яких задано #fg=brown

#path=Query\GenerateHTML.pykb
#open=0
#fg=brown
#bg=white

import sys
sys.path.append(programDir)
import MakeCode

for k in KB: # для усіх ключів у KB
    if k.startswith(r"""Base\Модель"""):
        for pykbFile in KB[k].codes: # для кожного pykb файлу в каталозі k
            MakeCode.genHTML(k+'\\'+pykbFile) # генерувати HTML код   

