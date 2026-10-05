from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Scratchpad:
    notes: list[str] = field(default_factory=list)

    def add(self, note: str) -> None:
        self.notes.append(note.strip())

    def dump(self, *, last: int = 12) -> str:
        return "\n".join(self.notes[-last:])
