import sys

class ReleaseManager:

    plugins = [
            #{ "name":"script.common.plugin.cache", "url":"http://hg.tobiasussing.dk/hgweb.cgi/cachexbmc/"},
            #{ "name":"script.module.simple.downloader", "url":"http://hg.tobiasussing.dk/hgweb.cgi/downloadxbmc"},
            { "name":"script.module.parsedom", "url":"http://hg.tobiasussing.dk/hgweb.cgi/commonxbmc/"},
            #{ "name":"plugin.video.youtube", "url":"http://hg.tobiasussing.dk/hgweb.cgi/youtubexbmc/"},
            #{ "name":"plugin.video.vimeo", "url":"http://hg.tobiasussing.dk/hgweb.cgi/vimeoxbmc/"},
            #{ "name":"plugin.video.bliptv", "url":"http://hg.tobiasussing.dk/hgweb.cgi/bliptvxbmc/"}
          ]

    xbmc_imports = [{"name":"xbmc.python", "eden_version": "2.0", "frodo_version":"2.1.0", "testing_version":"12.23" }]

    branches = ["testing", "default"]

    branch_versions = {"testing":12}

    updates = []

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem
        self.repository = sys.modules["__main__"].repository
        self.pluginmanager = sys.modules["__main__"].pluginmanager

    def updatePluginsAsNecessary(self):
        self.setupWorkingFolders()

        for plugin in self.plugins:
            self.clonePluginFromRepositoryBranchesToWorkingFolders(plugin)
            self.pluginmanager.extractDependencyInformationFromMainBranch(plugin)
            self.pluginmanager.extractVersionInformationFromBranches(plugin, self.branches)

        self.updates = self.pluginmanager.getPluginBranchesWhichNeedToBeUpdated(self.plugins, self.branches)

        self.updateReleaseBranches()
        self.packageNewPluginVersionsAsZipFiles(self.updates)

    def setupWorkingFolders(self):
        self.filesystem.deleteWorkingFolderRecursively()
        self.filesystem.createWorkingFolderStructure(self.branches)

    def clonePluginFromRepositoryBranchesToWorkingFolders(self, plugin):
        for branch in self.branches:
            self.repository.cloneBranch(plugin, branch)

    def updateReleaseBranches(self):

        for update in self.updates:
            # clean each plugin subdir in each branch subdir
            self.filesystem.cleanReleaseBranch(update)
            self.filesystem.copyPluginToReleaseBranch(update)

            self.pluginmanager.UpdateVersionAndNames(update, self.branch_versions)
            self.pluginmanager.UpdateDependencies(update, self.branch_versions, self.plugins, self.xbmc_imports)

            self.repository.updateBranch(update)


    def packageNewPluginVersionsAsZipFiles(self, updates):
        pass

        #for each plugin
            # clone main branch of plugin to subdir in trunk
            # get the current version in release and save it
            # clone each release branch of plugin to subdir in branch subdir
            # get the current version in each branch and save it
            # if a branch is out of date (a new version is ready) save that status

    def emailUpdatesToMaintainers(self):
        for plugin_update in self.updates:
            print repr(plugin_update)
