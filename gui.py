from collections import OrderedDict
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QState, QStateMachine
from PyQt5.QtWidgets import QBoxLayout

Icons = './icons/'

win = None

def GUI(qApp,window):
    global win
    win = window
    return {
        'Menus': [
            ['File'     ,[ 'Open','Save','Save As','Exit' ]],
            ['Tables'   ,[ 'New Class', 'New Dict', 'Bind Generators', 'Generate all']],
        ],
        'actions': OrderedDict([
            # key       statusText      shortcut,   icon    func    checkable
            ('Open'            ,['Open file'      ,'Ctrl+o'      , None, window.open     ]),
            ('Save'            ,['Save file'      ,'Ctrl+s'      , None, window.save     ]),
            ('Save As'         ,['Save file'      ,'Ctrl+shift+s', None, window.saveAs   ]),
            ('Exit'            ,['get out'        ,'Ctrl+q'      , None, window.close    ]),
            ('New Class'       ,['new class table', ''           , None, window.newclass ]),
            ('New Dict'        ,['new dict table' , ''           , None, window.newdict  ]),
            ('Bind Generators' ,['bind them'      , ''           , None, window.bindGenerators,True]),
            ('Generate all'    ,['generate'       , ''           , None, window.generateAll ]),
        ]),
    }


def buildAction(
    parent,key,statusText=None,shortcut=None, icon=None,func=None,checkable=False
):
    a = QAction(QIcon(Icons + ('' if icon is None else icon)), '&'+key, parent)
    a.setStatusTip(statusText)
    a.setShortcut(shortcut)
    a.setCheckable(checkable)
    a.triggered.connect(func)
    return a

def twoStateButton(name,stateMachine,action,*states):
    st = QStateMachine()

    a1,a2 = states
    s1,s2 = QState(),QState()
    icon1 = QIcon(Icons + a1[1])
    icon2 = QIcon(Icons + a2[1])
    s1.setObjectName(a1[0])
    s2.setObjectName(a2[0])
    s1.assignProperty(action, "icon", icon1)
    s2.assignProperty(action, "icon", icon2)
    s1.assignProperty(action, "text", a1[0])
    s2.assignProperty(action, "text", a2[0])

    s1.addTransition(action.triggered, s2)
    s2.addTransition(action.triggered, s1)
    st.addState(s1)
    st.addState(s2)
    st.setInitialState(s1)

    stateMachine[name] = st
    st.start()

