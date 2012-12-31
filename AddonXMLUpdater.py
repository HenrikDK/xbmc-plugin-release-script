import shutil
import os
import xml.etree.ElementTree as ET
from distutils import dir_util

class FileSystem():

    def deleteWorkingFolderRecursively(self):
        if os.path.exists("./tmp"):
            shutil.rmtree('./tmp')

    def createWorkingFolderStructure(self, branches):
        os.makedirs("./tmp")
        for branch in branches:
            os.makedirs("./tmp/" + branch)

    def readFileFromDisk(self, filePath):
        if (os.path.exists(filePath)):
            with open(filePath, "r") as f:
                result = f.read()
            return result
        return ""

    def saveFileToDisk(self, filePath, contents):
        if (os.path.exists(filePath)):
            with open(filePath, "w") as f:
                f.write(contents)

    def readAddonXml(self, plugin, branch):
        filePath = "addon.xml"

        if branch == "default":
            filePath = "plugin/" + filePath

        filePath = "tmp/" + branch + "/" + plugin["name"] + "/" + filePath
        return self.readFileFromDisk(filePath)

    def cleanReleaseBranch(self, update):
        folderPath = "tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"

        print "cleaning branch folder: " + folderPath
        for root, dirs, files in os.walk(folderPath):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                if d != ".hg":
                    shutil.rmtree(os.path.join(root, d))

    def cleanCompiledOutputFromReleaseBranch(self, update):
        folderPath = "tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"

        print "cleaning compiled output from release folder: " + folderPath
        for root, dirs, files in os.walk(folderPath):
            for f in files:
                if f.find(".pyc") > 0:
                    os.unlink(os.path.join(root, f))

    def copyPluginToReleaseBranch(self, update):
        source = "tmp/default/" + update["plugin"]["name"] + "/plugin/"
        destination = "tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"

        print "copying files from: " + source + " to: " + destination
        dir_util.copy_tree(source, destination)

    def getAllPluginFiles(self, update):
        python_files = []
        branch_folder = "tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"
        for folder_name, dirs, files in os.walk(branch_folder):
            for file_name in files:
                if file_name.rfind(".xml") > 0 or file_name.rfind(".py") > 0:
                    python_files.append(os.path.join(folder_name,file_name))

        return python_files

    def getAllPluginPythonFiles(self, update):
        python_files = []
        branch_folder = "tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"
        for folder_name, dirs, files in os.walk(branch_folder):
            for file_name in files:
                if file_name.rfind(".py") > 0:
                    python_files.append(os.path.join(folder_name,file_name))

        return python_files

    def updateVersionNumberAndDependencyInformationInAddonXml(self, update):
        file = "tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/Addon.xml"
        print "updating Addon.xml: " + file
        with open(file) as f:
            s = f.read()

        if len(s) == 0:
            return

        xml = ET.fromstring(s)
        xml.attrib["version"] = update["plugin"]["new_" + update["branch"] + "_version"]

        self.updateXMLDependencyInformation(update, xml)

        s = ET.tostring(xml, encoding="UTF-8")

        s = s.replace("<?xml version='1.0' encoding='UTF-8'?>", "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>")
        with open(file, "w") as f:
            f.write(s)

    def updateXMLDependencyInformation(self, plugin_update, xml):
        plugin = plugin_update["plugin"]
        branch = plugin_update["branch"]

        imports = xml.findall("*/import")
        for update in plugin["dependencies"]:
            if not (update.has_key("new_version") or update.has_key("new_" + branch + "_version")):
                continue

            for dependency in imports:
                if (dependency.attrib["addon"] == update["name"]):
                    if (update.has_key("new_version")):
                        dependency.attrib["version"] = update["new_version"]
                    elif (update.has_key("new_" + branch + "_version")):
                        dependency.attrib["version"] = update["new_" + branch + "_version"]
