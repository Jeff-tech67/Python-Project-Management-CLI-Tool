import argparse
import sys

from utils.file_io import load_all, save_all
from models.user import User
from models.project import Project
from models.task import Task
from utils.cli_helpers import print_users, print_projects, print_tasks


def main():
    parser = argparse.ArgumentParser(description="Project management CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    # user commands
    add_user = subparsers.add_parser("add-user", help="Create a new user")
    add_user.add_argument("--name", required=True)
    add_user.add_argument("--email", required=False)

    list_users = subparsers.add_parser("list-users", help="List all users")

    # project commands
    add_proj = subparsers.add_parser("add-project", help="Add project to a user")
    add_proj.add_argument("--user", required=True, help="Owner name")
    add_proj.add_argument("--title", required=True)
    add_proj.add_argument("--description", default="")
    add_proj.add_argument("--due-date", dest="due_date", help="ISO date string")

    list_proj = subparsers.add_parser("list-projects", help="List projects")
    list_proj.add_argument("--user", help="Filter by user name")

    # task commands
    add_task = subparsers.add_parser("add-task", help="Add task to a project")
    add_task.add_argument("--project", required=True)
    add_task.add_argument("--title", required=True)
    add_task.add_argument("--assigned-to", dest="assigned_to", help="User name")

    list_task = subparsers.add_parser("list-tasks", help="List tasks")
    list_task.add_argument("--project", help="Filter by project title")
    list_task.add_argument("--user", help="Filter by assigned user")

    complete = subparsers.add_parser("complete-task", help="Mark a task complete")
    complete.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    load_all()

    if args.command == "add-user":
        if User.find_by_name(args.name):
            print(f"User {args.name} already exists")
            sys.exit(1)
        User(args.name, args.email)
        save_all()
        print(f"Added user {args.name}")

    elif args.command == "list-users":
        print_users(User.users)

    elif args.command == "add-project":
        user = User.find_by_name(args.user)
        if not user:
            print(f"User {args.user} not found")
            sys.exit(1)
        if Project.find_by_title(args.title):
            print(f"Project {args.title} already exists")
            sys.exit(1)
        proj = Project(args.title, args.description, args.due_date)
        user.add_project(proj)
        save_all()
        print(f"Added project {args.title} to user {user.name}")

    elif args.command == "list-projects":
        projs = Project.projects
        if args.user:
            user = User.find_by_name(args.user)
            projs = user.projects if user else []
        print_projects(projs)

    elif args.command == "add-task":
        proj = Project.find_by_title(args.project)
        if not proj:
            print(f"Project {args.project} not found")
            sys.exit(1)
        assigned = None
        if args.assigned_to:
            assigned = User.find_by_name(args.assigned_to)
            if not assigned:
                print(f"User {args.assigned_to} not found")
                sys.exit(1)
        if Task.find_by_title(args.title):
            print(f"Task {args.title} already exists")
            sys.exit(1)
        task = Task(args.title, assigned)
        proj.add_task(task)
        save_all()
        print(f"Added task {args.title} to project {proj.title}")

    elif args.command == "list-tasks":
        tasks = Task.tasks
        if args.project:
            proj = Project.find_by_title(args.project)
            tasks = proj.tasks if proj else []
        if args.user:
            tasks = [t for t in tasks if t.assigned_to and t.assigned_to.name == args.user]
        print_tasks(tasks)

    elif args.command == "complete-task":
        task = next((t for t in Task.tasks if t.id == args.id), None)
        if not task:
            print(f"Task id {args.id} not found")
            sys.exit(1)
        task.mark_complete()
        save_all()
        print(f"Task {task.title} marked complete")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
