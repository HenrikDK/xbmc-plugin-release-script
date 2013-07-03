import sys

class PluginManager:

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem
        self.dependencymanager = sys.modules["__main__"].dependencymanager
        self.versionmanager = sys.modules["__main__"].versionmanager
        self.addonxmlupdater = sys.modules["__main__"].addonxmlupdater

    def extractPluginInformationFromBranches(self, plugin, branches, branch_versions):
        self.versionmanager.extractVersionInformationFromBranches(plugin, branches)
        self.dependencymanager.extractDependencyInformationFromBranches(plugin, branches)
        self.versionmanager.extrapolateCurrentVersionsFromMasterBranchVersion(plugin, branches, branch_versions)

    def getPluginBranchesWhichNeedToBeUpdated(self, plugins, branches):
        print "calculating necessary updates"
        result = []

        for plugin in plugins:
            for branch in branches:
                print repr(branch)  + " - " + repr(plugin)
                if branch != "master" and plugin[branch + "_version"] != plugin["master_" + branch + "_version"]:
                    result.append( {"plugin": plugin, "branch": branch, "reason":"update available"} )

        print "the following plugins will be updated: " + repr(result)
        return result

    def updatePlugin(self, update, branch_versions, plugins, xbmc_imports):
        self.versionmanager.UpdateVersionAndNames(update, branch_versions)
        self.dependencymanager.UpdateDependencies(update, branch_versions, plugins, xbmc_imports)
        self.addonxmlupdater.UpdateVersionNumberAndDependencyInformationInAddonXml(update)

    def updateMainPluginXML(self, update):
        self.addonxmlupdater.UpdateVersionNumberAndDependencyInformationInAddonXml(update)