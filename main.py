import sys
import os
import json

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QTabBar,
                             QFrame, QStackedLayout)
from PyQt5.QtGui import QIcon, QWindow, QImage
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


class AddressBar(QLineEdit):
	def __init__(self):
		super().__init__()
	
	def mousePressEvent(self, e):
		self.selectAll()


class App(QFrame):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Web Browser")
		self.setGeometry(0, 0, 1024, 768)
		# self.setBaseSize(1366, 768)
		self.CreateApp()
	
	def CreateApp(self):
		self.layout = QVBoxLayout()
		self.layout.setSpacing(0)
		self.setContentsMargins(0, 0, 0, 0)
		# Create Tabs
		self.tabbar = QTabBar(movable=True, tabsClosable=True)
		self.tabbar.tabCloseRequested.connect(self.CloseTab)
		self.tabbar.tabBarClicked.connect(self.SwitchTab)
		self.tabbar.setCurrentIndex(0)
		
		# Keep track of tabs
		self.tabCount = 0
		self.tabs = []
		
		# Create AddressBar
		self.Toolbar = QWidget()
		self.ToolbarLayout = QHBoxLayout()
		self.addressbar = AddressBar()
		
		self.addressbar.returnPressed.connect(self.BrowseTo)
		
		self.Toolbar.setLayout(self.ToolbarLayout)
		self.ToolbarLayout.addWidget(self.addressbar)
		
		# New tab button
		self.AddTabButton = QPushButton("+")
		self.AddTabButton.clicked.connect(self.AddTab)
		
		self.ToolbarLayout.addWidget(self.AddTabButton)
		# set main view
		self.container = QWidget()
		self.container.layout = QStackedLayout()
		self.container.setLayout(self.container.layout)
		
		self.layout.addWidget(self.tabbar)
		self.layout.addWidget(self.Toolbar)
		self.layout.addWidget(self.container)
		self.setLayout(self.layout)
		self.AddTab()
		
		self.show()
	
	def CloseTab(self, i):
		self.tabbar.removeTab(i)
	
	def AddTab(self):
		i = self.tabCount
		
		self.tabs.append(QWidget())
		self.tabs[i].layout = QVBoxLayout()
		self.tabs[i].setObjectName("tab" + str(i))
		
		# Open webview
		self.tabs[i].content = QWebEngineView()
		self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))
		
		# Add webview to tabs layout
		self.tabs[i].layout.addWidget(self.tabs[i].content)
		
		# set top level tab from [] to layout
		self.tabs[i].setLayout(self.tabs[i].layout)
		
		# Add tab to top level stackedwidget
		self.container.layout.addWidget(self.tabs[i])
		self.container.layout.setCurrentWidget(self.tabs[i])
		
		# Set the tab at the top of the screen
		self.tabbar.addTab("New Tab")
		self.tabbar.setTabData(i, "tab" + str(i))
		self.tabbar.setCurrentIndex(i)
		
		self.tabCount += 1
		
	def SwitchTab(self, i):
		tab_data = self.tabbar.tabData(i)
		# print("tab:", tab_data)
		
		tab_content = self.findChild(QWidget, tab_data)
		self.container.layout.setCurrentWidget(tab_content)

	def BrowseTo(self):
		text = self.addressbar.text()
		
		i = self.tabbar.currentIndex()
		tab = self.tabbar.tabData(i)
		wv = self.findChild(QWidget, tab).content
		
		if "http" not in text:
			if "." not in text:
				url = "https://www.google.com/#q=" + text
			else:
				url = "http://" + text
		else:
			url = text
		
		wv.load(QUrl.fromUserInput(url))
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = App()
	sys.exit(app.exec_())
