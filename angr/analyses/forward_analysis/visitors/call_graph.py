from ...cfg.cfg_utils import CFGUtils
from .graph import GraphVisitor


class CallGraphVisitor(GraphVisitor):
    """
    :param networkx.DiGraph callgraph:
    """
    def __init__(self, callgraph):
        super(CallGraphVisitor, self).__init__()
        self.callgraph = callgraph

        self.reset()

    def startpoints(self):
        # TODO: make sure all connected components are covered
        start_nodes = [node for node in self.callgraph.nodes() if self.callgraph.in_degree(node) == 0]

        if not start_nodes:
            # randomly pick one
            start_nodes = [ self.callgraph.nodes()[0] ]

        return start_nodes

    def successors(self, node):
        return list(self.callgraph.successors(node))

    def predecessors(self, node):
        return list(self.callgraph.predecessors(node))

    def sort_nodes(self, nodes=None):
        sorted_nodes = CFGUtils.quasi_topological_sort_nodes(self.callgraph)

        if nodes is not None:
            sorted_nodes = [ n for n in sorted_nodes if n in set(nodes) ]

        return sorted_nodes
