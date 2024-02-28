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
