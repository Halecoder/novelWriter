# -*- coding: utf-8 -*-
"""novelWriter Config Class

 novelWriter – Config Class
============================
 This class reads and store the main preferences of the application

 File History:
 Created: 2018-09-22 [0.0.1]

"""

import logging
import configparser
import nw

from os           import path, mkdir, getcwd
from appdirs      import user_config_dir
from datetime     import datetime

from nw.constants import nwQuotes

logger = logging.getLogger(__name__)

class Config:

    CNF_STR  = 0
    CNF_INT  = 1
    CNF_BOOL = 2
    CNF_LIST = 3

    def __init__(self):

        # Set Application Variables
        self.appName   = nw.__package__
        self.appHandle = nw.__package__.lower()
        self.showGUI   = True
        self.debugGUI  = False
        self.debugInfo = False

        # Set Paths
        self.confPath  = None
        self.confFile  = None
        self.homePath  = None
        self.appPath   = None
        self.appRoot   = None
        self.guiPath   = None
        self.themeRoot = None
        self.themePath = None

        # Set default values
        self.confChanged  = False

        ## General
        self.guiTheme     = "default_dark"
        self.winGeometry  = [1100, 650]
        self.treeColWidth = [120, 30, 50]
        self.mainPanePos  = [300, 800]
        self.docPanePos   = [400, 400]

        ## Dialogs
        self.dlgTimeLine  = [600, 400]

        ## Project
        self.autoSaveProj = 60
        self.autoSaveDoc  = 30

        ## Text Editor
        self.textFont        = None
        self.textSize        = 12
        self.textFixedW      = True
        self.textWidth       = 600
        self.textMargin      = [40, 40]
        self.tabWidth        = 40
        self.doJustify       = True
        self.autoSelect      = True
        self.doReplace       = True
        self.doReplaceSQuote = True
        self.doReplaceDQuote = True
        self.doReplaceDash   = True
        self.doReplaceDots   = True
        self.styleSQuote     = 1
        self.styleDQuote     = 1
        self.wordCountTimer  = 5.0

        self.fmtDoubleQuotes = ["“","”"]
        self.fmtSingleQuotes = ["‘","’"]
        self.fmtApostrophe   = "’"

        self.spellLanguage   = "en_GB"

        # Path
        self.recentList = [""]*10

        return

    ##
    #  Actions
    ##

    def initConfig(self, confPath=None):

        if confPath is None:
            self.confPath = user_config_dir(self.appHandle)
        else:
            logger.info("Setting config from alternative path: %s" % confPath)
            self.confPath = confPath

        self.confFile  = self.appHandle+".conf"
        self.homePath  = path.expanduser("~")
        self.appPath   = path.dirname(__file__)
        self.appRoot   = path.join(self.appPath,path.pardir)
        self.helpPath  = path.join(self.appRoot,"help","en_GB")
        self.guiPath   = path.join(self.appPath,"gui")
        self.themeRoot = path.join(self.appPath,"themes")
        self.themePath = path.join(self.themeRoot)

        # If config folder does not exist, make it.
        # This assumes that the os config folder itself exists.
        # TODO: This does not work on Windows
        if not path.isdir(self.confPath):
            mkdir(self.confPath)

        # Check if config file exists
        if path.isfile(path.join(self.confPath,self.confFile)):
            # If it exists, load it
            self.loadConfig()
        else:
            # If it does not exist, save a copy of the defaults
            self.saveConfig()

        return True

    def loadConfig(self):

        logger.debug("Loading config file")
        cnfParse = configparser.ConfigParser()
        try:
            cnfParse.read_file(open(path.join(self.confPath,self.confFile)))
        except Exception as e:
            logger.error("Could not load config file")
            return False

        ## Main
        cnfSec = "Main"
        self.guiTheme        = self._parseLine(cnfParse, cnfSec, "theme", self.CNF_STR, self.guiTheme)

        ## Sizes
        cnfSec = "Sizes"
        self.winGeometry     = self._parseLine(cnfParse, cnfSec, "geometry", self.CNF_LIST, self.winGeometry)
        self.treeColWidth    = self._parseLine(cnfParse, cnfSec, "treecols", self.CNF_LIST, self.treeColWidth)
        self.mainPanePos     = self._parseLine(cnfParse, cnfSec, "mainpane", self.CNF_LIST, self.mainPanePos)
        self.docPanePos      = self._parseLine(cnfParse, cnfSec, "docpane",  self.CNF_LIST, self.docPanePos)
        self.dlgTimeLine     = self._parseLine(cnfParse, cnfSec, "timeline", self.CNF_LIST, self.dlgTimeLine)

        ## Project
        cnfSec = "Project"
        self.autoSaveProj    = self._parseLine(cnfParse, cnfSec, "autosaveproject", self.CNF_INT, self.autoSaveProj)
        self.autoSaveDoc     = self._parseLine(cnfParse, cnfSec, "autosavedoc",     self.CNF_INT, self.autoSaveDoc)

        ## Editor
        cnfSec = "Editor"
        self.textFont        = self._parseLine(cnfParse, cnfSec, "textfont",    self.CNF_STR,  self.textFont)
        self.textSize        = self._parseLine(cnfParse, cnfSec, "textsize",    self.CNF_INT,  self.textSize)
        self.textFixedW      = self._parseLine(cnfParse, cnfSec, "fixedwidth",  self.CNF_BOOL, self.textFixedW)
        self.textWidth       = self._parseLine(cnfParse, cnfSec, "width",       self.CNF_INT,  self.textWidth)
        self.textMargin      = self._parseLine(cnfParse, cnfSec, "margins",     self.CNF_LIST, self.textMargin)
        self.tabWidth        = self._parseLine(cnfParse, cnfSec, "tabwidth",    self.CNF_INT,  self.tabWidth)
        self.doJustify       = self._parseLine(cnfParse, cnfSec, "justify",     self.CNF_BOOL, self.doJustify)
        self.autoSelect      = self._parseLine(cnfParse, cnfSec, "autoselect",  self.CNF_BOOL, self.autoSelect)
        self.doReplace       = self._parseLine(cnfParse, cnfSec, "autoreplace", self.CNF_BOOL, self.doReplace)
        self.doReplaceSQuote = self._parseLine(cnfParse, cnfSec, "repsquotes",  self.CNF_BOOL, self.doReplaceSQuote)
        self.doReplaceDQuote = self._parseLine(cnfParse, cnfSec, "repdquotes",  self.CNF_BOOL, self.doReplaceDQuote)
        self.doReplaceDash   = self._parseLine(cnfParse, cnfSec, "repdash",     self.CNF_BOOL, self.doReplaceDash)
        self.doReplaceDots   = self._parseLine(cnfParse, cnfSec, "repdots",     self.CNF_BOOL, self.doReplaceDots)
        self.styleSQuote     = self._parseLine(cnfParse, cnfSec, "stylesquote", self.CNF_INT,  self.styleSQuote)
        self.styleDQuote     = self._parseLine(cnfParse, cnfSec, "styledquote", self.CNF_INT,  self.styleDQuote)
        self.spellLanguage   = self._parseLine(cnfParse, cnfSec, "spellcheck",  self.CNF_STR,  self.spellLanguage)

        ## Path
        cnfSec = "Path"
        for i in range(10):
            self.recentList[i] = self._parseLine(cnfParse, cnfSec, "recent%d" % i,self.CNF_STR, self.recentList[i])

        if self.styleSQuote >= 0 and self.styleSQuote < len(nwQuotes.SINGLE):
            self.fmtSingleQuotes[0] = nwQuotes.SINGLE[self.styleSQuote][0]
            self.fmtSingleQuotes[1] = nwQuotes.SINGLE[self.styleSQuote][1]
        if self.styleDQuote >= 0 and self.styleDQuote < len(nwQuotes.DOUBLE):
            self.fmtDoubleQuotes[0] = nwQuotes.DOUBLE[self.styleDQuote][0]
            self.fmtDoubleQuotes[1] = nwQuotes.DOUBLE[self.styleDQuote][1]

        return True

    def saveConfig(self):

        logger.debug("Saving config file")
        cnfParse = configparser.ConfigParser()

        # Set options

        ## Main
        cnfSec = "Main"
        cnfParse.add_section(cnfSec)
        cnfParse.set(cnfSec,"timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cnfParse.set(cnfSec,"theme",     str(self.guiTheme))

        ## Sizes
        cnfSec = "Sizes"
        cnfParse.add_section(cnfSec)
        cnfParse.set(cnfSec,"geometry", self._packList(self.winGeometry))
        cnfParse.set(cnfSec,"treecols", self._packList(self.treeColWidth))
        cnfParse.set(cnfSec,"mainpane", self._packList(self.mainPanePos))
        cnfParse.set(cnfSec,"docpane",  self._packList(self.docPanePos))
        cnfParse.set(cnfSec,"timeline", self._packList(self.dlgTimeLine))

        ## Project
        cnfSec = "Project"
        cnfParse.add_section(cnfSec)
        cnfParse.set(cnfSec,"autosaveproject", str(self.autoSaveProj))
        cnfParse.set(cnfSec,"autosavedoc",     str(self.autoSaveDoc))

        ## Editor
        cnfSec = "Editor"
        cnfParse.add_section(cnfSec)
        cnfParse.set(cnfSec,"textfont",   str(self.textFont))
        cnfParse.set(cnfSec,"textsize",   str(self.textSize))
        cnfParse.set(cnfSec,"fixedwidth", str(self.textFixedW))
        cnfParse.set(cnfSec,"width",      str(self.textWidth))
        cnfParse.set(cnfSec,"margins",    self._packList(self.textMargin))
        cnfParse.set(cnfSec,"tabwidth",   str(self.tabWidth))
        cnfParse.set(cnfSec,"justify",    str(self.doJustify))
        cnfParse.set(cnfSec,"autoselect", str(self.autoSelect))
        cnfParse.set(cnfSec,"autoreplace",str(self.doReplace))
        cnfParse.set(cnfSec,"repsquotes", str(self.doReplaceSQuote))
        cnfParse.set(cnfSec,"repdquotes", str(self.doReplaceDQuote))
        cnfParse.set(cnfSec,"repdash",    str(self.doReplaceDash))
        cnfParse.set(cnfSec,"repdots",    str(self.doReplaceDots))
        cnfParse.set(cnfSec,"stylesquote",str(self.styleSQuote))
        cnfParse.set(cnfSec,"styledquote",str(self.styleDQuote))
        cnfParse.set(cnfSec,"spellcheck", str(self.spellLanguage))

        ## Path
        cnfSec = "Path"
        cnfParse.add_section(cnfSec)
        for i in range(10):
            cnfParse.set(cnfSec,"recent%d" % i, str(self.recentList[i]))

        # Write config file
        try:
            cnfParse.write(open(path.join(self.confPath,self.confFile),"w"))
            self.confChanged = False
        except Exception as e:
            logger.error("Could not save config file")
            return False

        return True

    ##
    #  Setters
    ##

    def setRecent(self, recentPath):
        if recentPath == "": return
        if recentPath in self.recentList[0:10]:
            self.recentList.remove(recentPath)
        self.recentList.insert(0,recentPath)
        return

    def setConfPath(self, newPath):
        if newPath is None:
            return True
        if not path.isfile(newPath):
            logger.error("Config: File not found. Using default config path instead.")
            return False
        self.confPath = path.dirname(newPath)
        self.confFile = path.basename(newPath)
        return True

    def setWinSize(self, newWidth, newHeight):
        if abs(self.winGeometry[0] - newWidth) > 5:
            self.winGeometry[0] = newWidth
            self.confChanged = True
        if abs(self.winGeometry[1] - newHeight) > 5:
            self.winGeometry[1] = newHeight
            self.confChanged = True
        return True

    def setTLineSize(self, newWidth, newHeight):
        if abs(self.dlgTimeLine[0] - newWidth) > 5:
            self.dlgTimeLine[0] = newWidth
            self.confChanged = True
        if abs(self.dlgTimeLine[1] - newHeight) > 5:
            self.dlgTimeLine[1] = newHeight
            self.confChanged = True
        return True

    def setTreeColWidths(self, colWidths):
        self.treeColWidth = colWidths
        self.confChanged = True
        return True

    def setMainPanePos(self, panePos):
        self.mainPanePos = panePos
        self.confChanged = True
        return True

    def setDocPanePos(self, panePos):
        self.docPanePos  = panePos
        self.confChanged = True
        return True

    ##
    #  Internal Functions
    ##

    def _unpackList(self, inStr, listLen, listDefault, castTo=int):
        inData  = inStr.split(",")
        outData = []
        for i in range(listLen):
            try:
                outData.append(castTo(inData[i]))
            except:
                outData.append(listDefault[i])
        return outData

    def _packList(self, inData):
        return ", ".join(str(inVal) for inVal in inData)

    def _parseLine(self, cnfParse, cnfSec, cnfName, cnfType, cnfDefault):
        if cnfParse.has_section(cnfSec):
            if cnfParse.has_option(cnfSec, cnfName):
                if cnfType == self.CNF_STR:
                    return cnfParse.get(cnfSec, cnfName)
                elif cnfType == self.CNF_INT:
                    return cnfParse.getint(cnfSec, cnfName)
                elif cnfType == self.CNF_BOOL:
                    return cnfParse.getboolean(cnfSec, cnfName)
                elif cnfType == self.CNF_LIST:
                    return self._unpackList(
                        cnfParse.get(cnfSec, cnfName), len(cnfDefault), cnfDefault
                    )
        return cnfDefault

# End Class Config
