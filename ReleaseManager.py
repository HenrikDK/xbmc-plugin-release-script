import sys

class ReleaseManager:

    plugins = [
            { "name":"script.common.plugin.cache", "url":"git@github.com:HenrikDK/xbmc-common-cache.git"},
            { "name":"script.module.simple.downloader", "url":"git@github.com:HenrikDK/xbmc-simple-downloader.git" },
            { "name":"script.module.parsedom", "url":"git@github.com:HenrikDK/xbmc-common-plugin-functions.git" },
            { "name":"plugin.video.youtube", "url":"git@github.com:HenrikDK/youtube-xbmc-plugin.git" },
            { "name":"plugin.video.vimeo", "url":"git@github.com:HenrikDK/vimeo-xbmc-plugin.git" },
            { "name":"plugin.video.bliptv", "url":"git@github.com:HenrikDK/bliptv-xbmc-plugin.git" },
          ]
#git@github.com:HenrikDK/youtube-xbmc-plugin.git
    xbmc_imports = [{"name":"xbmc.python", "eden_version": "2.0", "frodo_version":"2.1.0"}]

    repo_branch = "frodo"

    branches = ["frodo", "eden", "master"]

    branch_versions = {"frodo" : 1}

    updates = []

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem
        self.repository = sys.modules["__main__"].repository
        self.pluginmanager = sys.modules["__main__"].pluginmanager
        self.template = sys.modules["__main__"].template

    def updatePluginsAsNecessary(self):
        self.SetupWorkingFolders()

        for plugin in self.plugins:
            self.ClonePluginFromRepositoryBranchesToWorkingFolders(plugin)
            self.pluginmanager.extractPluginInformationFromBranches(plugin, self.branches)

        self.updates = self.pluginmanager.getPluginBranchesWhichNeedToBeUpdated(self.plugins, self.branches)

        self.UpdatePluginReleaseBranches()
        #self.PackageNewPluginVersionsAsZipFiles()
        self.template.createEmailFromTemplate(self.updates)

    def SetupWorkingFolders(self):
        self.filesystem.deleteWorkingFolderRecursively()
        self.filesystem.createWorkingFolderStructure(self.branches)

    def ClonePluginFromRepositoryBranchesToWorkingFolders(self, plugin):
        for branch in self.branches:
            self.repository.cloneBranch(plugin, branch)

    def UpdateMainBranch(self):
        updated = []
        for update in self.updates:
            if update["plugin"]["name"] not in updated:
                updated.append(update["plugin"]["name"])
                main_branch_update = {"plugin": update["plugin"], "branch": "master"}
                self.pluginmanager.updateMainPluginXML(main_branch_update)
                self.repository.updateBranch(main_branch_update)

    def UpdatePluginReleaseBranches(self):

        for update in self.updates:
            print "\n"
            print "Updating plugin: " + update["plugin"]["name"] + " - branch: " + update["branch"] + " - reason: " + update["reason"]
            print ""
            # clean each plugin subdir in each branch subdir
            self.filesystem.cleanReleaseBranch(update)
            self.filesystem.copyPluginToReleaseBranch(update)

            self.pluginmanager.updatePlugin(update, self.branch_versions, self.plugins, self.xbmc_imports)
            self.repository.updateBranch(update)

        self.UpdateMainBranch()

    def PackageNewPluginVersionsAsZipFiles(self):

        for update in self.updates:

            if update["branch"] != self.repo_branch:
                continue

            print "Zip'ing plugin: " + update["plugin"]["name"] + " - branch: " + update["branch"] + " for local repository"

            self.filesystem.copyPluginUpdateToZipBranch(update)
            self.filesystem.cleanPluginZipFolder(update)
            self.filesystem.ZipPluginUpdate(update)
            self.filesystem.copyPluginZipFileToLocalRepository(update)