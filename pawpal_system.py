from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import List, Optional
import json


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
    date: Optional[str] = None
    last_completed_date: Optional[str] = None

    def get_priority_score(self) -> int:
        """Return a numeric score for sorting tasks by priority."""
        priority_scores = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
        }
        return priority_scores[self.priority]

    def to_dict(self) -> dict:
        """Serialize the task to a JSON-compatible dictionary."""
        return {
            "title": self.title,
            "category": self.category,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority.value,
            "is_recurring": self.is_recurring,
            "is_complete": self.is_complete,
            "time": self.time,
            "recurrence": self.recurrence,
            "date": self.date,
            "last_completed_date": self.last_completed_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Restore a Task from a dictionary."""
        return cls(
            title=data.get("title", ""),
            category=data.get("category", "general"),
            duration_minutes=int(data.get("duration_minutes", 0)),
            priority=Priority(data.get("priority", Priority.MEDIUM.value)),
            is_recurring=data.get("is_recurring", False),
            is_complete=data.get("is_complete", False),
            time=data.get("time", "08:00"),
            recurrence=data.get("recurrence"),
            date=data.get("date"),
            last_completed_date=data.get("last_completed_date"),
        )

    def mark_complete(self, pet: Optional[Pet] = None) -> Optional["Task"]:
        """Mark the task as completed and create the next occurrence when it recurs."""
        today_date = datetime.now().strftime("%Y-%m-%d")
        self.is_complete = True
        self.last_completed_date = today_date
        if not self.date:
            self.date = today_date
        if self.is_recurring and self.recurrence in {"daily", "weekly"} and pet is not None:
            next_date = self._next_occurrence_date()
            next_task = Task(
                title=self.title,
                category=self.category,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                is_recurring=True,
                recurrence=self.recurrence,
                time=self.time,
                date=next_date,
            )
            pet.add_task(next_task)
            return next_task
        return None

    def _next_occurrence_date(self) -> str:
        """Return the next occurrence date for this recurring task."""
        current_date = datetime.strptime(self.date, "%Y-%m-%d") if self.date else datetime.now()
        step = 1 if self.recurrence == "daily" else 7
        return (current_date + timedelta(days=step)).strftime("%Y-%m-%d")


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)
    task_history: "TaskHistory" = field(default_factory=lambda: TaskHistory())

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's care list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return the pet's current list of tasks."""
        return self.tasks

    def to_dict(self) -> dict:
        """Serialize the pet and its tasks to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "notes": self.notes,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        """Restore a Pet from a dictionary."""
        pet = cls(
            name=data.get("name", ""),
            species=data.get("species", ""),
            age=int(data.get("age", 0)),
            notes=data.get("notes", ""),
        )
        for task_data in data.get("tasks", []):
            pet.add_task(Task.from_dict(task_data))
        return pet


@dataclass
class TaskGroup:
    tasks: List[Task]
    duration_minutes: int


def _can_overlap_as_parallel(previous: TimeBlock, current: TimeBlock) -> bool:
    """Return True when two time blocks represent parallel tasks for different pets."""
    if previous.task is None or current.task is None:
        return False
    if previous.pet is None or current.pet is None:
        return False
    if previous.pet is current.pet:
        return False
    return (
        previous.task.title.lower() == current.task.title.lower()
        and previous.task.category.lower() == current.task.category.lower()
        and previous.task.duration_minutes == current.task.duration_minutes
    )


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

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "available_start": self.available_start,
            "available_end": self.available_end,
            "preferences": self.preferences,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Owner":
        owner = cls(
            name=data.get("name", ""),
            available_start=data.get("available_start", "08:00"),
            available_end=data.get("available_end", "20:00"),
            preferences=data.get("preferences", []),
        )
        for pet_data in data.get("pets", []):
            owner.add_pet(Pet.from_dict(pet_data))
        return owner


@dataclass
class TaskRecord:
    task_title: str
    completed_date: str
    category: str
    pet_name: str

    def to_dict(self) -> dict:
        return {
            "task_title": self.task_title,
            "completed_date": self.completed_date,
            "category": self.category,
            "pet_name": self.pet_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskRecord":
        return cls(
            task_title=data.get("task_title", ""),
            completed_date=data.get("completed_date", ""),
            category=data.get("category", ""),
            pet_name=data.get("pet_name", ""),
        )


@dataclass
class TaskHistory:
    records: List[TaskRecord] = field(default_factory=list)

    def add_record(self, record: TaskRecord) -> None:
        """Store a completed task event for later planning decisions."""
        self.records.append(record)

    def to_dict(self) -> dict:
        return {"records": [record.to_dict() for record in self.records]}

    @classmethod
    def from_dict(cls, data: dict) -> "TaskHistory":
        history = cls()
        for record_data in data.get("records", []):
            history.add_record(TaskRecord.from_dict(record_data))
        return history

    def get_recent_tasks(self, pet_name: str, days: int = 7) -> List[TaskRecord]:
        """Return task records completed within the recent window for a given pet."""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            record
            for record in self.records
            if record.pet_name.lower() == pet_name.lower()
            and self._parse_date(record.completed_date) >= cutoff
        ]

    def should_repeat(self, task: Task, pet_name: Optional[str] = None) -> bool:
        """Return True when a recently completed task should be suppressed today."""
        if not self.records:
            return False

        recent_records = self.get_recent_tasks(pet_name or "", days=7) if pet_name else self.records
        target_title = task.title.lower()
        target_category = task.category.lower()

        return any(
            target_title in record.task_title.lower() or target_category in record.category.lower()
            for record in recent_records
        )

    @staticmethod
    def _parse_date(value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%d")


@dataclass
class TimeBlock:
    start_time: str
    end_time: str
    task: Optional[Task] = None
    pet: Optional[Pet] = None

    def is_available(self) -> bool:
        """Return True when the time block has no assigned task."""
        return self.task is None


@dataclass
class Schedule:
    date: str
    time_blocks: List[TimeBlock] = field(default_factory=list)

    def add_task(self, task: Task, start_time: str, pet: Optional[Pet] = None) -> None:
        """Add a task to the schedule at the provided start time."""
        start_dt = self._parse_time(start_time)
        end_dt = start_dt + timedelta(minutes=task.duration_minutes)
        self.time_blocks.append(
            TimeBlock(
                start_time=start_time,
                end_time=end_dt.strftime("%H:%M"),
                task=task,
                pet=pet,
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
        task_pool = [task for task in (tasks if tasks else pet.get_tasks()) if not task.is_complete]
        sorted_tasks = self.sort_tasks(task_pool)
        available_minutes = self._minutes_between(owner.available_start, owner.available_end)
        feasible_tasks = self.filter_by_time(sorted_tasks, available_minutes)

        schedule = Schedule(date="today")
        current_time = owner.available_start
        remaining_minutes = available_minutes

        for task in feasible_tasks:
            if task.duration_minutes > remaining_minutes:
                continue

            schedule.add_task(task, current_time, pet=pet)
            current_time = self._advance_time(current_time, task.duration_minutes)
            remaining_minutes -= task.duration_minutes

        resolved_schedule = self.resolve_conflicts(schedule)
        reliability_manager = ReliabilityManager()
        return reliability_manager.repair_schedule(resolved_schedule, feasible_tasks, owner)

    def build_multi_pet_plan(self, owner: Owner, tasks: Optional[List[Task]] = None) -> Schedule:
        """Build one consolidated schedule that covers all of an owner's pets."""
        task_pool = [task for task in (tasks if tasks is not None else [task for pet in owner.pets for task in pet.get_tasks()]) if not task.is_complete]
        if not task_pool:
            return Schedule(date="today")

        sorted_tasks = sorted(
            task_pool,
            key=lambda task: (
                self._time_to_minutes(task.time),
                -task.get_priority_score(),
                -task.duration_minutes,
                task.title,
            ),
        )
        available_minutes = self._minutes_between(owner.available_start, owner.available_end)
        feasible_tasks = self.filter_by_time(sorted_tasks, available_minutes)

        schedule = Schedule(date="today")
        current_time = owner.available_start
        pet_lookup = {id(task): pet for pet in owner.pets for task in pet.get_tasks()}

        for task_group in self._group_parallel_tasks(feasible_tasks, pet_lookup):
            group_start = min(task.time for task in task_group.tasks)
            start_time = max(current_time, group_start)
            available_minutes = self._minutes_between(start_time, owner.available_end)
            if task_group.duration_minutes > available_minutes:
                continue

            for task in task_group.tasks:
                schedule.add_task(task, start_time, pet=pet_lookup.get(id(task)))

            current_time = self._advance_time(start_time, task_group.duration_minutes)

        resolved_schedule = self.resolve_conflicts(schedule)
        reliability_manager = ReliabilityManager()
        return reliability_manager.repair_schedule(resolved_schedule, feasible_tasks, owner)

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
    def _group_parallel_tasks(self, tasks: List[Task], pet_lookup: dict[int, Pet]) -> list["TaskGroup"]:
        """Group identical tasks across different pets for parallel execution."""
        grouped: dict[tuple[str, str, int, Priority], list[Task]] = {}
        for task in tasks:
            key = (
                task.title.lower(),
                task.category.lower(),
                task.duration_minutes,
                task.priority,
            )
            grouped.setdefault(key, []).append(task)

        groups: list[TaskGroup] = []
        for task_list in grouped.values():
            groups.append(TaskGroup(tasks=task_list, duration_minutes=task_list[0].duration_minutes))

        groups.sort(key=lambda group: (
            -max(task.get_priority_score() for task in group.tasks),
            -group.duration_minutes,
            min(task.time for task in group.tasks),
            group.tasks[0].title,
        ))
        return groups
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
        """Remove overlapping time blocks from the schedule unless they are parallelizable across pets."""
        resolved_blocks: List[TimeBlock] = []
        for block in sorted(schedule.time_blocks, key=lambda item: item.start_time):
            if not resolved_blocks:
                resolved_blocks.append(block)
                continue

            previous = resolved_blocks[-1]
            if block.start_time < previous.end_time and not _can_overlap_as_parallel(previous, block):
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


@dataclass
class PlanningWorkflow:
    def gather_context(self, owner: Owner, pet: Pet, tasks: List[Task], history: Optional[TaskHistory]) -> dict:
        """Collect the owner, pet, task, and history context for planning."""
        return {
            "owner": owner,
            "pet": pet,
            "tasks": list(tasks),
            "history": history,
        }

    def prioritize_tasks(self, tasks: List[Task], history: Optional[TaskHistory], pet_name: Optional[str] = None) -> List[Task]:
        """Re-rank tasks using recent task history and priority."""
        ranked_tasks = []
        for task in tasks:
            priority_score = task.get_priority_score()
            if history is not None and history.should_repeat(task, pet_name):
                priority_score -= 1
            ranked_tasks.append((priority_score, task))

        ranked_tasks.sort(key=lambda item: (-item[0], item[1].time, item[1].title))
        return [task for _, task in ranked_tasks]

    def build_schedule(self, owner: Owner, pet: Pet, tasks: List[Task], history: Optional[TaskHistory] = None, pet_name: Optional[str] = None) -> Schedule:
        """Build an AI-informed schedule using history-aware prioritization."""
        task_pool = tasks if tasks else pet.get_tasks()
        prioritized_tasks = self.prioritize_tasks(task_pool, history, pet_name=pet_name or pet.name)
        scheduler = Scheduler()
        schedule = scheduler.build_daily_plan(owner, pet, prioritized_tasks)
        return schedule

    def generate_explanation(self, schedule: Schedule, history: Optional[TaskHistory] = None) -> str:
        """Create a short explanation of the resulting daily plan."""
        history_note = "history-aware" if history and history.records else "rule-based"
        return f"Generated a {history_note} daily plan with {len(schedule.time_blocks)} scheduled task block(s)."


@dataclass
class PlannerAgent:
    workflow: PlanningWorkflow = field(default_factory=PlanningWorkflow)
    scheduler: Scheduler = field(default_factory=Scheduler)
    reliability_manager: "ReliabilityManager" = field(default_factory=lambda: ReliabilityManager())
    explanation_engine: "ExplanationEngine" = field(default_factory=lambda: ExplanationEngine())

    def plan_daily_schedule(self, owner: Owner, pet: Pet, tasks: List[Task], history: Optional[TaskHistory] = None) -> Schedule:
        """Coordinate the planning workflow and return a safe, history-aware schedule."""
        task_pool = tasks if tasks else pet.get_tasks()
        prioritized_tasks = self.workflow.prioritize_tasks(task_pool, history, pet_name=pet.name)
        schedule = self.scheduler.build_daily_plan(owner, pet, prioritized_tasks)
        return self.reliability_manager.repair_schedule(schedule, prioritized_tasks, owner)

    def plan_owner_schedule(self, owner: Owner, history: Optional[TaskHistory] = None) -> Schedule:
        """Build one consolidated schedule for every pet owned by the same owner."""
        all_tasks = [task for pet in owner.pets for task in pet.get_tasks()]
        prioritized_tasks = self.workflow.prioritize_tasks(all_tasks, history)
        schedule = self.scheduler.build_multi_pet_plan(owner, prioritized_tasks)
        return self.reliability_manager.repair_schedule(schedule, prioritized_tasks, owner)

    def explain_plan(self, schedule: Schedule, history: Optional[TaskHistory] = None) -> str:
        """Return a human-readable explanation for the resulting plan."""
        return self.explanation_engine.generate_rationale(schedule, history)


@dataclass
class ReliabilityManager:
    def validate_schedule(self, schedule: Schedule) -> bool:
        """Return True when no time blocks overlap."""
        return len(self.detect_overlaps(schedule)) == 0

    def detect_overlaps(self, schedule: Schedule) -> List[TimeBlock]:
        """Return any overlapping schedule blocks."""
        overlaps: List[TimeBlock] = []
        sorted_blocks = sorted(schedule.time_blocks, key=lambda item: self._to_minutes(item.start_time))
        for previous, current in zip(sorted_blocks, sorted_blocks[1:]):
            if self._to_minutes(current.start_time) < self._to_minutes(previous.end_time):
                overlaps.append(current)
        return overlaps

    def repair_schedule(self, schedule: Schedule, tasks: List[Task], owner: Optional[Owner] = None) -> Schedule:
        """Move later blocks forward when they overlap earlier ones unless they are intentionally parallel."""
        if not schedule.time_blocks:
            return schedule

        repaired_blocks: List[TimeBlock] = []
        for block in sorted(schedule.time_blocks, key=lambda item: self._to_minutes(item.start_time)):
            if not repaired_blocks:
                repaired_blocks.append(block)
                continue

            previous = repaired_blocks[-1]
            previous_end = self._to_minutes(previous.end_time)
            current_start = self._to_minutes(block.start_time)
            if current_start < previous_end and not _can_overlap_as_parallel(previous, block):
                current_start = previous_end
                block.start_time = self._format_time(current_start)
                if block.task is not None:
                    block.end_time = self._format_time(current_start + block.task.duration_minutes)

            if owner is not None and current_start > self._to_minutes(owner.available_end):
                continue

            repaired_blocks.append(block)

        schedule.time_blocks = repaired_blocks
        return schedule

    def apply_safety_rules(self, schedule: Schedule) -> Schedule:
        """Apply overlap repair as a safety rule before returning the schedule."""
        return self.repair_schedule(schedule, [block.task for block in schedule.time_blocks if block.task is not None], None)

    @staticmethod
    def _to_minutes(value: str) -> int:
        hours, minutes = map(int, value.split(":"))
        return hours * 60 + minutes

    @staticmethod
    def _format_time(value: int) -> str:
        hours, minutes = divmod(value, 60)
        return f"{hours:02d}:{minutes:02d}"


@dataclass
@dataclass
class DataStore:
    file_path: str = "pawpal_data.json"

    def save(self, owner: Owner, history: TaskHistory, last_date: Optional[str] = None) -> None:
        if last_date is None:
            last_date = datetime.now().strftime("%Y-%m-%d")
        data = {
            "owner": owner.to_dict(),
            "history": history.to_dict(),
            "metadata": {"last_date": last_date},
        }
        Path(self.file_path).write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self) -> Optional[tuple[Owner, TaskHistory, dict]]:
        path = Path(self.file_path)
        if not path.exists():
            return None
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            owner_data = raw.get("owner", {})
            history_data = raw.get("history", {})
            metadata = raw.get("metadata", {})
            owner = Owner.from_dict(owner_data)
            history = TaskHistory.from_dict(history_data)
            return owner, history, metadata
        except (json.JSONDecodeError, TypeError, ValueError):
            return None


class ExplanationEngine:
    def generate_rationale(self, schedule: Schedule, history: Optional[TaskHistory] = None) -> str:
        """Create a short rationale for why the plan looks the way it does."""
        if history and history.records:
            return f"The plan uses recent task history to avoid overloading recurring care routines and to reduce overlap risk."
        return f"The plan schedules {len(schedule.time_blocks)} task block(s) while keeping the routine clear and conflict-aware."
