import re

from IRepresentation import Program, CodeBlock, CodeLine
from Pipeline.Pass import Pass

TEMP = re.compile(r"^t\d+$")


class DeadCodePass(Pass):
    def __init__(self):
        super().__init__("deadcode")

    def process(self, program: Program) -> Program:
        blocks = [self.process_block(block) for block in program.get_blocks()]
        return Program(blocks)

    def process_block(self, block):
        live = set()
        kept = []

        for line in reversed(block.get_lines()):
            dest = self.defined(line)
            if dest is not None and TEMP.match(dest) and dest not in live:
                continue

            kept.append(line)
            if dest is not None:
                live.discard(dest)
            for value in self.uses(line):
                live.add(value)

        kept.reverse()
        new_block = CodeBlock(block.label)
        for line in kept:
            new_block.add_line(line)
        return new_block

    def defined(self, line):
        if line.type in (CodeLine.ASSIGN, CodeLine.ARRAY_READ):
            return line.operands[0] if line.operands else None
        return None

    def uses(self, line):
        if line.type == CodeLine.ASSIGN:
            return line.operands[1:]
        if line.type == CodeLine.ARRAY_READ:
            return line.operands[2:3]
        if line.type == CodeLine.ARRAY_WRITE:
            return line.operands[1:3]
        if line.type == CodeLine.IF_GOTO:
            return line.operands[0:2]
        if line.type == CodeLine.PRINT:
            return line.operands[0:1]
        return []
