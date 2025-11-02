from enum import IntEnum


class CrudEnum(IntEnum):
    CREATE = 1
    READ = 2
    UPDATE = 3
    EDIT = UPDATE
    DELETE = 4
