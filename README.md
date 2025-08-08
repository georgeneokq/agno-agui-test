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

5. I will commit the patched up version - to test that the bug actually happens, look at `main.py` and comment/uncomment lines 4/5 as required.

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

### Each agent emits AG-UI TextMessageEnd event

**Note that the current fix will output all agents' output as is, instead of outputting only the team coordinator's output. This may not always be desired, especially in collaborate mode, and should preferably be made configurable through a configuration/parameter.**

Reception of message stream in CopilotKit ends prematurely when interacting with a Team. This is due to how AGUIApp emits AG-UI completion events even though there are still agents in the team left to process the messages.

The current fix is to separate the completion condition for agents and teams, in `lib/app/agui/utils.py` line 371 - 378.

Added a for_team parameter to function `async_stream_agno_response_as_agui_events` to differentiate between an agent and team run.

**Relevant code:**
```python
# Lifecycle end events to be emitted differs for Agent and Team
is_completion_event = chunk.event == TeamRunEvent.run_completed if for_team else (
    chunk.event == RunEvent.run_completed
    or chunk.event == RunEvent.run_paused
)

# Handle the lifecycle end event
if is_completion_event:
  ...
```

More tweaking is required to improve the formatting, as the output of the subsequent agent starts on the same line as the previous agent.
