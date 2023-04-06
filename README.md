# System Notification
A service designed as an MVP to validate the notification system.

## About commit messages
This project follow [the conventional commit](https://www.conventionalcommits.org/en/v1.0.0/)
Make sure follow this convention.

## How to run this project
- Install poetry following this instructions https://python-poetry.org/docs/#installation
- Clone this project
- Inside the project directory run this commands in your shell:
    - `pre-commit install`
    - `pre-commit install --hook-type commit-msg --hook-type pre-push`
- Execute the `poetry shell` inside the project
- Install the project dependencies by calling `poetry install`
- To run the api call `python app.py`