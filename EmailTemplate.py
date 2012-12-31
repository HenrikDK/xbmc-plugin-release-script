import sys

class EmailTemplate:
    def __init__(self):
        self.repository = sys.modules["__main__"].repository

    def createEmailFromTemplate(self, updates):
        print "\n"
        subject = self.getEmailSubject(updates)
        print subject

        for update in updates:
            print ""
            self.repository.getBranchUpdateDetails(update)
            details = self.getUpdateDetails(update)
            print details

    def getUpdateDetails(self, update):
        details = ""
        details += "*addon - " + update["plugin"]["name"] + "\r\n"
        details += "*version - " + update["plugin"]["new_" + update["branch"] + "_version"] + "\r\n"
        details += "*url - " + update["plugin"]["url"] + "\r\n"
        details += "*revision - " + update["revision"]
        details += "*branch - " + update["branch"] + "\r\n"
        details += "*xbmc version - " + update["branch"] + "\r\n"
        return details

    def getEmailSubject(self, updates):
        plugins = []
        for update in updates:
            plugins.append(update["plugin"]["name"])

        plugins = list(set(plugins))

        return "[Hg Pull] " + " ".join(plugins)