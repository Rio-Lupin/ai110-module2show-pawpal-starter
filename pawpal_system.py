from __future__ import annotations

from dataclasses import dataclass, field
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

    def get_priority_score(self) -> int:
        priority_scores = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
        }
        return priority_scores[self.priority]


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


@dataclass
class Owner:
    name: str
    available_start: str = "08:00"
    available_end: str = "20:00"
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def update_preferences(self, preferences: List[str]) -> None:
        self.preferences = preferences


@dataclass
class TimeBlock:
    start_time: str
    end_time: str
    task: Optional[Task] = None

    def is_available(self) -> bool:
        return self.task is None


@dataclass
class Schedule:
    date: str
    time_blocks: List[TimeBlock] = field(default_factory=list)

    def add_task(self, task: Task, start_time: str) -> None:
        # Placeholder for future scheduling logic.
        self.time_blocks.append(TimeBlock(start_time=start_time, end_time=start_time, task=task))

    def summarize(self) -> str:
        return f"Schedule for {self.date} with {len(self.time_blocks)} task block(s)."


@dataclass
class Scheduler:
    def build_daily_plan(self, owner: Owner, pet: Pet, tasks: List[Task]) -> Schedule:
        # Placeholder for future scheduling logic.
        return Schedule(date="today")

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: (-task.get_priority_score(), task.duration_minutes))

    def filter_by_time(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        return [task for task in tasks if task.duration_minutes <= available_minutes]

    def resolve_conflicts(self, schedule: Schedule) -> Schedule:
        return schedule
