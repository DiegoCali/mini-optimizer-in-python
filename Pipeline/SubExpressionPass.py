from IRepresentation import Program, CodeBlock, CodeLine
from Pipeline.Pass import Pass


class SubExpressionPass(Pass):
    def __init__(self):
        super().__init__("subexpression")

    def process(self, program: Program) -> Program:
        blocks = [self.process_block(block) for block in program.get_blocks()]
        return Program(blocks)

    def process_block(self, block):
        expr_map = {}
        aliases = {}
        new_block = CodeBlock(block.label)

        for line in block.get_lines():
            new_line = self.apply_aliases(line, aliases)
            self.invalidate(line, expr_map, aliases)
            new_block.add_line(new_line)
            self.register(line, new_line, expr_map, aliases)

        return new_block

    def invalidate(self, line, expr_map, aliases):
        if line.type == CodeLine.CALL:
            expr_map.clear()
            aliases.clear()
            return

        if line.type not in (CodeLine.ASSIGN, CodeLine.ARRAY_READ):
            return
        if not line.operands:
            return

        dest = line.operands[0]
        for key in list(expr_map):
            _, left, right = key
            if dest in (left, right) or expr_map[key] == dest:
                del expr_map[key]

        for var in list(aliases):
            if var == dest or aliases[var] == dest:
                del aliases[var]

    def apply_aliases(self, line, aliases):
        if not aliases:
            return line

        if line.type == CodeLine.ASSIGN:
            return self.apply_aliases_assign(line, aliases)

        if line.type == CodeLine.ARRAY_WRITE:
            name, index, value = line.operands
            new_index = aliases.get(index, index)
            new_value = aliases.get(value, value)
            if new_index == index and new_value == value:
                return line
            raw = f"{name}[{new_index}] = {new_value}"
            return CodeLine(
                raw, CodeLine.ARRAY_WRITE, [name, new_index, new_value]
            )

        if line.type == CodeLine.ARRAY_READ:
            dest, name, index = line.operands
            new_index = aliases.get(index, index)
            if new_index == index:
                return line
            raw = f"{dest} = {name}[{new_index}]"
            return CodeLine(raw, CodeLine.ARRAY_READ, [dest, name, new_index])

        if line.type == CodeLine.IF_GOTO:
            left, right, target = line.operands
            new_left = aliases.get(left, left)
            new_right = aliases.get(right, right)
            if new_left == left and new_right == right:
                return line
            raw = f"if {new_left} {line.operator} {new_right} goto {target}"
            return CodeLine(
                raw,
                CodeLine.IF_GOTO,
                [new_left, new_right, target],
                operator=line.operator,
            )

        if line.type == CodeLine.PRINT:
            value = line.operands[0]
            new_value = aliases.get(value, value)
            if new_value == value:
                return line
            return CodeLine(f"print {new_value}", CodeLine.PRINT, [new_value])

        return line

    def apply_aliases_assign(self, line, aliases):
        operands = line.operands

        if line.operator is not None and len(operands) == 3:
            dest, left, right = operands
            new_left = aliases.get(left, left)
            new_right = aliases.get(right, right)
            if new_left == left and new_right == right:
                return line
            raw = f"{dest} = {new_left} {line.operator} {new_right}"
            return CodeLine(
                raw, CodeLine.ASSIGN, [dest, new_left, new_right], operator=line.operator
            )

        if line.operator is None and len(operands) == 2:
            dest, src = operands
            new_src = aliases.get(src, src)
            if new_src == src:
                return line
            raw = f"{dest} = {new_src}"
            return CodeLine(raw, CodeLine.ASSIGN, [dest, new_src])

        return line

    def register(self, line, new_line, expr_map, aliases):
        if new_line.type != CodeLine.ASSIGN:
            return

        operands = new_line.operands

        if new_line.operator is not None and len(operands) == 3:
            dest, left, right = operands
            if dest in (left, right):
                return
            key = (new_line.operator, left, right)
            if key in expr_map:
                aliases[dest] = expr_map[key]
            else:
                expr_map[key] = dest
            return

        if line.operator is None and len(line.operands) == 2:
            dest, src = line.operands
            if src in aliases:
                aliases[dest] = aliases[src]
