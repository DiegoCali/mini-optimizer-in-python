from IRepresentation import Parser
from Pipeline import (
    PeepHolePass,
    PropagationPass,
    SubExpressionPass,
    DeadCodePass,
)

PASSES = [
    PeepHolePass(),
    PropagationPass(),
    SubExpressionPass(),
    DeadCodePass(),
]

MAX_ITERATIONS = 10
OUTPUT_PATH = "optimized.tac"


def count_lines(program):
    return sum(len(block.get_lines()) for block in program.get_blocks())


program = Parser.parse("code.tac")
original_lines = count_lines(program)

for iteration in range(1, MAX_ITERATIONS + 1):
    snapshot = str(program)
    for current_pass in PASSES:
        program = current_pass.process(program)
    if str(program) == snapshot:
        break

final_lines = count_lines(program)
removed = original_lines - final_lines
percentage = (removed / original_lines * 100) if original_lines else 0.0

print(str(program))
print()
print(f"Iteraciones: {iteration}")
print(f"Líneas: {original_lines} -> {final_lines}")
print(f"Optimización: {percentage:.2f}% (eliminadas {removed})")

with open(OUTPUT_PATH, "w") as output:
    output.write(str(program) + "\n")
