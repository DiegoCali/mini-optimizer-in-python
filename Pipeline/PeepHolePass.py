from IRepresentation import Program, Parser, CodeLine
from Pipeline.Pass import Pass


class PeepHolePass(Pass):
    def __init__(self):
        super().__init__("peephole")

    def process(self, program: Program) -> Program:
        lines = self.flatten(program)
        optimized = self.apply_rules(lines)
        optimized = self.merge_consecutive_labels(optimized)
        optimized = self.remove_fallthrough_gotos(optimized)
        optimized = self.remove_unreferenced_labels(optimized)
        return Program(Parser.split_blocks(optimized))

    def flatten(self, program):
        lines = []
        for block in program.get_blocks():
            lines.extend(block.get_lines())
        return lines

    def apply_rules(self, lines):
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]

            rewritten = self.algebraic(line)
            if rewritten is False:
                i += 1
                continue
            if rewritten is not None:
                result.append(rewritten)
                i += 1
                continue

            next_line = lines[i + 1] if i + 1 < len(lines) else None
            if self.redundant_self(line):
                i += 1
                continue
            if self.redundant_swap(line, next_line):
                result.append(line)
                i += 2
                continue

            after_next = lines[i + 2] if i + 2 < len(lines) else None
            if self.flow_drop_goto(line, next_line, after_next):
                result.append(line)
                i += 2
                continue

            redirected = self.flow_redirect_if_goto(lines, i)
            if redirected is not None:
                result.append(redirected)
                i += 1
                continue

            result.append(line)
            i += 1

        return result

    def algebraic(self, line):
        if (
            line.type != CodeLine.ASSIGN
            or len(line.operands) != 3
            or line.operator not in ("+", "-", "*", "/")
        ):
            return None

        dest, left, right = line.operands
        identity = "0" if line.operator in ("+", "-") else "1"
        if right != identity:
            return None

        if left == dest:
            return False
        return self.assign(dest, left)

    def redundant_self(self, line):
        return (
            line.type == CodeLine.ASSIGN
            and line.operator is None
            and len(line.operands) == 2
            and line.operands[0] == line.operands[1]
        )

    def redundant_swap(self, line, next_line):
        if not self.is_plain_assign(line):
            return False
        if next_line is None or not self.is_plain_assign(next_line):
            return False
        return (
            line.operands[0] == next_line.operands[1]
            and line.operands[1] == next_line.operands[0]
        )

    def flow_drop_goto(self, line, next_line, after_next):
        if line.type != CodeLine.IF_GOTO or next_line is None or after_next is None:
            return False
        if next_line.type != CodeLine.GOTO or after_next.type != CodeLine.LABEL:
            return False
        return next_line.operands[0] == after_next.operands[0]

    def flow_redirect_if_goto(self, lines, index):
        line = lines[index]
        if line.type != CodeLine.IF_GOTO:
            return None

        target = line.operands[2]
        label_index = index + 1
        while label_index < len(lines) and lines[label_index].type != CodeLine.LABEL:
            label_index += 1

        if label_index >= len(lines) or lines[label_index].operands[0] != target:
            return None

        goto_index = label_index + 1
        if goto_index >= len(lines) or lines[goto_index].type != CodeLine.GOTO:
            return None

        new_target = lines[goto_index].operands[0]
        left, right = line.operands[0], line.operands[1]
        raw = f"if {left} {line.operator} {right} goto {new_target}"
        return CodeLine(
            raw, CodeLine.IF_GOTO, [left, right, new_target], operator=line.operator
        )

    def merge_consecutive_labels(self, lines):
        aliases = {}
        result = []
        pending_labels = []

        for line in lines:
            if line.type == CodeLine.LABEL:
                pending_labels.append(line.operands[0])
                continue

            if pending_labels:
                canonical = pending_labels[0]
                for label in pending_labels[1:]:
                    aliases[label] = canonical
                result.append(CodeLine(f"{canonical}:", CodeLine.LABEL, [canonical]))
                pending_labels = []
            result.append(line)

        if pending_labels:
            canonical = pending_labels[0]
            for label in pending_labels[1:]:
                aliases[label] = canonical
            result.append(CodeLine(f"{canonical}:", CodeLine.LABEL, [canonical]))

        if not aliases:
            return result

        return [self.redirect_label(line, aliases) for line in result]

    def redirect_label(self, line, aliases):
        if line.type == CodeLine.GOTO:
            target = aliases.get(line.operands[0], line.operands[0])
            if target == line.operands[0]:
                return line
            return CodeLine(f"goto {target}", CodeLine.GOTO, [target])

        if line.type == CodeLine.IF_GOTO:
            left, right, target = line.operands
            new_target = aliases.get(target, target)
            if new_target == target:
                return line
            raw = f"if {left} {line.operator} {right} goto {new_target}"
            return CodeLine(
                raw,
                CodeLine.IF_GOTO,
                [left, right, new_target],
                operator=line.operator,
            )

        return line

    def remove_fallthrough_gotos(self, lines):
        result = []
        for index, line in enumerate(lines):
            next_line = lines[index + 1] if index + 1 < len(lines) else None
            if (
                line.type == CodeLine.GOTO
                and next_line is not None
                and next_line.type == CodeLine.LABEL
                and line.operands[0] == next_line.operands[0]
            ):
                continue
            result.append(line)
        return result

    def remove_unreferenced_labels(self, lines):
        referenced = set()
        for line in lines:
            if line.type == CodeLine.GOTO:
                referenced.add(line.operands[0])
            elif line.type == CodeLine.IF_GOTO:
                referenced.add(line.operands[2])
        return [
            line
            for line in lines
            if line.type != CodeLine.LABEL or line.operands[0] in referenced
        ]

    def assign(self, dest, src):
        return CodeLine(f"{dest} = {src}", CodeLine.ASSIGN, [dest, src])

    def is_plain_assign(self, line):
        return (
            line is not None
            and line.type == CodeLine.ASSIGN
            and line.operator is None
            and len(line.operands) == 2
        )
