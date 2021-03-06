# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010-2017  Sergey Satskiy <sergey.satskiy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Menu provider for codimension subversion plugin
"""


import os.path
from ui.mainwindowtabwidgetbase import MainWindowTabWidgetBase
from utils.fileutils import isFileSearchable
from utils.pixmapcache import getIcon
from .svnindicators import (pluginHomeDir, IND_ERROR, IND_ADDED, IND_DELETED,
                            IND_MERGED, IND_MODIFIED_LR, IND_MODIFIED_L,
                            IND_REPLACED, IND_CONFLICTED, IND_UPTODATE)


class SVNMenuMixin:

    """
    Adds menu functionality to the plugin class
    """

    def __init__(self):
        pass

    def populateMainMenu(self, parentMenu):
        """Called to build main menu"""
        parentMenu.aboutToShow.connect(self.onMainMenuAboutToShow)
        parentMenu.addAction(getIcon(pluginHomeDir + 'svnmenuconf.png'),
                             'Configure', self.configure)

    def populateFileContextMenu(self, parentMenu):
        """Builds a file context menu in the project and FS browsers"""
        self.fileParentMenu = parentMenu
        parentMenu.aboutToShow.connect(self.onFileContextMenuAboutToShow)
        self.fileContextInfoAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuinfo.png'),
            "Detailed &info", self.fileInfo)
        self.fileContextAnnotateAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuannotate.png'),
            "&Annotate", self.fileAnnotate)
        self.fileContextLogAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenulog.png'),
            "&Log...", self.fileLog)
        self.fileContextDiffAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenudiff.png'),
            "&Diff", self.fileDiff)
        parentMenu.addSeparator()
        self.fileContextUpdateAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuupdate.png'),
            "&Update", self.fileUpdate)
        self.fileContextPropsAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuprops.png'),
            "&Properties...", self.fileProps)
        self.fileContextAddAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuadd.png'),
            "A&dd", self.fileAddToRepository)
        self.fileContextCommitAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenucommit.png'),
            "&Commit...", self.fileCommit)
        self.fileContextRevertAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuundo.png'),
            "&Revert", self.fileRevert)
        parentMenu.addSeparator()
        self.fileContextDeleteAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenudelete.png'),
            "D&elete...", self.fileDelete)

    def populateDirectoryContextMenu(self, parentMenu):
        """Builds a dir context menu in the project and FS browsers"""
        self.dirParentMenu = parentMenu
        parentMenu.aboutToShow.connect(self.onDirectoryContextMenuAboutToShow)
        self.dirContextInfoAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuinfo.png'),
            "Detailed &info ", self.dirInfo)
        self.dirContextLocalStatusAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenustatus.png'),
            "&Status (local only)...", self.dirLocalStatus)
        self.dirContextReposStatusAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenustatus.png'),
            "S&tatus (repository)...", self.dirRepositoryStatus)
        parentMenu.addSeparator()
        self.dirContextUpdateAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuupdate.png'),
            "&Update", self.dirUpdate)
        self.dirContextPropsAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuprops.png'),
            "&Properties...", self.dirProps)
        self.dirContextAddAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuadd.png'),
            "A&dd", self.dirAddToRepository)
        self.dirContextAddRecursiveAct = parentMenu.addAction(
            "Add recursively", self.dirAddToRepositoryRecursively)
        self.dirContextCommitAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenucommit.png'),
            "&Commit...", self.dirCommit)
        self.dirContextRevertAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuundo.png'),
            "&Revert", self.dirRevert)
        parentMenu.addSeparator()
        self.dirContextDeleteAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenudelete.png'),
            "D&elete...", self.dirDelete)

    def populateBufferContextMenu(self, parentMenu):
        """Called to build a buffer context menu"""
        parentMenu.aboutToShow.connect(self.onBufferContextMenuAboutToshow)
        self.bufContextInfoAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuinfo.png'),
            "Detailed &info", self.bufferInfo)
        self.bufContextAnnotateAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuannotate.png'),
            "&Annotate", self.bufferAnnotate)
        self.bufContextLogAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenulog.png'),
            "&Log...", self.bufferLog)
        self.bufContextUpdateAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuupdate.png'),
            "&Update", self.bufferUpdate)
        self.bufContextPropsAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuprops.png'),
            "&Properties...", self.bufferProps)
        self.bufContextDiffAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenudiff.png'),
            "&Diff", self.bufferDiff)
        parentMenu.addSeparator()
        self.bufContextAddAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuadd.png'),
            "A&dd", self.bufferAddToRepository)
        self.bufContextCommitAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenucommit.png'),
            "&Commit...", self.bufferCommit)
        self.bufContextRevertAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenuundo.png'),
            "&Revert", self.bufferRevert)
        parentMenu.addSeparator()
        self.bufContextDeleteAct = parentMenu.addAction(
            getIcon(pluginHomeDir + 'svnmenudelete.png'),
            "D&elete...", self.bufferDelete)

    def onMainMenuAboutToShow(self):
        """Called when a main menu is about to show"""
        pass

    def onFileContextMenuAboutToShow(self):
        """Called when the plugin file context menu is about to show"""
        path = str(self.fileParentMenu.menuAction().data().toString())
        pathStatus = self.getLocalStatus(path)
        debugMode = self.ide.mainWindow.debugMode
        if pathStatus == IND_ERROR:
            self.fileContextInfoAct.setEnabled(False)
            self.fileContextUpdateAct.setEnabled(False)
            self.fileContextAnnotateAct.setEnabled(False)
            self.fileContextLogAct.setEnabled(False)
            self.fileContextAddAct.setEnabled(False)
            self.fileContextCommitAct.setEnabled(False)
            self.fileContextDeleteAct.setEnabled(False)
            self.fileContextRevertAct.setEnabled(False)
            self.fileContextDiffAct.setEnabled(False)
            self.fileContextPropsAct.setEnabled(False)
            return

        if pathStatus == self.NOT_UNDER_VCS:
            self.fileContextInfoAct.setEnabled(False)
            self.fileContextUpdateAct.setEnabled(False)
            self.fileContextAnnotateAct.setEnabled(False)
            self.fileContextLogAct.setEnabled(False)
            self.fileContextCommitAct.setEnabled(False)
            self.fileContextDeleteAct.setEnabled(False)
            self.fileContextRevertAct.setEnabled(False)
            self.fileContextDiffAct.setEnabled(False)
            self.fileContextPropsAct.setEnabled(False)

            upperDirStatus = self.getLocalStatus(os.path.dirname(path))
            if upperDirStatus == self.NOT_UNDER_VCS:
                self.fileContextAddAct.setEnabled(False)
            else:
                self.fileContextAddAct.setEnabled(upperDirStatus != IND_ERROR
                                                  and not debugMode)
            return

        self.fileContextInfoAct.setEnabled(True)
        self.fileContextUpdateAct.setEnabled(not debugMode)
        self.fileContextAnnotateAct.setEnabled(True)
        self.fileContextLogAct.setEnabled(True)
        self.fileContextAddAct.setEnabled(False)
        self.fileContextPropsAct.setEnabled(not debugMode)
        self.fileContextCommitAct.setEnabled(
            pathStatus in [IND_ADDED, IND_DELETED, IND_MERGED, IND_MODIFIED_LR,
                           IND_MODIFIED_L, IND_REPLACED, IND_CONFLICTED] and
            not debugMode)
        self.fileContextDeleteAct.setEnabled(pathStatus != IND_DELETED and
                                             not debugMode)
        self.fileContextRevertAct.setEnabled(pathStatus != IND_UPTODATE and
                                             not debugMode)

        # Diff makes sense only for text files
        self.fileContextDiffAct.setEnabled(isFileSearchable(path))

    def onDirectoryContextMenuAboutToShow(self):
        """Called when the plugin directory context manu is about to show"""
        path = self.dirParentMenu.menuAction().data()
        pathStatus = self.getLocalStatus(path)
        debugMode = self.ide.mainWindow.debugMode
        if pathStatus == IND_ERROR:
            self.dirContextInfoAct.setEnabled(False)
            self.dirContextUpdateAct.setEnabled(False)
            self.dirContextAddAct.setEnabled(False)
            self.dirContextAddRecursiveAct.setEnabled(False)
            self.dirContextCommitAct.setEnabled(False)
            self.dirContextLocalStatusAct.setEnabled(False)
            self.dirContextReposStatusAct.setEnabled(False)
            self.dirContextDeleteAct.setEnabled(False)
            self.dirContextRevertAct.setEnabled(False)
            self.dirContextPropsAct.setEnabled(False)
            return

        if pathStatus == self.NOT_UNDER_VCS:
            self.dirContextInfoAct.setEnabled(False)
            self.dirContextUpdateAct.setEnabled(False)
            self.dirContextCommitAct.setEnabled(False)
            self.dirContextLocalStatusAct.setEnabled(False)
            self.dirContextReposStatusAct.setEnabled(False)
            self.dirContextDeleteAct.setEnabled(False)
            self.dirContextRevertAct.setEnabled(False)
            self.dirContextPropsAct.setEnabled(False)

            if path.endswith(os.path.sep):
                upperDirStatus = self.getLocalStatus(
                    os.path.dirname(path[:-1]))
            else:
                upperDirStatus = self.getLocalStatus(os.path.dirname(path))
            if upperDirStatus == self.NOT_UNDER_VCS:
                self.dirContextAddAct.setEnabled(False)
                self.dirContextAddRecursiveAct.setEnabled(False)
            else:
                self.dirContextAddAct.setEnabled(
                    upperDirStatus != IND_ERROR and not debugMode)
                self.dirContextAddRecursiveAct.setEnabled(
                    upperDirStatus != IND_ERROR and not debugMode)
            return

        self.dirContextInfoAct.setEnabled(True)
        self.dirContextUpdateAct.setEnabled(not debugMode)
        self.dirContextAddAct.setEnabled(False)
        self.dirContextAddRecursiveAct.setEnabled(not debugMode)
        self.dirContextCommitAct.setEnabled(not debugMode)
        self.dirContextLocalStatusAct.setEnabled(True)
        self.dirContextReposStatusAct.setEnabled(True)
        self.dirContextDeleteAct.setEnabled(
            pathStatus != IND_DELETED and not debugMode)
        self.dirContextRevertAct.setEnabled(
            pathStatus != IND_UPTODATE and not debugMode)
        self.dirContextPropsAct.setEnabled(not debugMode)

    def onBufferContextMenuAboutToshow(self):
        """Called when the plugin buffer context menu is about to show"""
        path = self.ide.currentEditorWidget.getFileName()
        debugMode = self.ide.mainWindow.debugMode
        if not os.path.isabs(path):
            self.bufContextInfoAct.setEnabled(False)
            self.bufContextUpdateAct.setEnabled(False)
            self.bufContextAnnotateAct.setEnabled(False)
            self.bufContextLogAct.setEnabled(False)
            self.bufContextAddAct.setEnabled(False)
            self.bufContextCommitAct.setEnabled(False)
            self.bufContextDeleteAct.setEnabled(False)
            self.bufContextRevertAct.setEnabled(False)
            self.bufContextDiffAct.setEnabled(False)
            self.bufContextPropsAct.setEnabled(False)
            return

        pathStatus = self.getLocalStatus(path)
        if pathStatus == IND_ERROR:
            self.bufContextInfoAct.setEnabled(False)
            self.bufContextUpdateAct.setEnabled(False)
            self.bufContextAnnotateAct.setEnabled(False)
            self.bufContextLogAct.setEnabled(False)
            self.bufContextAddAct.setEnabled(False)
            self.bufContextCommitAct.setEnabled(False)
            self.bufContextDeleteAct.setEnabled(False)
            self.bufContextRevertAct.setEnabled(False)
            self.bufContextDiffAct.setEnabled(False)
            self.bufContextPropsAct.setEnabled(False)
            return

        if pathStatus == self.NOT_UNDER_VCS:
            self.bufContextInfoAct.setEnabled(False)
            self.bufContextUpdateAct.setEnabled(False)
            self.bufContextAnnotateAct.setEnabled(False)
            self.bufContextLogAct.setEnabled(False)
            self.bufContextCommitAct.setEnabled(False)
            self.bufContextDeleteAct.setEnabled(False)
            self.bufContextRevertAct.setEnabled(False)
            self.bufContextDiffAct.setEnabled(False)
            self.bufContextPropsAct.setEnabled(False)

            upperDirStatus = self.getLocalStatus(os.path.dirname(path))
            if upperDirStatus == self.NOT_UNDER_VCS:
                self.bufContextAddAct.setEnabled(False)
            else:
                self.bufContextAddAct.setEnabled(
                    upperDirStatus != IND_ERROR and not debugMode)
            return

        self.bufContextInfoAct.setEnabled(True)
        self.bufContextUpdateAct.setEnabled(not debugMode)
        self.bufContextAddAct.setEnabled(False)
        self.bufContextPropsAct.setEnabled(not debugMode)
        self.bufContextDeleteAct.setEnabled(
            pathStatus != IND_DELETED and not debugMode)
        self.bufContextRevertAct.setEnabled(
            pathStatus != IND_UPTODATE and not debugMode)

        # Diff makes sense only for text files
        self.bufContextDiffAct.setEnabled(isFileSearchable(path))

        widgetType = self.ide.currentEditorWidget.getType()
        if widgetType in [MainWindowTabWidgetBase.PlainTextEditor,
                          MainWindowTabWidgetBase.PythonGraphicsEditor]:
            self.bufContextAnnotateAct.setEnabled(True)
            self.bufContextLogAct.setEnabled(True)
        else:
            self.bufContextAnnotateAct.setEnabled(False)
            self.bufContextLogAct.setEnabled(False)

        # Set the Commit... menu item status
        if pathStatus not in [IND_ADDED, IND_DELETED, IND_MERGED,
                              IND_MODIFIED_LR, IND_MODIFIED_L, IND_REPLACED,
                              IND_CONFLICTED]:
            self.bufContextCommitAct.setEnabled(False)
        else:
            if widgetType in [MainWindowTabWidgetBase.PlainTextEditor,
                              MainWindowTabWidgetBase.PythonGraphicsEditor]:
                self.bufContextCommitAct.setEnabled(
                    not self.ide.currentEditorWidget.isModified() and
                    not debugMode)
            else:
                self.bufContextCommitAct.setEnabled(False)
