from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    title: str
    category: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    is_recurring: bool = False
    is_complete: bool = False
    time: str = "08:00"
    recurrence: Optional[str] = None

    def get_priority_score(self) -> int:
        """Return a numeric score for sorting tasks by priority."""
        priority_scores = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
        }
        return priority_scores[self.priority]

    def mark_complete(self, pet: Optional[Pet] = None) -> Optional["Task"]:
        """Mark the task as completed and create the next occurrence when it recurs."""
        self.is_complete = True
        if self.is_recurring and self.recurrence in {"daily", "weekly"} and pet is not None:
            next_task = Task(
                title=self.title,
                category=self.category,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                is_recurring=True,
                recurrence=self.recurrence,
                time=self.time,
            )
            pet.add_task(next_task)
            return next_task
        return None


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's care list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return the pet's current list of tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_start: str = "08:00"
    available_end: str = "20:00"
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to this owner."""
        self.pets.append(pet)

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the owner's preference list."""
        self.preferences = preferences


@dataclass
class TimeBlock:
    start_time: str
    end_time: str
    task: Optional[Task] = None

    def is_available(self) -> bool:
        """Return True when the time block has no assigned task."""
        return self.task is None


@dataclass
class Schedule:
    date: str
    time_blocks: List[TimeBlock] = field(default_factory=list)

    def add_task(self, task: Task, start_time: str) -> None:
        """Add a task to the schedule at the provided start time."""
        start_dt = self._parse_time(start_time)
        end_dt = start_dt + timedelta(minutes=task.duration_minutes)
        self.time_blocks.append(
            TimeBlock(
                start_time=start_time,
                end_time=end_dt.strftime("%H:%M"),
                task=task,
            )
        )

    @staticmethod
    def _parse_time(value: str) -> datetime:
        return datetime.strptime(value, "%H:%M")

    def summarize(self) -> str:
        """Return a short summary of the schedule."""
        return f"Schedule for {self.date} with {len(self.time_blocks)} task block(s)."


@dataclass
class Scheduler:
    def build_daily_plan(self, owner: Owner, pet: Pet, tasks: List[Task]) -> Schedule:
        """Build a simple daily plan for the pet within the owner's available window."""
        task_pool = tasks if tasks else pet.get_tasks()
        sorted_tasks = self.sort_tasks(task_pool)
        available_minutes = self._minutes_between(owner.available_start, owner.available_end)
        feasible_tasks = self.filter_by_time(sorted_tasks, available_minutes)

        schedule = Schedule(date="today")
        current_time = owner.available_start
        remaining_minutes = available_minutes

        for task in feasible_tasks:
            if task.duration_minutes > remaining_minutes:
                continue

            schedule.add_task(task, current_time)
            current_time = self._advance_time(current_time, task.duration_minutes)
            remaining_minutes -= task.duration_minutes

        return self.resolve_conflicts(schedule)

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Order tasks by priority, duration, and title."""
        return sorted(
            tasks,
            key=lambda task: (
                -task.get_priority_score(),
                -task.duration_minutes,
                task.title,
            ),
        )

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by their scheduled clock time."""
        return sorted(tasks, key=lambda task: tuple(map(int, task.time.split(":"))))

    def filter_by_time(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        """Keep only tasks that fit within the available time budget."""
        return [task for task in tasks if task.duration_minutes <= available_minutes]

    def filter_tasks(self, tasks: List[Task], *, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status or pet name when provided."""
        filtered_tasks = list(tasks)
        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.is_complete is completed]
        if pet_name is not None:
            filtered_tasks = [task for task in filtered_tasks if pet_name.lower() in task.title.lower() or pet_name.lower() in task.category.lower()]
        return filtered_tasks

    def resolve_conflicts(self, schedule: Schedule) -> Schedule:
        """Remove overlapping time blocks from the schedule."""
        resolved_blocks: List[TimeBlock] = []
        for block in sorted(schedule.time_blocks, key=lambda item: item.start_time):
            if not resolved_blocks:
                resolved_blocks.append(block)
                continue

            previous = resolved_blocks[-1]
            if block.start_time < previous.end_time:
                continue
            resolved_blocks.append(block)

        schedule.time_blocks = resolved_blocks
        return schedule

    def detect_conflicts(self, tasks: List[Task]) -> Optional[str]:
        """Return a warning message when tasks overlap in time; otherwise return None."""
        try:
            sorted_tasks = self.sort_by_time(tasks)
            for previous, current in zip(sorted_tasks, sorted_tasks[1:]):
                previous_start = self._time_to_minutes(previous.time)
                current_start = self._time_to_minutes(current.time)
                if current_start < previous_start + previous.duration_minutes:
                    return f"Warning: {previous.title} and {current.title} overlap in time."
        except (ValueError, AttributeError):
            return None
        return None

    @staticmethod
    def _time_to_minutes(value: str) -> int:
        """Convert an HH:MM time string into total minutes."""
        hours, minutes = map(int, value.split(":"))
        return hours * 60 + minutes

    @staticmethod
    def _minutes_between(start_time: str, end_time: str) -> int:
        """Return the number of minutes between two clock times."""
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.strptime(end_time, "%H:%M")
        return int((end_dt - start_dt).total_seconds() // 60)

    @staticmethod
    def _advance_time(start_time: str, minutes: int) -> str:
        """Return a new clock time after adding the given number of minutes."""
        start_dt = datetime.strptime(start_time, "%H:%M")
        return (start_dt + timedelta(minutes=minutes)).strftime("%H:%M")
