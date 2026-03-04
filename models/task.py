from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .project import Project


class Task:       # This is a Task class which is assignd to a project then to a user
    

    _id_counter = 1
    tasks: List['Task'] = []

    def __init__(self, title: str, assigned_to: Optional[User] = None):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.status = "incomplete"            #initialize the status of the task as incomplete
        self.assigned_to = assigned_to
        self.project: Optional[Project] = None
        Task.tasks.append(self)

    def mark_complete(self):
        self.status = "complete"      # when this method is called the status of the task will be changed to complete

    def to_dict(self): # converting the to dicttionary
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to.id if self.assigned_to else None,
            "project": self.project.id if self.project else None,
        }

    @classmethod  
    def from_dict(cls, data):
        task = cls(data['title'])
        task.id = data['id']
        task.status = data.get('status', 'incomplete')
        return task

    @classmethod
    def find_by_title(cls, title: str) -> Optional['Task']:
        for t in cls.tasks:
            if t.title == title:
                return t
        return None

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, status={self.status})"
