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
- Configure the `ENVIRON_TYPE` env var: Eg. `ENVIRON_TYPE=DEV`
- Configure the `DEV__SECRET` env var to be used by the JWT Auth Handler var: Eg. `DEV__SECRET=<YOUR SECRET>`
- Configure the `SLACK_API_TOKEN` env var to be used when you wil send messages to the slack
- To run the api call `python app.py`


## How to implement new Notification Handlers
- You need to implement a new class following the `NotificationSender` Protocol
- You need to implement a new class following the `NotificationFactory` Protocol that knows to build the new class above.
- In the app.py you need to add your `factory`: Eg. 
```python
factory_caller.add_factory(SlackNotificationFactory(slack_token=SETTINGS.get("SLACK_API_TOKEN", ""))
)
```

## How Send messages to the slack
- Send a request `POST /notification` with following payload:
```json
{
	"data": {
		"title": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
		"content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum",
		"icon": ":partying_face:",
		"destin": [
			{
				"type": "slack_channel",
				"target": "tech_logs"
			}
		]
	}
}
```


