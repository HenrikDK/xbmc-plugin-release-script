import sys
import re
import xml.etree.ElementTree as ET
from distutils.version import StrictVersion

class VersionManager:

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem

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

    def extrapolateCurrentVersionsFromMasterBranchVersion(self, plugin, branches, branch_versions):
        for branch in branches:
            new_version = self.parseVersionNumber(plugin["master_version"])
            if branch != "master":
                if branch in branch_versions:
                    new_version[0] = new_version[0] + branch_versions[branch]
                plugin["master_" + branch + "_version"] = self.getVersionNumberAsString(new_version)

    def getNewVersionNumberForBranch(self, update, branch_versions):
        main_version = self.parseVersionNumber(update["plugin"]["master_version"])
        new_version = main_version[:]

        if branch_versions.has_key(update["branch"]):
            new_version[0] = new_version[0] + branch_versions[update["branch"]]

        if  update.has_key("reason") and update["reason"] == "dependency updated":
            branch_versions = update["plugin"][update["branch"] + "_version"]
            default_version = update["plugin"]["master_version"]

            if StrictVersion(branch_versions) > StrictVersion(default_version):
                new_version = self.parseVersionNumber(branch_versions)

            new_version[len(new_version) -1] += 1

        if not branch_versions.has_key(update["branch"]):
            update["plugin"]["new_master_version"] = self.getVersionNumberAsString(new_version)

        update["plugin"]["new_"+ update["branch"] + "_version"] = self.getVersionNumberAsString(new_version)

    def UpdateVersionAndNames(self, update, branch_versions):
        self.getNewVersionNumberForBranch(update, branch_versions)
        self.replaceVersionNumberInAllPythonFiles(update)
        self.replaceBetaTagInAllPluginFiles(update)
        self.filesystem.cleanCompiledOutputFromReleaseBranch(update)

    def replaceVersionNumberInAllPythonFiles(self, update):
        files = self.filesystem.getAllPluginPythonFiles(update)
        for file in files:
            print "replacing version number in python file: " + file
            content = self.filesystem.readFileFromDisk(file)
            content = self.replaceVersionNumberInPythonFile(content, update)
            self.filesystem.saveFileToDisk(file, content)

    def replaceVersionNumberInPythonFile(self, content, update):
        old_version = update["plugin"]["master_version"]
        new_version = update["plugin"]["new_" + update["branch"] + "_version"]
        content = content.replace(old_version, new_version)

        versions = re.findall(r'version\s*=\s*\D+([\d.][\d.][\d.]+\d+?)', content)
        if len(versions) > 0:
            print "greedy search found several version declarations in that will be replaced: "
            print repr(versions)

        for version in versions:
            content = content.replace(version, new_version)

        return content

    def replaceBetaTagInAllPluginFiles(self, update):
        files = self.filesystem.getAllPluginFiles(update)
        for file in files:
            print "replacing beta tag in file: " + file
            content = self.filesystem.readFileFromDisk(file)
            content = self.replaceBetaTagInFile(content)
            self.filesystem.saveFileToDisk(file, content)

    def replaceBetaTagInFile(self, content):
        content = content.replace(".beta", "")
        content = content.replace(" Beta", "")
        return content

