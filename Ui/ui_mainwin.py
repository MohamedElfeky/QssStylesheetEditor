# -*- coding: utf-8 -*-   
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from .editor import CodeEditor
from .preview import previewWidget
from .flow_layout import QFlowLayout

class Widgets_MainWin(object):
    def setupUi(self, mainwin):
        self.win = mainwin
        self.win.resize(1200, 600)
        self.menubar = mainwin.menuBar()
        self.statusbar = mainwin.statusBar()
        self.mainWidget = QTabWidget()
        self.editor=CodeEditor()

        self.actions = {}
        self.menus = {}
        self.contexMenus = {}
        self.toolbars = {}
        self.status = {}
        self.docks = {}
        self.documents = {}

        self.createActions()
        self.createMenubar()
        self.createContexMenus()
        self.createToolbars()
        self.createStatusBar()
        self.createDocks()
        self.createMainWidget()

    def createActions(self):
        def createAct(text, tip=None, shortcut=None, iconimg=None, checkable=False, slot=None):
            action = QAction(self.tr(text), self)
            if iconimg is not None:
                action.setIcon(QIcon(iconimg))
            if shortcut is not None:
                action.setShortcut(shortcut)
            if tip is not None:
                tip=self.tr(tip)
                action.setToolTip(tip)
                action.setStatusTip(tip)
            if checkable:
                action.setCheckable(True)
            if slot is not None:
                action.triggered.connect(slot)
            return action

        self.actions["new"] = createAct("&New","new",QKeySequence.New,'img/NewDocument.png')
        self.actions["open"] = createAct("&Open","Open",QKeySequence.Open,'img/openHS.png')
        self.actions["save"] = createAct("&Save","Save",QKeySequence.Save,'img/save.png')
        self.actions["saveas"] = createAct("&Save as...","Save as",QKeySequence.SaveAs,'img/saveas.png')
        self.actions["export"] = createAct("&ExportQss","ExportQss","Ctrl+Alt+E",'img/export5.png')
        self.actions["exit"] = createAct("&Exit","Exit","Ctrl+Q",'img/close.png')
        self.actions["undo"] = createAct("&Undo","Undo",QKeySequence.Undo,'img/undo.png')
        self.actions["redo"] = createAct("&Redo","Redo",QKeySequence.Redo,'img/redo.png')
        self.actions["cut"] = createAct("&Cut","Cut",QKeySequence.Cut,'img/cut.png')
        self.actions["copy"] = createAct("&Copy","Copy",QKeySequence.Copy,'img/copy.png')
        self.actions["paste"] = createAct("&Paste","Paste",QKeySequence.Paste,'img/paste.png')

        # self.fontcolorAct=QAction(QIcon("img/broadcast_send_fontcolor_normal.bmp"),"&FontColor",self)
        # self.fontcolorAct.setShortcut("Ctr+Shit+C")
        # self.fontcolorAct.setStatusTip("FontColor")
        self.actions["DisableQss"] = createAct("&DisableQss","DisableQss",checkable=True)
        self.actions["DisableQss"].setChecked(False)
        self.actions["ShowColor"] = createAct("&ColorPanel","ShowColorPanel",None,"img/color.png",checkable=True)
        self.actions["ShowColor"].setChecked(True)
        self.actions["ShowPreview"] = createAct("&PreviewPanel","ShowPreviewPanel",None,"img/view.png",checkable=True)
        self.actions["ShowPreview"].setChecked(True)

        self.actions["about"] = createAct("&About","About")

        # self.exitAct.triggered.connect(qApp.exit)#等价于qApp.quit
        self.actions["exit"].triggered.connect(self.close)

    def createMenubar(self):
        self.menus["File"] = QMenu("&File")
        self.menus["Edit"] = QMenu("&Edit")
        self.menus["View"] = QMenu("&View")

        self.menus["File"].addMenu(self.menus["View"])
        self.menus["File"].addAction(self.actions["new"])
        self.menus["File"].addAction(self.actions["open"])
        self.menus["File"].addAction(self.actions["save"])
        self.menus["File"].addAction(self.actions["saveas"])
        self.menus["File"].addAction(self.actions["export"])
        self.menus["File"].addSeparator()
        self.menus["File"].addAction(self.actions["exit"])

        # editMenu=self.menus["Edit"].addMenu("TextEdit")
        editMenu = QMenu("Text", self.menus["Edit"])
        editMenu.addAction(self.actions["undo"])
        editMenu.addAction(self.actions["redo"])
        editMenu.addSeparator()
        editMenu.addAction(self.actions["cut"])
        editMenu.addAction(self.actions["copy"])
        editMenu.addAction(self.actions["paste"])
        self.menus["Edit"].addMenu(editMenu)

        self.menus["View"] = QMenu("&View")
        self.menus["View"].addAction(self.actions["ShowColor"])
        self.menus["View"].addAction(self.actions["ShowPreview"])

        self.menus["Help"] = QMenu("&Help")
        self.menus["Help"].addAction(self.actions["about"])

        for m in self.menus.values():
            self.menubar.addMenu(m)

    def createContexMenus(self):
        self.contexMenus["Edit"] = QMenu("Edit")
        self.contexMenus["Edit"].addAction(self.actions["cut"])
        self.contexMenus["Edit"].addAction(self.actions["copy"])
        self.contexMenus["Edit"].addAction(self.actions["paste"])

    def createToolbars(self):
        checkbox = QCheckBox("DisableQSS")
        self.themeCombo = QComboBox()
        self.themeCombo.addItems(QStyleFactory.keys())
        theme = QApplication.style().objectName()
        self.themeCombo.setCurrentIndex(self.themeCombo.findText(theme, Qt.MatchFixedString))
        #self.themeCombo.setEnabled(False)
        #themeCombo.activated[str].connect(qApp.setStyle)
        # themeCombo.currentTextChanged.connect(qApp.setStyle)
        #checkbox.stateChanged.connect(self.themeCombo.setEnabled)
        checkbox.stateChanged.connect(self.actions["DisableQss"].setChecked)
        #checkbox.stateChanged.connect(lambda x:self.actions["DisableQss"].setChecked(checkbox.isChecked()))

        self.toolbars["main"] = QToolBar("main")
        self.toolbars["main"].addWidget(checkbox)
        self.toolbars["main"].addWidget(self.themeCombo)
        
        self.toolbars["file"]=QToolBar("file")
        self.toolbars["file"].addAction(self.actions["new"])
        self.toolbars["file"].addAction(self.actions["open"])
        self.toolbars["file"].addAction(self.actions["save"])
        # self.toolbars["file"].addAction(self.actions["saveas"])
        self.toolbars["file"].addAction(self.actions["export"])

        self.toolbars["Edit"] = QToolBar("Edit")
        self.toolbars["Edit"].addAction(self.actions["undo"])
        self.toolbars["Edit"].addAction(self.actions["redo"])
        self.toolbars["Edit"].addSeparator()
        self.toolbars["Edit"].addAction(self.actions["cut"])
        self.toolbars["Edit"].addAction(self.actions["copy"])
        self.toolbars["Edit"].addAction(self.actions["paste"])

        self.toolbars["View"] = QToolBar("View")
        self.toolbars["View"].addAction(self.actions["ShowColor"])
        self.toolbars["View"].addAction(self.actions["ShowPreview"])

        for t in self.toolbars.values():
            self.win.addToolBar(t)

    def createStatusBar(self):
        self.status["date"] = QLabel()
        self.statusbar.showMessage("Ready")
        # self.statusbar.addWidget(QWidget(),1)
        self.statusbar.addPermanentWidget(self.status["date"])
        self.status["date"].setText(QDate.currentDate().toString())

    def createDocks(self):
        self.docks["color"] = QDockWidget("Colors")
        self.docks["preview"] = QDockWidget("Preview")

        self.docks["color"].setMinimumSize(QSize(120, 20))
        self.docks["color"].setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.docks["preview"].setMinimumSize(QSize(200, 200))
        self.docks["preview"].setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        self.win.addDockWidget(Qt.LeftDockWidgetArea, self.docks["color"])
        self.win.addDockWidget(Qt.RightDockWidgetArea, self.docks["preview"])

        class ColorPanelWidget(QWidget):
            def __init__(self):
                super().__init__()
            def sizeHint(self):
                return self.layout().sizeHint()
        colorPanelWidget = ColorPanelWidget()
        self.colorPanelLayout = QFlowLayout()
        colorPanelWidget.setLayout(self.colorPanelLayout)
        self.docks["color"].setWidget(colorPanelWidget)
        self.docks["preview"].setWidget(previewWidget())
        
        self.docks["color"].visibilityChanged.connect(self.actions["ShowColor"].setChecked)

    def createMainWidget(self):
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setTabBarAutoHide(True)
        self.mainWidget.addTab(self.editor, "main")