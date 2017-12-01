
'''
Genclass
'''

from PyQt5.QtWidgets import (qApp,
                             QApplication,QWidget,
                             QMessageBox, QFileDialog,
                             QPushButton,
                             QTableView,QTableWidget,QTableWidgetItem,
                             QSizePolicy, QHeaderView,
                             QComboBox, QCheckBox, QLineEdit,
                             QMainWindow,QDesktopWidget,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import (Qt, pyqtSignal, QEvent)
from PyQt5.QtGui import QIcon
# from TableWidgetDragRows import TableWidgetDragRows # dysfunct

import sys
import yaml

import yml
import gui
from Struct import Struct
import Generators
from generators import *

Generators.Generators._load([Monguo,WtForm,ReactComponent,ReactList,TorgHandler])
icon = "./icon.png"
KnownDefinitions = yml.load("templates.yaml")

classTables = []
dictTables = []
types = None
typeTable = None
DefaultGenerator = Generators.Generators(KnownDefinitions)
DefaultGenerator.dir = '../torg/api/'


class Table(QTableWidget):
    Change = pyqtSignal(QTableWidgetItem)
    Add = pyqtSignal(QTableWidgetItem)
    Del = pyqtSignal(QTableWidgetItem)

    def __init__(_,parent):
        super().__init__(parent)
        _.center()

    def center(_):
        qr = _.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        _.move(qr.topLeft())


class TypesTable(Table):

    def __init__(_, types=[], name=None, generators=DefaultGenerator, parent=None):
        super().__init__(parent)
        _.name = name
        _.setColumnCount(1)
        _.setRowCount(len(types))
        _.setColumnWidth(0,200)
        _.adjustSize()
        #_.setBaseSize(500,200)
        _.load(types)
        #_.itemChanged.connect(_.TyChange.emit)

    def load(_,types):
        _.clear()
        _.setRowCount(len(types))

        for x in range(len(types)):
            if types[x] in _.names():
                #print(types[x],'already in')
                pass
            else:
                it = QTableWidgetItem()
                it.setText(types[x])
                _.setItem(x,0,it)

    def types(_):
        for x in range(_.rowCount()):
            yield _.item(x,0)

    def names(_) :
        return [i.text() if i else '' for i in _.types()]

    def getItemNamed(_,n):
        i = _.names().index(n)
        #print("get item named",n,i)

        return _.item(i,0)

    def newType(_,s=''):
        if s in _.names():
            #print('already in', s)
            i = _.names().index(s)
            return _.itemAt(i,0)
        else:
            lt = _.rowCount()
            it = QTableWidgetItem()
            it.setText(s)
            _.setRowCount(lt+1)
            _.setItem(lt,0,it)
            _.Add.emit(it)
            return it


    def addType(_):
        '''
        add a new empty item and broadcast it.
        when the name is set the chgtype event is triggered
        '''
        if '' not in _.names():
            lt = _.rowCount()
            _.setRowCount(lt+1)
            it = QTableWidgetItem()
            _.setItem(lt,0,it)
            _.editItem(it)
            _.Add.emit(it)


    def clearType(_):
        i = _.currentRow()
        if i > -1:
            it = _.takeItem(i,0)
            if it:
                _.Del.emit(it)

    def delType(_):
        i = _.currentRow()
        if i > -1:
            it = _.takeItem(i,0)
            if it:
                _.removeRow(i)
                _.Del.emit(it)

    def keyPressEvent(_,event) :

        if _.state() != QTableView.EditingState:
            if event.key() == Qt.Key_Backspace:
                _.delType()

            if event.key() == Qt.Key_Delete:
                _.clearType()

            elif event.key() == Qt.Key_Return:
                _.addType()

            elif event.key() == Qt.Key_Space:
                _.load(['0','1','2'])


        else :
            super().keyPressEvent(event)


    def generate(_):
        return "%s: %s" % (_.name,"[%s]" % ",".join(_.names()))


    def save(_):
        return {
            'name':_.name,
            'names':_.names(),
        }


class DictTable(Table):

    def __init__(_, D, name=None, parent=None):
        super().__init__(parent)
        _.name = name
        _.dict = D
        _.setColumnCount(2)
        _.setRowCount(len(D))
        #_.setColumnWidth(0,200)
        i = 0
        for k,v in D.items():
            ik = QTableWidgetItem(k)
            iv = QTableWidgetItem(str(v))
            _.setItem(i,0,ik)
            _.setItem(i,1,iv)
            i += 1

        #_.itemChanged.connect(_.TyChange.emit)

    def name(_):
        for x in range(_.rowCount()): yield _.item(x,0)

    def value(_):
        for x in range(_.rowCount()): yield _.item(x,1)

    def names(_) :
        return [i.text() if i else '' for i in _.name()]

    def values(_) :
        return [i.text() if i else '' for i in _.value()]


    def add(_):
        if '' not in _.names():
            lt = _.rowCount()
            _.setRowCount(lt+1)
            it = QTableWidgetItem()
            _.setItem(lt,0,it)
            _.editItem(it)
            _.Add.emit(it)

    def rm(_):
        i = _.currentRow()
        if i > -1:
            it = _.takeItem(i,0)
            if it:
                _.Del.emit(it)

    def keyPressEvent(_,event) :

        if _.state() != QTableView.EditingState:
            if event.key() == Qt.Key_Backspace: _.rm()
            elif event.key() == Qt.Key_Return: _.add()
        else :
            super().keyPressEvent(event)

    def save(_):
        yaml.dump(_.dict)

    def generate(_) :
        return yaml.dump(_.dict)



class MembersTable(Table):

    def __init__(_, types, members, parent=None):
        super().__init__(parent)
        _.setColumnCount(4)
        _.setRowCount(len(members))
        _.setHorizontalHeaderLabels(['name','type','R','L'])

        for i in range(_.rowCount()):
            it = QTableWidgetItem(members[i][0])
            _.setItem(i,0,it)

            combo = QComboBox()
            combo.addItems(types.names())
            #print(types.names())
            idx = types.names().index(members[i][1][0])
            combo.setCurrentIndex(idx)
            _.setCellWidget(i,1,combo)

            cb = QCheckBox()
            cb.setTristate(True)
            cb.setCheckState(members[i][1][1])
            _.setCellWidget(i,2,cb)
            cb = QCheckBox()
            cb.setTristate(True)

            if len(members[i][1]) == 2:
                members[i][1].append(0)
            cb.setCheckState(members[i][1][2])
            _.setCellWidget(i,3,cb)

        _.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def rowcount(_):
        return range(_.rowCount())

    def combo(_,x):
        return _.cellWidget(x,1)

    def combos(_):
        for x in _.rowcount(): yield _.combo(x)

    def members(_) :
        for x in _.rowcount(): yield _.name(x)

    def name(_,x):
        return _.item(x,0).text()

    def cb(_,x):
        return _.cellWidget(x,2)

    def cb2(_,x):
        return _.cellWidget(x,3)

    def dict(_) :
        return [
            {
                _.name(x): [
                    _.combo(x).currentText(),
                    int(_.cb(x).checkState()),
                    int(_.cb2(x).checkState())
                ]
            } for x in range(_.rowCount())]

    def names(_) :
        return [ i if i else '' for i in _.members()]

    def fields(_) :
        ''' return '''
        return [
            ( _.item(x,0).text(),
              _.combo(x).currentText(),
              _.cb(x).checkState(),
              _.cb2(x).checkState()
              )
            for x in range(_.rowCount())
        ]


    def addTy(_,tableitem):
        '''
        update the types. new combos
        if the set type still exist in the new list, keep it
        '''
        [co.addItem("") for co in _.combos() ]
        #[_.combo(x).addItem("undefined") for x in range(_.rowCount()) ]

        '''
        for index in range(_.rowCount()):
            combo = _.cellWidget(index,1)
            combo.addItem("undefined") # or "None" :) ?
        '''

    def chgTy(_,it):
        [co.setItemText(it.row(),it.text()) for co in _.combos() ]
        '''
        update the types. new combos
        if the set type still exist in the new list, keep it
        '''
        '''
        for index in range(_.rowCount()):
            combo = _.cellWidget(index,1)
            combo.addItem("undefined") # or "None" :) ?
        '''

    def setTypesTable(_,types):
        '''
        update the types. new combos
        if the set type still exist in the new list, keep it
        '''
        for x in range(_.rowCount()):
            combo = QComboBox()
            combo.addItems(types)
            v = _.cellWidget(x,1)
            _.setCellWidget(x,1,combo)
            if v in types:
                i = types.index(v)
                _.cellWidget(x,1).setCurrentIndex(i)



    def keyPressEvent(_,event) :

        if _.state() != QTableView.EditingState:
            if event.key() == Qt.Key_Return:
                    if '' not in [n for n in _.names()]:
                        lt = _.rowCount()
                        _.setRowCount(lt+1)
                        it = QTableWidgetItem()
                        _.setItem(lt,0,it)
                        _.editItem(it)
                        _.Add.emit(it)

                        combo = QComboBox()
                        combo.addItems(types.names())
                        _.setCellWidget(lt,1,combo)

                        cb = QCheckBox()
                        cb.setTristate(True)
                        _.setCellWidget(lt,2,cb)
                        cb2 = QCheckBox()
                        cb2.setTristate(True)
                        _.setCellWidget(lt,3,cb2)

            elif event.key() == Qt.Key_Delete:
                    i = _.currentRow()
                    if i > -1:
                        it = _.takeItem(i,0)
                        _.Del.emit(it)

            elif event.key() == Qt.Key_Backspace:
                    i = _.currentRow()
                    if i > -1:
                        it = _.takeItem(i,0)
                        if it:
                            _.Del.emit(it)
                        _.removeRow(i)

            else :
                super().keyPressEvent(event)




class ClassTable(QWidget):
    '''
    remember that types can either be primitive types or come from a ClassTable
    hence a generic TypeName
    don't elucubrate on subset heritance, this is volatile data.
    '''

    boundGenerators = False
    activateLock = False

    def __init__(
            _, typesTable, data=[], name='undefined',
            generators=DefaultGenerator, parent=None):
        '''
        pop out a ClassTable types is Typetable
        '''
        super().__init__(parent)
        #_.setWindowFlags(Qt.Tool)
        _.name = name
        _.generators = generators
        _.typesTable = typeTable

        _.nameWidget = QLineEdit()
        _.nameWidget.setText(name)
        _.nameWidget.textEdited.connect(_.setName)
        _.cat = QCheckBox()
        _.cat.setTristate(True)
        _.generateButton = QPushButton("g")
        _.copyButton = QPushButton("c")

        btnSize = (20,20)
        maxsize = (QSizePolicy.Fixed,QSizePolicy.Fixed)
        _.generateButton.setMaximumSize(*btnSize)
        _.generateButton.setSizePolicy(*maxsize)
        _.copyButton.setMaximumSize(*btnSize)
        _.copyButton.setSizePolicy(*maxsize)
        _.selectGenerator = QComboBox()
        _.selectGenerator.addItems(generators._availables())
        _.selectGenerator.addItem('ALL')
        _.selectGenerator.currentIndexChanged.connect(_.generatorChanged)

        _.generateButton.clicked.connect(_.generate)
        _.copyButton.clicked.connect(_.copy)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        grid = QGridLayout()

        hbox.addWidget(_.nameWidget)
        hbox.addWidget(_.cat)
        hbox.addWidget(_.selectGenerator)
        hbox.addWidget(_.generateButton)
        hbox.addWidget(_.copyButton)

        _.setLayout(grid)
        grid.addLayout(hbox,0,0)
        grid.addLayout(vbox,1,0)

        _.members = MembersTable(types,data)
        typesTable.Add.connect(_.members.addTy)
        typesTable.itemChanged.connect(_.members.chgTy)
        vbox.addWidget(_.members)

        _.typeitem = typesTable.newType()
        _.setName(name)


    def setName(_,s):
        _.name = s

        if s in _.typesTable.table.names():
            it = _.typesTable.table.getItemNamed(s)
            #print(s,'already',it.text())
            _.typeitem = it

        _.typeitem.setText(s)
        _.setWindowTitle(s)

    def generate(_):
        gen = _.selectGenerator
        if gen.currentText() == "ALL" :
            gens = [ gen.itemText(x) for x in range(gen.count())]
            gens.remove('ALL')
            [ _.__generate(g) for g in gens ]
        else :
            _.__generate(gen.currentText())

    def __generate(_,gen):
        G = _.generators._get(gen)
        # add the class list to the generator, so it can differenciate
        # types and primitive types from Objects
        _.generators.classes = [ c.name for c in classTables]
        res = G(_.generators,_) # method is called externally as functor

        print(res)


    def copy(_):
        name = _.name + str(len(classTables))
        if name in types.names():
            QMessageBox.warning(None,'woops','''
There's already a class named %s''' % name,QMessageBox.Ok)

        else:
            m = [list(m.items())[0] for m in _.members.dict()]

            C = ClassTable(
                typesTable=types,
                data=m,
                name=name)
            classTables.append(C)
            C.show()
            C.move(_.x()+_.width(),_.y()+20)


    def save(_):
        return {
            _.name : {
                'position':[ _.x(), _.y()],
                'size' : [_.width(), _.height()],
                'generator': _.selectGenerator.currentIndex(),
                'members':[ x for x in _.members.dict() ]
            }
        }

    def generatorChanged(_,i):
        if ClassTable.boundGenerators :
            [ c.selectGenerator.setCurrentIndex(i) for c in classTables]



class GenTable(QWidget): # superflu

    def __init__(_, table, name='undefined', parent=None):
        super().__init__(parent)
        grid = QGridLayout()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        _.name = name
        _.table = table

        _.nameEdit = QLineEdit()
        _.generateButton = QPushButton("generate")
        _.nameEdit.textEdited.connect(_.setName)
        _.generateButton.clicked.connect(_.generate)

        vbox.addWidget(table)
        hbox.addWidget(_.nameEdit)
        hbox.addWidget(_.generateButton)
        grid.addLayout(hbox,0,0)
        grid.addLayout(vbox,1,0)
        _.setLayout(grid)
        _.nameEdit.setText(name)

        _.setWindowTitle(name)


    def setName(_,s):
        _.name = s
        _.table.name = s

    def generate(_):
        r = _.table.generate()
        return r

    def yml(_):
        return "%s: %s" % (_.name,"[%s]" % ",".join(_.table.names()))


    def save(_):
        T = _.table.save()
        T.update({
            'position':[_.x(),_.y()],
            'size':[_.width(),_.height()]
        })
        return T


class MainWindow(QMainWindow):
    '''
    need an intermediate central widget?
    '''
    def __init__(_):
        super().__init__()
        _.app = app
        _.setWindowTitle('Genclass')
        _.setWindowIcon(QIcon(icon))
        _.forceclose = True
        _.lastsavefile = None
        menubar = _.menuBar()

        Gui = gui.GUI(qApp, _)
        G = dict()
        for k, a in Gui['actions'].items():
            G[k] = gui.buildAction(_, k, *a)

        for menu in Gui['Menus']:
            m = menubar.addMenu(menu[0])
            for entry in menu[1]:
                m.addAction(G[entry])

        _.center()

    def center(_):
        qr = _.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        _.move(qr.topLeft())


    def keyPressEvent(_,event):
        if event.key() == Qt.Key_Escape:
            sys.exit()


    def closeEvent(_, event):
        if not _.forceclose :
            event.accept()
            reply = QMessageBox.question(_, 'Message',
                                            "Are you sure to quit?",
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No )
            if reply == QMessageBox.Yes :
                #_.clean_at_exit()
                return event.accept()
            else: event.ignore()
        else:
            sys.exit()

    def changeEvent(_,event):
        if event.type() == QEvent.ActivationChange:
            if _.isActiveWindow():
                [ c.raise_() for c in classTables ]

    def save(_):
        if not _.lastsavefile:
            _.saveAs()
        else:

            t = yaml.dump({'types':typeTable.save()})
            classes = {'classes':[x.save() for x in classTables]}
            ya = yaml.dump(classes)
            print(ya)
            with open(_.lastsavefile,'w') as file:
                file.write(t)
                file.write(ya)

    def saveAs(_):
        fileName = QFileDialog.getSaveFileName(
            _,"Save File",
            "genclass.yml",
            "yaml (*.yml)")

        if fileName[0]:
            with open(fileName[0],'w') as file:
                file.write(yaml.dump({'types':typeTable.save()}))
                classes = {'classes':[x.save() for x in classTables]}
                ya = yaml.dump(classes)
                print(ya)
                file.write(ya)
                _.lastsavefile = fileName[0]
            print('saved')


    def open(_):
        fileName = QFileDialog.getOpenFileName(
            _,"Save File",
            "genclass.yml",
            "yaml (*.yml)")

        if fileName[0]:
            _.load(fileName[0])

    def load(_,file):
        S = yml.load(file)

        [ x.close() for x in classTables ]
        classTables.clear()

        t = Struct(S.types)
        typeTable.nameEdit.setText(t.name)
        typeTable.setName(t.name)

        typeTable.table.load(t.names)

        typeTable.show()
        typeTable.move(*t.position)
        typeTable.resize(*t.size)

        for x in S.classes:
            k = list(x.keys())[0]
            klass = x[k]
            print('loading %s' % k)

            C = ClassTable(
                typeTable.table,
                [list(m.items())[0] for m in klass['members']],
                k)

            C.selectGenerator.setCurrentIndex(klass['generator'])
            C.show()
            C.move(*klass['position'])
            C.resize(*klass['size'])
            classTables.append(C)

        _.lastsavefile = file


    def newclass(_):
        if '' in types.names():
            QMessageBox.warning(None,'woops','''
There's already a class without a name,
and only one nameless class is allowed at a time.
so set its name first before creating a new one''',QMessageBox.Ok)

        else:
            C = ClassTable(typesTable=types, data=[('a',['int',0])])
            classTables.append(C)
            C.show()
            C.move(_.x()+_.width(),_.y())

    def newdict(_):
        D = DictTable({1:1})
        classTables.append(D)
        D.show()
        D.move(_.x()+_.width(),_.y())


    def bindGenerators(_):
        ClassTable.boundGenerators = not ClassTable.boundGenerators

    def generateAll(_):
        [ c.generate() for c in classTables]
        print('done')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    types = TypesTable(KnownDefinitions.types, 'types')
    typeTable = GenTable(types,'types')
    typeTable.show()

    m = MainWindow()
    m.show()
    m.load('genclass.yml')

    '''
    D = DictTable({'A':1})
    D1 = GenTable(D)
    D1.show()
    D1.move(700,700)
    '''

    app.exec_()

    sys.exit()

