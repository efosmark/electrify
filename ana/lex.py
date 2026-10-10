import lang

class Define:
    def __init__(self, /, *args):
        ...

comment = Define(lang.COMMENT_START, ..., lang.COMMENT_STOP)

identifier = Define(lang.SymbolSet.IDENT_FIRST, lang.SymbolSet.IDENT_BODY, anything(),  not_in(lang.SymbolSet.IDENT_BODY))

class Not:
    ...

class Rule:
    ...

class Anything:
    ...
    