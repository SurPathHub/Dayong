"""
dayong.tasks.manager
~~~~~~~~~~~~~~~~~~~~

Task managers for coroutines.
"""
import asyncio
from asyncio.tasks import Task
from typing import Any, Callable, Coroutine


class TaskManager:
    """Generic coroutine task manager and scheduler."""

    tasks: dict[str, Task[Any]] = {}

    def get_task(self, task_name: str) -> Task[Any]:
        """Fetch the task object for a specified task.

        Args:
            task_id (int): The name assigned to the task object to retrieve.

        Returns:
            Task[Any]: A coroutine wrapped in a Future.
        """
        return self.tasks[task_name]

    async def start_task(
        self,
        coro_fn: Callable[..., Coroutine[Any, Any, Any]],
        task_name: str,
        execute_in: float,
        *coro_args: Any,
    ) -> tuple[str, Task[Any]]:
        """Schedule the execution of a coroutine.

        Args:
            coro_fn (Callable[..., Coroutine[Any, Any, Any]]): The coroutine to execute.
            task_name (str): The name of the task to execute.
            execute_in (float): The execution time delay.

        Returns:
            tuple[str, Task[Any]]: The task name and `asyncio.Task` object.
        """
        if task_name in self.tasks:
            raise RuntimeError

        async def wrapped_coro():
            try:
                await asyncio.sleep(execute_in)
                return await coro_fn(*coro_args)
            finally:
                del self.tasks[task_name]

        loop = asyncio.get_running_loop()
        task = loop.create_task(wrapped_coro(), name=task_name)
        self.tasks[task.get_name()] = task

        return task_name, task

    def stop_task(self, task_name: str):
        """Stop a task running in the background.

        Args:
            task_id (int): Integer associated with a task object.
        """
        task = self.get_task(task_name)
        task.cancel()
