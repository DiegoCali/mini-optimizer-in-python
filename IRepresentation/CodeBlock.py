class CodeBlock:
    def __init__(self, label=None):
        self.label = label
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def get_lines(self):
        return self.lines

    def __str__(self):
        return "\n".join(str(line) for line in self.lines)

    def __repr__(self):
        return f"CodeBlock(label={self.label!r}, lines={len(self.lines)})"
