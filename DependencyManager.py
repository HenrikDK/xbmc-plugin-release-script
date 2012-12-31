import sys
import xml.etree.ElementTree as ET
from distutils.version import StrictVersion

class PluginManager:

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem
        self.dependencymanager = sys.modules["__main__"].dependencymanager
        self.versionmanager = sys.modules["__main__"].versionmanager

    def parseVersionNumber(self, version_string):
        version = []
        for v in version_string.split("."):
            version.append(int(v))
        return version

    def getVersionNumberAsString(self, version):
        return ".".join(map(str, version))

    def extractVersionInformationFromBranches(self, plugin, branches):
        for branch in branches:
            version_string = "0.0.0"
            file = self.filesystem.readAddonXml(plugin, branch)
            if len(file) > 0:
                xml = ET.fromstring(file)
                version_string = xml.attrib['version']

            plugin[ branch + "_version"] = version_string

    def extractDependencyInformationFromMainBranch(self, plugin, branches):
        file = self.filesystem.readAddonXml(plugin, "default")
        dependencies = []
        if len(file) > 0:
            xml = ET.fromstring(file)
            imports = xml.findall("*/import")
            for dependency in imports:
                temp = {}
                temp["name"] = dependency.attrib["addon"].replace(".beta","")
                temp["current_version"] = dependency.attrib["version"]
                dependencies.append( temp )

        plugin["dependencies"] = dependencies

    def UpdateVersionAndNames(self, update, branch_versions):
        self.getNewVersionNumberForBranch(update, branch_versions)
        self.filesystem.replaceBetaTagInAllFiles(update)
        self.filesystem.replaceVersionNumberInAllPythonFiles(update)
        self.filesystem.cleanCompiledOutputFromReleaseBranch(update)

    def UpdateDependencies(self, update, branch_versions, plugins, xbmc_imports):
        self.UpdateInternalServiceDependencies(update, branch_versions, plugins)
        self.UpdateXBMCDependencies(update, xbmc_imports)
        self.filesystem.updateVersionNumberAndDependencyInformationInAddonXml(update)

    def UpdateInternalServiceDependencies(self, update, branch_versions, plugins):
        print "calculating internal service dependencies"
        for dependency in update["plugin"]["dependencies"]:
            self.UpdateDependencyVersionIfNecessary(dependency, update["branch"], branch_versions, plugins)

    def UpdateXBMCDependencies(self, update, xbmc_imports):
        print "calculating xbmc dependencies"
        for dependency in update["plugin"]["dependencies"]:
            self.UpdateXBMCDependencyIfNecessary(dependency, update["branch"], xbmc_imports)

    def getPluginBranchesWhichNeedToBeUpdated(self, plugins, branches):
        print "calculating necessary updates"
        result = []

        for plugin in plugins:
            for branch in branches:
                if branch != "default" and plugin[branch + "_version"] != plugin["default_version"]:
                    result.append( {"plugin": plugin, "branch": branch, "reason":"update available"} )

        possible_changes = []
        for update in result:
            for plugin in plugins:
                for dependency in plugin["dependencies"]:
                    if dependency["name"] == update["plugin"]["name"] and dependency["current_version"] != update["plugin"][update["branch"] + "_version"]:
                        possible_changes.append({"plugin": plugin, "branch":update["branch"], "reason": "dependency updated"})

        for change in possible_changes:
            found = False
            for update in result:
                if (change["plugin"]["name"] == update["plugin"]["name"] and change["branch"] == update["branch"]):
                    found = True

            if not found:
                result.append(change)

        print "the following plugins will be updated: " + repr(result)
        return result

    def getNewVersionNumberForBranch(self, update, branch_versions):
        main_version = self.parseVersionNumber(update["plugin"]["default_version"])
        new_version = main_version[:]

        if branch_versions.has_key(update["branch"]):
            new_version[0] = new_version[0] + branch_versions[update["branch"]]

        if  update.has_key("reason") and update["reason"] == "dependency updated":
            branch_versions = update["plugin"][update["branch"] + "_version"]
            default_version = update["plugin"]["default_version"]

            if StrictVersion(branch_versions) > StrictVersion(default_version):
                new_version = self.parseVersionNumber(branch_versions)

            new_version[len(new_version) -1] += 1

        update["plugin"]["new_"+ update["branch"] + "_version"] = self.getVersionNumberAsString(new_version)

    def UpdateDependencyVersionIfNecessary(self, dependency, branch, branch_versions, plugins):
        plugin = self.getDependencyFromListOfPlugins(dependency["name"], plugins)
        if plugin:
            self.getNewVersionNumberForBranch({"plugin": plugin, "branch": branch}, branch_versions)
            dependency["new_version"] = plugin["new_" + branch + "_version"]

    def UpdateXBMCDependencyIfNecessary(self, dependency, branch, xbmc_imports):
        plugin = self.getDependencyFromListOfPlugins(dependency["name"], xbmc_imports)
        if plugin:
            dependency["new_version"] = plugin[branch + "_version"]

    def getDependencyFromListOfPlugins(self, dependency_name, plugins):
        for candidate in plugins:
            if candidate["name"] == dependency_name:
                return candidate
        return ""
