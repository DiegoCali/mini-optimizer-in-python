class CodeLine:
    PROC = "PROC"
    END = "END"
    LABEL = "LABEL"
    GOTO = "GOTO"
    IF_GOTO = "IF_GOTO"
    CALL = "CALL"
    PRINT = "PRINT"
    ARRAY_WRITE = "ARRAY_WRITE"
    ARRAY_READ = "ARRAY_READ"
    ASSIGN = "ASSIGN"

    MAX_OPERANDS = 3

    def __init__(self, raw, type, operands=None, operator=None):
        self.raw = raw
        self.type = type
        self.operands = operands or []
        self.operator = operator
        self.validate()

    def validate(self):
        if len(self.operands) > self.MAX_OPERANDS:
            raise ValueError(
                f"Too many operands ({len(self.operands)}): {self.raw}"
            )

    def get_operands(self):
        return self.operands

    def __str__(self):
        return self.raw

    def __repr__(self):
        return (
            f"CodeLine(type={self.type!r}, raw={self.raw!r}, "
            f"operator={self.operator!r}, operands={self.operands!r})"
        )
