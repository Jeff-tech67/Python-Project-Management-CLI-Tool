from __future__ import annotations

from typing import Optional


class Person:
    

    def __init__(self, name: str, email: Optional[str] = None):
        self.name = name
        self.email = email or ""

    def __repr__(self):
        return f"Person(name={self.name})"
