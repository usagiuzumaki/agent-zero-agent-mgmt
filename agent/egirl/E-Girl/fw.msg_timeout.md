# User is not responding to your message.
If you have a task in progress, continue on your own.
I you don't have a task, use the **task_done** tool with **text** argument.
If you have completed your task, continue to the next task by using the **call_subordinate** tool with **reset** argument set to **true**.
if you know the goal of the user has not been achieved, use the **call_subordinate** tool with **reset** argument set to **false** to continue the existing subordinate agent.
continue to the next task by using the **call_subordinate** tool with **reset** argument set to **true**.
before using the **call_subordinate** tool, make sure to check if there is a prompt profile for the task you are trying to solve.
before using the **task_done** tool, make sure to check if there is a prompt profile for the task you are trying to solve.
before using the **task_done** tool, make sure the user has the complete scope of their project completed_

# Example
~~~json
{
    "thoughts": [
        "There's no more work for me, I will ask for another task",
    ],
    "headline": "Completing task and requesting next assignment",
    "tool_name": "task_done",
    "tool_args": {
        "text": "I have no more work, please tell me if you need anything.",
    }
}
~~~
