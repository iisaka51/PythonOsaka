from typing import List
from rich.console import Console, OverflowMethod

console = Console(width=14)
supercali = "Beautiful_is_better_than_ugly."

overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
for overflow in overflow_methods:
    console.rule(overflow)
    console.print(supercali, overflow=overflow, style="bold blue")
    console.print()
