from collections import defaultdict
from typing import *
import lang

def is_valid_identifier(x:str|None) -> bool:
    return x is not None \
       and len(x) > 0 \
       and x[0] in lang.SymbolSet.IDENT_FIRST \
       and x.isalnum()

class TreeSearch:
    resolution:dict
    branchlets:dict[str, set[str]]
    
    def __init__(self):
        self.resolution = dict()
        self.branchlets = defaultdict(set)
    
    def add_to_tree(self, text:str, res_value:Any):
        if text in self.resolution:
            raise IndexError(f"Text {repr(text)} is already in the tree.")
        self.resolution[text] = res_value        
        for i in range(len(text)):
            self.branchlets[text[:i]].add(text[i])

    def lookup(self, text:str):
        return (self.resolution.get(text), self.branchlets[text])




if __name__ == "__main__":
    ts = TreeSearch()
    ts.add_to_tree("pF", "picofarad")
    ts.add_to_tree("uF", "microfarad")
    ts.add_to_tree("pH", "picohenry")
    ts.add_to_tree("abc", "FIRST")
    ts.add_to_tree("def", "SECOND")
    ts.add_to_tree("abcdef", "THIRD")
    
    print(ts.lookup("abc"))
    print(ts.lookup("def"))
    print(ts.lookup("abcd"))
    print(ts.lookup("pF"))
    print(ts.lookup("p"))
#
