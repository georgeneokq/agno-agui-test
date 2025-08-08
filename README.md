# Agno X CopilotKit test

CopilotKit is a great frontend framework for interacting with agents.

This repository documents the code I have used to test the bugs of Agno's AGUIApp.

## Setup

1. Create a `agents/.env` file from `agents/.env.example`

2. Run the app
```bash
docker compose up -d
```

3. Access CopilotKit app at `http://localhost:3000`

4. Enter "Tesla" into the chat. For testing, I have hardcoded for the tools to support this one value.

5. To reproduce the bugs that I have described fixes for below, look at `agents/src/main.py` and comment/uncomment lines 4/5 as required.

## Fixes

### Team.arun() allows list[str] but not list[Message]

I have found that Team.arun() does not handle list[Message] type. Not sure if I should fix that directly in Agno's Team class, so I have stuck to doing what I can within the AGUIApp confines for now. I have converted the list[Message] to a list[str] by extracting out the "content" property of each Agno Message.

**Traceback:**

```
Error running team: sequence item 0: expected str instance, Message found
Traceback (most recent call last):
  File "/app/agents/src/lib/app/agui/async_router.py", line 63, in run_team
    response_stream = await team.arun(
                      ^^^^^^^^^^^^^^^^
    ...<4 lines>...
    )
    ^
  File "/app/.venv/lib/python3.13/site-packages/agno/team/team.py", line 1342, in arun
    run_messages = self.get_run_messages(
        session_id=session_id,
    ...<7 lines>...
        **kwargs,
    )
  File "/app/.venv/lib/python3.13/site-packages/agno/team/team.py", line 5570, in get_run_messages
    user_message = self._get_user_message(
        message,
    ...<6 lines>...
        **kwargs,
    )
  File "/app/.venv/lib/python3.13/site-packages/agno/team/team.py", line 5648, in _get_user_message
    user_message_content = "\n".join(message)
TypeError: sequence item 0: expected str instance, Message found
```

### Each agent emits AG-UI RunFinishedEvent

Reception of message stream in CopilotKit ends prematurely when interacting with a Team. This is due to how AGUIApp emits AG-UI completion events even though there are still agents in the team left to process the messages.

First part of the fix can be found in `app/agui/utils.py`, `async_stream_agno_response_as_agui_events` function.
Reset the message_started flag to False when an agent finishes its response, which ensures that the next agent will
emit a new TextMessageStartedEvent.

```python
async for chunk in response_stream:
    # Handle the lifecycle end event
    if (
        chunk.event == TeamRunEvent.run_completed
        or chunk.event == RunEvent.run_completed
        or chunk.event == RunEvent.run_paused
    ):
        completion_events = _create_completion_events(
            chunk, event_buffer, message_started, message_id
        )

        # Reset to false to ensure next team member emits a new TextMessageStartEvent
        message_started = False

        ...
```

Second part of the fix is in `app/agui/utils.py`, `_create_completion_events` and `stream_agno_response_as_agui_events` (including async ver.) function,
and also the `run_agent` and `run_team` functions of both `app/agui/sync_router.py` and `app/agui/async_router.py`.
Instead of emitting the RunFinishedEvent from `stream_agno_response_as_agui_events` (including async ver.), we shift it into `run_agent`/`run_team` as that is where we know for sure where the run for that agent/team ends.
