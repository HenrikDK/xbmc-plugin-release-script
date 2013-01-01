import sys
import xml.etree.ElementTree as ET

class AddonXMLUpdater():

    def __init__(self):
        self.filesystem = sys.modules["__main__"].filesystem

    def UpdateAddonVersion(self, update, xml):
        xml.attrib["version"] = update["plugin"]["new_" + update["branch"] + "_version"]

    def ParseXMLStructure(self, content):
        xml = ET.fromstring(content)
        return xml

    def OutputXMLAsString(self, xml):
        content = ET.tostring(xml, encoding="UTF-8")
        content = content.replace("<?xml version='1.0' encoding='UTF-8'?>", "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>")
        return content

    def UpdateVersionNumberAndDependencyInformationInAddonXml(self, update):
        file = "tmp/" + update["branch"] + "/" + update["plugin"]["name"] + "/Addon.xml"
        if update["branch"] == "default":
            file = file.replace("/Addon.xml","/plugin/Addon.xml")

        print "updating addon manifest xml: " + file
        content = self.filesystem.readFileFromDisk(file)

        if len(content) == 0:
            return

        xml = self.ParseXMLStructure(content)

        self.UpdateAddonVersion(update, xml)
        self.UpdatePluginDependencyInformation(update, xml)

        content = self.OutputXMLAsString(xml)

        self.filesystem.saveFileToDisk(file, content)

    def UpdateDependencyVersion(self, branch, imports, update):
        for dependency in imports:
            if (dependency.attrib["addon"].replace(".beta","") == update["name"]):
                if (update.has_key("new_version")):
                    dependency.attrib["version"] = update["new_version"]
                elif (update.has_key("new_" + branch + "_version")):
                    dependency.attrib["version"] = update["new_" + branch + "_version"]

    def UpdatePluginDependencyInformation(self, plugin_update, xml):
        plugin = plugin_update["plugin"]
        branch = plugin_update["branch"]

        imports = xml.findall("*/import")
        for update in plugin["dependencies"]:
            if not (update.has_key("new_version") or update.has_key("new_" + branch + "_version")):
                continue

            self.UpdateDependencyVersion(branch, imports, update)