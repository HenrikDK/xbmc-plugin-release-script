import sys
import xml.etree.ElementTree as ET

class PluginManager:

    plugins = [
            { "name":"script.common.plugin.cache", "url":"http://hg.tobiasussing.dk/hgweb.cgi/cachexbmc/"},
            { "name":"script.module.simple.downloader", "url":"http://hg.tobiasussing.dk/hgweb.cgi/downloadxbmc"},
            { "name":"script.module.parsedom", "url":"http://hg.tobiasussing.dk/hgweb.cgi/commonxbmc/"},
            { "name":"plugin.video.youtube", "url":"http://hg.tobiasussing.dk/hgweb.cgi/youtubexbmc/"},
            { "name":"plugin.video.vimeo", "url":"http://hg.tobiasussing.dk/hgweb.cgi/vimeoxbmc/"},
            { "name":"plugin.video.bliptv", "url":"http://hg.tobiasussing.dk/hgweb.cgi/bliptvxbmc/"}
          ]

    branches = ["eden", "default"]
    branch_versions = {"eden":"1", "frodo":"2"}

    updates = []

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem
        self.repository = sys.modules["__main__"].repository

    def setupWorkingFolders(self):
        self.filesystem.deleteWorkingFolderRecursively()
        self.filesystem.createWorkingFolderStructure(self.branches)

    def clonePluginFromRepositoryBranchesToWorkingFolders(self, plugin):
        for branch in self.branches:
            self.repository.cloneBranch(plugin, branch)

    def extractVersionInformationFromBranches(self, plugin):
        for branch in self.branches:
            version_string = "0.0.0"
            file = self.filesystem.readAddonXml(plugin, branch)
            if len(file) > 0:
                xml = ET.fromstring(file)
                version_string = xml.attrib['version']
            version = version_string.split(".")

            plugin[ branch + "_version"] = version_string

    def getPluginBranchesWhichNeedToBeUpdated(self):
        result = []

        for plugin in self.plugins:
            for branch in self.branches:
                if plugin[branch + "_version"] != plugin["default_version"] and branch != "default":
                    result.append( (plugin, branch) )

        return result

    def updateReleaseBranches(self):

        for (plugin, branch) in self.updates:
            # clean each plugin subdir in each branch subdir
            self.filesystem.cleanReleaseBranch(plugin, branch)
            self.filesystem.copyPluginToReleaseBranch(plugin, branch)
            self.filesystem.UpdateVersionAndNames(plugin, branch)
            # copy contents of plugin subdir from main branch to release branch

        pass

    def packageNewPluginVersionsAsZipFiles(self, updates):
        pass

    def updatePluginsAsNecessary(self):
        self.setupWorkingFolders()

        for plugin in self.plugins:
            self.clonePluginFromRepositoryBranchesToWorkingFolders(plugin)

            self.extractVersionInformationFromBranches(plugin)

        self.updates = self.getPluginBranchesWhichNeedToBeUpdated()

        self.updateReleaseBranches()
        self.packageNewPluginVersionsAsZipFiles(self.updates)

        #for each plugin
            # clone main branch of plugin to subdir in trunk
            # get the current version in release and save it
            # clone each release branch of plugin to subdir in branch subdir
            # get the current version in each branch and save it
            # if a branch is out of date (a new version is ready) save that status

    def emailUpdatesToMaintainers(self):
        for plugin_update in self.updates:
            print repr(plugin_update)
