import re

from .Program import Program
from .CodeBlock import CodeBlock
from .CodeLine import CodeLine


class Parser:
    PROC = re.compile(r"^proc\s+(\w+)\s*\{$")
    END = re.compile(r"^\}$")
    LABEL = re.compile(r"^(\w+):$")
    IF_GOTO = re.compile(r"^if\s+(\S+)\s+(\S+)\s+(\S+)\s+goto\s+(\w+)$")
    GOTO = re.compile(r"^goto\s+(\w+)$")
    CALL = re.compile(r"^call\s+(\w+)$")
    PRINT = re.compile(r"^print\s+(\S+)$")
    ARRAY_WRITE = re.compile(r"^(\w+)\[(.+)\]\s*=\s*(.+)$")
    ARRAY_READ = re.compile(r"^(\w+)\s*=\s*(\w+)\[(.+)\]$")
    ASSIGN = re.compile(r"^(\w+)\s*=\s*(.+)$")
    OPERATOR = re.compile(r"\s*([+\-*/])\s*")

    @staticmethod
    def parse(file_path):
        with open(file_path, "r") as file:
            return Parser.parse_text(file.read())

    @staticmethod
    def parse_text(text):
        return Program(Parser.split_blocks(Parser.parse_lines(text)))

    @staticmethod
    def parse_lines(text):
        lines = []
        for raw in text.splitlines():
            line = raw.strip()
            if line:
                lines.append(Parser.parse_line(line))
        return lines

    @staticmethod
    def split_blocks(lines):
        blocks = []
        current = CodeBlock()

        def flush():
            nonlocal current
            if current.lines:
                blocks.append(current)
            current = CodeBlock()

        for i, parsed in enumerate(lines):
            if parsed.type in (CodeLine.PROC, CodeLine.LABEL):
                flush()
                current.label = parsed.operands[0]
                current.add_line(parsed)
            elif parsed.type == CodeLine.END:
                current.add_line(parsed)
                flush()
            else:
                current.add_line(parsed)
                if parsed.type == CodeLine.IF_GOTO:
                    next_line = lines[i + 1] if i + 1 < len(lines) else None
                    if not (next_line and next_line.type == CodeLine.GOTO):
                        flush()
                elif parsed.type in (CodeLine.GOTO, CodeLine.CALL):
                    flush()

        flush()
        return blocks

    @staticmethod
    def parse_line(line):
        match = Parser.PROC.match(line)
        if match:
            return CodeLine(line, CodeLine.PROC, [match.group(1)])

        if Parser.END.match(line):
            return CodeLine(line, CodeLine.END)

        match = Parser.LABEL.match(line)
        if match:
            return CodeLine(line, CodeLine.LABEL, [match.group(1)])

        match = Parser.IF_GOTO.match(line)
        if match:
            return CodeLine(
                line,
                CodeLine.IF_GOTO,
                [match.group(1), match.group(3), match.group(4)],
                operator=match.group(2),
            )

        match = Parser.GOTO.match(line)
        if match:
            return CodeLine(line, CodeLine.GOTO, [match.group(1)])

        match = Parser.CALL.match(line)
        if match:
            return CodeLine(line, CodeLine.CALL, [match.group(1)])

        match = Parser.PRINT.match(line)
        if match:
            return CodeLine(line, CodeLine.PRINT, [match.group(1)])

        match = Parser.ARRAY_WRITE.match(line)
        if match:
            return CodeLine(
                line, CodeLine.ARRAY_WRITE, [match.group(1), match.group(2), match.group(3)]
            )

        match = Parser.ARRAY_READ.match(line)
        if match:
            return CodeLine(
                line, CodeLine.ARRAY_READ, [match.group(1), match.group(2), match.group(3)]
            )

        match = Parser.ASSIGN.match(line)
        if match:
            dest = match.group(1)
            parts = [part for part in Parser.OPERATOR.split(match.group(2)) if part]
            if len(parts) == 3:
                return CodeLine(
                    line,
                    CodeLine.ASSIGN,
                    [dest, parts[0], parts[2]],
                    operator=parts[1],
                )
            return CodeLine(line, CodeLine.ASSIGN, [dest] + parts)

        raise ValueError(f"Unrecognized line: {line}")
