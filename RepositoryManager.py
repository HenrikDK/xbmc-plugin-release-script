from subprocess import call, check_output

class RepositoryManager:

    def cloneBranch(self, plugin, branch):
        source = plugin["url"]
        destination = "../tmp/" + branch + "/" + plugin["name"]

        command = "git clone " + source + " " + destination + " -b " + branch
        print "cloning: " + source + " into: " + destination
        call(command, shell=True)
        print "destination contents: "
        call("ls -lh" + " ../tmp/" + branch + "/" + plugin["name"], shell=True)

    def updateBranch(self, update):
        source = "../tmp/" + update["branch"] + "/" + update["plugin"]["name"]
        command = "cd " + source + '; git add -u . && git commit -m "Jenkins commit" && git push'
        call(command, shell=True)

    def getBranchUpdateDetails(self, update):
        command = "git ls-remote " + update["plugin"]["url"] + " -b " + update["branch"]
        try:
            revision = check_output(command, shell=True)
            if  len(revision) > 0:
                revision = revision.split()[0]
            update["revision"] = revision + "\r\n"
        except :
            update["revision"] = "unable to find revision\r\n"
