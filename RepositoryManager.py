from subprocess import call, check_output

class RepositoryManager:

    def cloneBranch(self, plugin, branch):
        source = plugin["url"]
        destination = "tmp/" + branch + "/" + plugin["name"]

        command = "hg clone " + source + " " + destination + " -b " + branch
        print "cloning: " + source + " into: " + destination
        call(command, shell=True)
        print "destination contents: "
        call("ls -lh" + " tmp/" + branch + "/" + plugin["name"], shell=True)

    def updateBranch(self, update):
        source = "tmp/" + update["branch"] + "/" + update["plugin"]["name"]
        command = "cd " + source + '; hg add && hg commit -m "Jenkins commit" && hg push'
        call(command, shell=True)

    def getBranchUpdateDetails(self, update):
        command = "hg id -r " + update["branch"] + " " + update["plugin"]["url"]
        try:
            update["revision"] = check_output(command, shell=True)
        except :
            update["revision"] = "unable to find revision\r\n"