from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from angr.knowledge_base.knowledge_base import KnowledgeBase

default_plugins = {}


class KnowledgeBasePlugin:
    def __init__(self, kb: "KnowledgeBase"):
        self._kb = kb

    def copy(self):
        raise NotImplementedError

    @staticmethod
    def register_default(name, cls):
        if name in default_plugins:
            raise Exception(f"{default_plugins[name]} is already set as the default for {name}")
        default_plugins[name] = cls


class KnowledgeViewPlugin(KnowledgeBasePlugin):
    """
    This represents a special kind of knowledge that is "frozen" after initial generation
    Some KB Plugins function like databases/datastores, where any analysis can e.g. add xrefs in addition to just
    looking up existing xrefs

    but for some kinds of knowledge there is a clear "initial generation" phase, after which the knowledge never changes
    e.g. if metadata is parsed from a binary, it is not expected to change after the initial extraction

    This gathering of data shouldn't happen inside the plugin, but be a separate analysis
    This separate analysis can then also internally use KnowledgeBase.request_knowledge on some other KnowledgeViewPlugin
    to get some data that is required for the analysis

    """

    def gather(self):
        raise NotImplementedError()
