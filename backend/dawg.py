# Modified version of https://gist.github.com/smhanov/94230b422c2100ae4218
# coding:utf-8

import json
from collections import OrderedDict

class DawgNode(object):
    NextId = 0
    
    def __init__(self):
        self.id = DawgNode.NextId
        DawgNode.NextId += 1
        self.final = False
        self.edges = OrderedDict()
 
        # Number of end nodes reachable from this one.
        self.count = 0
 
    def __unicode__(self):        
        arr = []
        if self.final: 
            arr.append("1")
        else:
            arr.append("0")
 
        for (label, node) in self.edges.items():
            arr.append( label )
            arr.append( str( node.id ) )
 
        return "_".join(arr)
 
    def __hash__(self):
        return self.__str__().__hash__()
 
    def __eq__(self, other):
        return self.__str__() == other.__str__()
 
    def numReachable(self):
        # if a count is already assigned, return it
        if self.count: return self.count
 
        # count the number of final nodes that are reachable from this one.
        # including self
        count = 0
        if self.final: count += 1
        for label, node in self.edges.items():
            count += node.numReachable()
 
        self.count = count
        return count
 
class Dawg(object):
    def __init__(self, skip_ok=False):
        self.previousWord = ""
        self.root = DawgNode()
 
        # Here is a list of nodes that have not been checked for duplication.
        self.uncheckedNodes = []
 
        # Here is a list of unique nodes that have been checked for
        # duplication.
        self.minimizedNodes = {}
 
        # Here is the data associated with all the nodes
        self.data = []

    def insert( self, word, data ):
        # find common prefix between word and previous word
        commonPrefix = 0
        for i in range( min( len( word ), len( self.previousWord ) ) ):
            if word[i] != self.previousWord[i]: break
            commonPrefix += 1
 
        # Check the uncheckedNodes for redundant nodes, proceeding from last
        # one down to the common prefix size. Then truncate the list at that
        # point.
        self._minimize( commonPrefix )
 
        self.data.append(data)
 
        # add the suffix, starting from the correct node mid-way through the
        # graph
        if len(self.uncheckedNodes) == 0:
            node = self.root
        else:
            node = self.uncheckedNodes[-1][2]
 
        for letter in word[commonPrefix:]:
            nextNode = DawgNode()
            node.edges[letter] = nextNode
            self.uncheckedNodes.append( (node, letter, nextNode) )
            node = nextNode
 
        node.final = True
        self.previousWord = word
 
    def finish( self ):
        # minimize all uncheckedNodes
        self._minimize( 0 );
 
        # go through entire structure and assign the counts to each node.
        self.root.numReachable()
 
    def _minimize( self, downTo ):
        # proceed from the leaf up to a certain point
        for i in range( len(self.uncheckedNodes) - 1, downTo - 1, -1 ):
            (parent, letter, child) = self.uncheckedNodes[i];
            if child in self.minimizedNodes:
                # replace the child with the previously encountered one
                parent.edges[letter] = self.minimizedNodes[child]
            else:
                # add the state to the minimized nodes.
                self.minimizedNodes[child] = child;
            self.uncheckedNodes.pop()
 
    def lookup( self, word ):
        node = self.root
        skipped = 0 # keep track of number of final nodes that we skipped
        for letter in word:
            if letter not in node.edges:
                return None
            for label, child in node.edges.items():
                if label == letter: 
                    if node.final: skipped += 1
                    node = child
                    break
                skipped += child.count
 
        if node.final:
            return self.data[skipped]

    def nodeCount( self ):
        return len(self.minimizedNodes)
 
    def edgeCount( self ):
        count = 0
        for node in self.minimizedNodes:
            count += len(node.edges)
        return count
