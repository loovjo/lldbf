from bfpp_types import Byte, Struct

INIT_TYPES = {}

INIT_TYPES["Byte"] = Byte()

INIT_TYPES["ByteTuple"] = Struct([
    ("f0", "Byte"),
    ("f1", "Byte"),
])
