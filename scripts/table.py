from typing import *
from electrify.value import format_value

class Column(NamedTuple):
    field:str
    name:str
    width:int
    format:Callable = format_value

class Table:
    cols:Final[Sequence[Column]]
    rows:list[dict[str,Any]]
    td_sep:str
    th_sep:str
    
    def __init__(self, cols:Sequence[Column], td_sep=' | ', th_sep='-'):
        self.cols = cols
        self.rows = []
        self.td_sep = td_sep
        self.th_sep = th_sep
    
    def add_row(self, row:dict[str,Any]):
        self.rows.append(row)
    
    def values(self, field_name:str) -> list[Any]:
        return [ r[field_name] for r in self.rows ]
    
    def print_heading(self):
        print(self.td_sep, end='')
        for col in self.cols:
            print(f'{col.name: >{col.width}}', end=self.td_sep)
        print()
        
        print(self.td_sep, end='')
        for col in self.cols:
            print((self.th_sep * col.width), end=self.td_sep)
        print()
    
    def print_rows(self):
        for row in self.rows:
            print(self.td_sep, end='')
            for col in self.cols:
                disp = col.format(row[col.field])
                print(f'{disp: >{col.width}}', end=self.td_sep)
            print()
