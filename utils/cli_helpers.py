from rich.console import Console
from rich.table import Table

console = Console()


def print_users(users):
    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Email")
    for u in users:
        table.add_row(str(u.id), u.name, u.email or "")
    console.print(table)


def print_projects(projects):
    table = Table(title="Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due Date")
    for p in projects:
        owner = p.owner.name if p.owner else ""
        table.add_row(str(p.id), p.title, owner, str(p.due_date) if p.due_date else "")
    console.print(table)


def print_tasks(tasks):
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Assigned")
    table.add_column("Project")
    for t in tasks:
        assigned = t.assigned_to.name if t.assigned_to else ""
        proj = t.project.title if t.project else ""
        table.add_row(str(t.id), t.title, t.status, assigned, proj)
    console.print(table)
