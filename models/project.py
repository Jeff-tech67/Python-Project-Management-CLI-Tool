from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class Project:       # This is a project class which is assigned to a user and has some tasks
    

    _id_counter = 1
    projects: List['Project'] = []

    def __init__(self, title: str, description: str = "", due_date: Optional[str] = None):
        self.id = Project._id_counter
        Project._id_counter += 1
        self.title = title
        self.description = description
        # internal storage for due date string
        self._due_date: Optional[str] = None
        if due_date:
            self.due_date = due_date
        self.owner: Optional[User] = None
        self.tasks: List[Task] = []
        Project.projects.append(self)

    def add_task(self, task: Task):
        task.project = self
        self.tasks.append(task)

    @property
    def due_date(self) -> Optional[str]:
        
        return self._due_date

    @due_date.setter
    def due_date(self, value: Optional[str]):
        if value is None:
            self._due_date = None
            return
        try:
            self._due_date = datetime.fromisoformat(value).isoformat()
        except ValueError:
            self._due_date = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner.id if self.owner else None,
            "tasks": [t.id for t in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        proj = cls(data['title'], data.get('description', ''), data.get('due_date', None))
        proj.id = data['id']
        # link owner later
        return proj

    @classmethod
    def find_by_title(cls, title: str) -> Optional['Project']:
        for p in cls.projects:
            if p.title == title:
                return p
        return None

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title})"
