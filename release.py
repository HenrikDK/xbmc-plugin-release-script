from AddonXMLUpdater import AddonXMLUpdater
from DependencyManager import DependencyManager
from EmailTemplate import EmailTemplate
from FileSystem import FileSystem
from PluginManager import PluginManager
from ReleaseManager import ReleaseManager
from RepositoryManager import RepositoryManager
from VersionManager import VersionManager

filesystem = ""
repository = ""
addonxmlupdater = ""
pluginmanager = ""
versionmanager = ""
dependencymanager = ""
template = ""

if __name__ == "__main__":
    # make and clean tmp dir

    filesystem = FileSystem()
    addonxmlupdater = AddonXMLUpdater()
    repository = RepositoryManager()
    template = EmailTemplate()
    versionmanager = VersionManager()
    dependencymanager = DependencyManager()
    pluginmanager = PluginManager()

    manager = ReleaseManager()
    manager.updatePluginsAsNecessary()