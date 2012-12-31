import sys

class ReleaseManager:

    plugins = [
            { "name":"script.common.plugin.cache", "url":"http://hg.tobiasussing.dk/hgweb.cgi/cachexbmc/"},
            { "name":"script.module.simple.downloader", "url":"http://hg.tobiasussing.dk/hgweb.cgi/downloadxbmc"},
            { "name":"script.module.parsedom", "url":"http://hg.tobiasussing.dk/hgweb.cgi/commonxbmc/"},
            { "name":"plugin.video.youtube", "url":"http://hg.tobiasussing.dk/hgweb.cgi/youtubexbmc/"},
            { "name":"plugin.video.vimeo", "url":"http://hg.tobiasussing.dk/hgweb.cgi/vimeoxbmc/"},
            { "name":"plugin.video.bliptv", "url":"http://hg.tobiasussing.dk/hgweb.cgi/bliptvxbmc/"}
          ]

    xbmc_imports = [{"name":"xbmc.python", "eden_version": "2.0", "frodo_version":"2.1.0"}]

    branches = ["frodo", "eden", "default"]

    branch_versions = {"frodo" : 1}

    updates = []

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem
        self.repository = sys.modules["__main__"].repository
        self.pluginmanager = sys.modules["__main__"].pluginmanager
        self.template = sys.modules["__main__"].template

    def updatePluginsAsNecessary(self):
        self.setupWorkingFolders()

        for plugin in self.plugins:
            self.clonePluginFromRepositoryBranchesToWorkingFolders(plugin)
            self.pluginmanager.extractPluginInformationFromBranches(plugin, self.branches)

        self.updates = self.pluginmanager.getPluginBranchesWhichNeedToBeUpdated(self.plugins, self.branches)

        self.updatePluginReleaseBranches()
        self.packageNewPluginVersionsAsZipFiles(self.updates)
        self.template.createEmailFromTemplate(self.updates)

    def setupWorkingFolders(self):
        self.filesystem.deleteWorkingFolderRecursively()
        self.filesystem.createWorkingFolderStructure(self.branches)

    def clonePluginFromRepositoryBranchesToWorkingFolders(self, plugin):
        for branch in self.branches:
            self.repository.cloneBranch(plugin, branch)

    def updatePluginReleaseBranches(self):

        for update in self.updates:
            print "\n"
            print "Updating plugin: " + update["plugin"]["name"] + " - branch: " + update["branch"] + " - reason: " + update["reason"]
            print ""
            # clean each plugin subdir in each branch subdir
            self.filesystem.cleanReleaseBranch(update)
            self.filesystem.copyPluginToReleaseBranch(update)

            self.pluginmanager.updatePlugin(update, self.branch_versions, self.plugins, self.xbmc_imports)

            self.repository.updateBranch(update)

    def packageNewPluginVersionsAsZipFiles(self, updates):
        pass