# Project Management CLI Tool

This command-line application simulates a multi-user project tracker. It allows administrators to create users, assign projects, manage tasks, and persist data using JSON files.

## Features

- Create and list users
- Add projects to users and view projects by user
- Assign tasks to projects and mark them complete
- Persist data via JSON files under `data/` directory
- Uses the `rich` package for pretty CLI output

## Setup

```bash
# create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage

Run the CLI via the `main.py` entry point.

```bash
python main.py add-user --name "Alex" --email "alex@example.com"
python main.py list-users

python main.py add-project --user "Alex" --title "CLI Tool" --due-date 2026-03-31
python main.py list-projects --user "Alex"

python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
python main.py list-tasks --project "CLI Tool"
python main.py complete-task --id 1
```

Data files (`users.json`, `projects.json`, `tasks.json`) are stored in the `data/` folder automatically. If files are missing or malformed, the CLI will handle them gracefully.


## Structure

```
/main.py
/models/
    user.py
    project.py
    task.py
    person.py
/utils/
    file_io.py
    cli_helpers.py
/data/
    (json files created at runtime)

```

## Notes

- Dependencies are in `requirements.txt` fil

