import sys
import xml.etree.ElementTree as ET
from distutils.version import StrictVersion

class DependencyManager:

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem
        self.versionmanager = sys.modules["__main__"].versionmanager

    def extractDependencyInformationFromBranches(self, plugin, branches):
        dependencies = []
        for branch in branches:
            branch_dependencies = self.extractDependencyInformationFromBranch(plugin, branch)

            for branch_dependency in branch_dependencies:
                self.correlateDependencyBranchVersions(branch_dependency, branch, dependencies)

        plugin["dependencies"] = dependencies

    def correlateDependencyBranchVersions(self, branch_dependency, branch, dependencies):
        dependency_exists = False

        for dependency in dependencies:
            if branch_dependency["name"] == dependency["name"]:
                dependency[branch +"_version"] = branch_dependency[branch + "_version"]
                dependency_exists = True

        if not dependency_exists:
            dependencies.append(branch_dependency)

    def extractDependencyInformationFromBranch(self, plugin, branch):
        file = self.filesystem.readAddonXml(plugin, branch)
        dependencies = []
        if len(file) > 0:
            xml = ET.fromstring(file)
            imports = xml.findall("*/import")
            for dependency in imports:
                temp = {}
                temp["name"] = dependency.attrib["addon"].replace(".beta", "")
                temp[ branch + "_version"] = dependency.attrib["version"]
                dependencies.append(temp)

        return dependencies

    def UpdateDependencies(self, update, branch_versions, plugins, xbmc_imports):
        self.UpdateInternalServiceDependencies(update, branch_versions, plugins)
        self.UpdateXBMCDependencies(update, xbmc_imports)

    def UpdateInternalServiceDependencies(self, update, branch_versions, plugins):
        print "calculating internal service dependencies"
        for dependency in update["plugin"]["dependencies"]:
            self.UpdateDependencyVersionIfNecessary(dependency, update["branch"], branch_versions, plugins)

    def UpdateXBMCDependencies(self, update, xbmc_imports):
        print "calculating xbmc dependencies"
        for dependency in update["plugin"]["dependencies"]:
            self.UpdateXBMCDependencyIfNecessary(dependency, update["branch"], xbmc_imports)

    def UpdateDependencyVersionIfNecessary(self, dependency, branch, branch_versions, plugins):
        plugin = self.getDependencyFromListOfPlugins(dependency["name"], plugins)
        if plugin:
            self.versionmanager.getNewVersionNumberForBranch({"plugin": plugin, "branch": branch}, branch_versions)
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