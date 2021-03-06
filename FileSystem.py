import shutil
import os
from distutils import dir_util
import zipfile

class FileSystem():

    fullRepositoryPath = "/usr/local/www/data/hg/nightly-repo/tmp"

    def deleteWorkingFolderRecursively(self):
        if os.path.exists("../tmp"):
            shutil.rmtree('../tmp')

    def createWorkingFolderStructure(self, branches):
        os.makedirs("../tmp")
        os.makedirs("../tmp/zip")
        for branch in branches:
            os.makedirs("../tmp/" + branch)

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

        if branch == "master":
            filePath = "plugin/" + filePath

        filePath = "../tmp/" + branch + "/" + plugin["name"] + "/" + filePath
        return self.readFileFromDisk(filePath)

    def cleanReleaseBranch(self, update):
        folderPath = "../tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"

        print "cleaning branch folder: " + folderPath
        for root, dirs, files in os.walk(folderPath):
            for f in files:
                file_path = os.path.join(root, f)
                if file_path.rfind(".git") < 0:
                    os.unlink(os.path.join(root, f))
            for d in dirs:
                full_path = os.path.join(root, d)
                if full_path.rfind(".git") < 0:
                    shutil.rmtree(full_path)

    def cleanCompiledOutputFromReleaseBranch(self, update):
        folderPath = "../tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"

        print "cleaning compiled output from release folder: " + folderPath
        for root, dirs, files in os.walk(folderPath):
            for f in files:
                if f.find(".pyc") > 0:
                    os.unlink(os.path.join(root, f))

    def copyPluginToReleaseBranch(self, update):
        source = "../tmp/master/" + update["plugin"]["name"] + "/plugin/"
        destination = "../tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"

        print "copying files from: " + source + " to: " + destination
        dir_util.copy_tree(source, destination)

    def getAllPluginFiles(self, update):
        python_files = []
        branch_folder = "../tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"
        for folder_name, dirs, files in os.walk(branch_folder):
            for file_name in files:
                full_path = os.path.join(folder_name,file_name)
                if full_path.find(".git") >= 0:
                    continue
                if file_name.rfind(".xml") > 0 or file_name.rfind(".py") > 0:
                    python_files.append(full_path)

        return python_files

    def getAllPluginPythonFiles(self, update):
        python_files = []
        branch_folder = "../tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"
        for folder_name, dirs, files in os.walk(branch_folder):
            for file_name in files:
                full_path = os.path.join(folder_name,file_name)
                if full_path.find(".git") >= 0:
                    continue
                if file_name.rfind(".py") > 0:
                    python_files.append(full_path)

        return python_files

    def copyPluginUpdateToZipBranch(self, update):
        source = "../tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/"
        destination = "../tmp/zip/" + update["plugin"]["name"] + "-" + update["plugin"]["new_" + update["branch"] + "_version"] + "/"

        print "copying files from: " + source + " to: " + destination
        dir_util.copy_tree(source, destination)

    def cleanPluginZipFolder(self, update):
        folderPath = "../tmp/zip/" + update["plugin"]["name"] + "-" + update["plugin"]["new_" + update["branch"] + "_version"] + "/"

        print "cleaning zip folder: " + folderPath
        for root, dirs, files in os.walk(folderPath):
            for f in files:
                file_path = os.path.join(root, f)
                if file_path.rfind(".git") >= 0:
                    os.unlink(os.path.join(root, f))
            for d in dirs:
                full_path = os.path.join(root, d)
                if full_path.rfind(".git") >= 0:
                    shutil.rmtree(full_path)

    def ZipPluginUpdate(self, update):
        filename = "../tmp/zip/" + update["plugin"]["name"] + "-" + update["plugin"]["new_" + update["branch"] + "_version"] + ".zip"
        zip_dir = "../tmp/zip/" + update["plugin"]["name"] + "-" + update["plugin"]["new_" + update["branch"] + "_version"] + "/"

        with zipfile.ZipFile(filename, 'w') as myzip:
            for root, dirs, files in os.walk(zip_dir):
                for file in files:
                    fn = os.path.join(root, file)
                    myzip.write(fn, fn[len(zip_dir):])

    def copyPluginZipFileToLocalRepository(self, update):
        filename = "../tmp/zip/" + update["plugin"]["name"] + "-" + update["plugin"]["new_" + update["branch"] + "_version"] + ".zip"

        shutil.copy(filename, self.fullRepositoryPath)
