from IRepresentation import Program, CodeBlock, CodeLine
from Pipeline.Pass import Pass


class PropagationPass(Pass):
    def __init__(self):
        super().__init__("propagation")

    def process(self, program: Program) -> Program:
        blocks = [self.process_block(block) for block in program.get_blocks()]
        return Program(blocks)

    def process_block(self, block):
        defs = {}
        new_block = CodeBlock(block.label)
        for line in block.get_lines():
            new_line = self.propagate(line, defs)
            new_block.add_line(new_line)
            self.update_defs(new_line, defs)
        return new_block

    def propagate(self, line, defs):
        if (
            line.type == CodeLine.ASSIGN
            and line.operator is None
            and len(line.operands) == 2
        ):
            dest, src = line.operands
            if src in defs:
                operands, operator = defs[src]
                left, right = operands
                raw = f"{dest} = {left} {operator} {right}"
                return CodeLine(
                    raw, CodeLine.ASSIGN, [dest, left, right], operator=operator
                )
        return line

    def update_defs(self, line, defs):
        if line.type == CodeLine.CALL:
            defs.clear()
            return

        if line.type != CodeLine.ASSIGN or not line.operands:
            return

        dest = line.operands[0]
        for name in list(defs):
            operands, _ = defs[name]
            if dest in operands:
                del defs[name]
        defs.pop(dest, None)

        if line.operator is not None and len(line.operands) == 3:
            left, right = line.operands[1], line.operands[2]
            if dest not in (left, right):
                defs[dest] = ([left, right], line.operator)
