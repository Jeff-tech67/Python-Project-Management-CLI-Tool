import json
import os
from typing import Any, Dict, List

from models.user import User
from models.project import Project
from models.task import Task

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _ensure_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_all():
    """Persist users, projects, and tasks to JSON files."""
    _ensure_dir()
    users_data = [u.to_dict() for u in User.users]
    projects_data = [p.to_dict() for p in Project.projects]
    tasks_data = [t.to_dict() for t in Task.tasks]

    with open(os.path.join(DATA_DIR, "users.json"), "w") as f:
        json.dump(users_data, f, indent=2)
    with open(os.path.join(DATA_DIR, "projects.json"), "w") as f:
        json.dump(projects_data, f, indent=2)
    with open(os.path.join(DATA_DIR, "tasks.json"), "w") as f:
        json.dump(tasks_data, f, indent=2)


def load_all():
    """Load objects from disk, reconstruct relationships."""
    _ensure_dir()
    # clear existing
    User.users.clear()
    Project.projects.clear()
    Task.tasks.clear()

    user_map = {}
    project_map = {}

    try:
        with open(os.path.join(DATA_DIR, "users.json")) as f:
            raw = json.load(f)
            for u in raw:
                user = User.from_dict(u)
                user_map[user.id] = user
    except FileNotFoundError:
        pass

    try:
        with open(os.path.join(DATA_DIR, "projects.json")) as f:
            raw = json.load(f)
            for p in raw:
                proj = Project.from_dict(p)
                project_map[proj.id] = proj
                owner_id = p.get("owner")
                if owner_id:
                    owner = user_map.get(owner_id)
                    if owner:
                        owner.add_project(proj)
    except FileNotFoundError:
        pass

    try:
        with open(os.path.join(DATA_DIR, "tasks.json")) as f:
            raw = json.load(f)
            for t in raw:
                task = Task.from_dict(t)
                assigned_id = t.get("assigned_to")
                if assigned_id:
                    task.assigned_to = user_map.get(assigned_id)
                proj_id = t.get("project")
                if proj_id:
                    proj = project_map.get(proj_id)
                    if proj:
                        proj.add_task(task)
    except FileNotFoundError:
        pass
