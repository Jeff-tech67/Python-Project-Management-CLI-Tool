from __future__ import annotations

import json
from typing import List, Optional, TYPE_CHECKING

from .person import Person

if TYPE_CHECKING:
    from .project import Project


class User(Person):
   

    _id_counter = 1
    users: List['User'] = []  # class-level collection

    def __init__(self, name: str, email: Optional[str] = None):
        super().__init__(name, email)
        self.id = User._id_counter
        User._id_counter += 1
        self.projects: List[Project] = []
        User.users.append(self)

    def add_project(self, project: Project):
        project.owner = self
        self.projects.append(project)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [p.id for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['name'], data.get('email'))
        user.id = data['id']
        # projects will be linked after projects are loaded
        return user

    @classmethod
    def find_by_name(cls, name: str) -> Optional['User']:
        for u in cls.users:
            if u.name == name:
                return u
        return None

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"
