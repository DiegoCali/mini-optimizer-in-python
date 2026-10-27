class Program:
    def __init__(self, blocks=None):
        self.blocks = blocks or []

    def add_block(self, block):
        self.blocks.append(block)

    def get_blocks(self):
        return self.blocks

    def __str__(self):
        return "\n\n".join(str(block) for block in self.blocks)

    def __repr__(self):
        return f"Program(blocks={len(self.blocks)})"
