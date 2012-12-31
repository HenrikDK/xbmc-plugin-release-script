import shutil
import os
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