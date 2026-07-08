from datetime import date, timedelta

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def test_sort_tasks_orders_by_priority_and_duration():
    scheduler = Scheduler()
    tasks = [
        Task("Feeding", "feeding", 15, Priority.LOW, time="12:00"),
        Task("Walk", "walk", 30, Priority.HIGH, time="08:30"),
        Task("Medicine", "medication", 10, Priority.HIGH, time="09:00"),
    ]

    ordered = scheduler.sort_tasks(tasks)

    assert [task.title for task in ordered] == ["Walk", "Medicine", "Feeding"]


def test_build_daily_plan_schedules_tasks_within_owner_window():
    owner = Owner("Jordan", available_start="08:00", available_end="09:00")
    pet = Pet("Mochi", "dog")
    scheduler = Scheduler()
    tasks = [
        Task("Morning walk", "walk", 25, Priority.HIGH),
        Task("Feeding", "feeding", 10, Priority.MEDIUM),
        Task("Medicine", "medication", 15, Priority.HIGH),
    ]

    schedule = scheduler.build_daily_plan(owner, pet, tasks)

    assert len(schedule.time_blocks) == 3
    assert schedule.time_blocks[0].task.title == "Morning walk"
    assert schedule.time_blocks[0].start_time == "08:00"
    assert schedule.time_blocks[-1].end_time == "08:50"
    assert "3 task block" in schedule.summarize()


def test_sort_by_time_orders_tasks_by_clock_time():
    scheduler = Scheduler()
    tasks = [
        Task("Dinner", "feeding", 15, Priority.HIGH, time="20:00"),
        Task("Breakfast", "feeding", 10, Priority.HIGH, time="08:00"),
        Task("Lunch", "feeding", 15, Priority.MEDIUM, time="12:30"),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [task.title for task in ordered] == ["Breakfast", "Lunch", "Dinner"]


def test_filter_tasks_by_completion_and_pet_name():
    scheduler = Scheduler()
    tasks = [
        Task("Walk", "exercise", 20, Priority.HIGH, time="08:00"),
        Task("Feed", "feeding", 10, Priority.MEDIUM, time="12:00"),
    ]
    tasks[0].mark_complete()

    filtered = scheduler.filter_tasks(tasks, completed=True)
    assert [task.title for task in filtered] == ["Walk"]

    filtered_by_name = scheduler.filter_tasks(tasks, pet_name="feed")
    assert [task.title for task in filtered_by_name] == ["Feed"]


def test_mark_complete_creates_next_occurrence_for_recurring_task():
    pet = Pet("Mochi", "dog")
    task = Task(
        "Walk",
        "exercise",
        20,
        Priority.HIGH,
        is_recurring=True,
        recurrence="daily",
        time="08:00",
    )
    pet.add_task(task)

    new_task = task.mark_complete(pet=pet)

    assert task.is_complete is True
    assert new_task is not None
    assert new_task.is_complete is False
    assert new_task.recurrence == "daily"
    assert new_task.date == (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    assert len(pet.get_tasks()) == 2


def test_detect_conflicts_returns_warning_message_for_overlapping_tasks():
    scheduler = Scheduler()
    tasks = [
        Task("Walk", "exercise", 30, Priority.HIGH, time="08:00"),
        Task("Feed", "feeding", 20, Priority.MEDIUM, time="08:15"),
    ]

    warning = scheduler.detect_conflicts(tasks)

    assert warning is not None
    assert "overlap" in warning.lower()


def test_detect_conflicts_flags_duplicate_times():
    scheduler = Scheduler()
    tasks = [
        Task("Walk", "exercise", 30, Priority.HIGH, time="08:00"),
        Task("Feed", "feeding", 20, Priority.MEDIUM, time="08:00"),
    ]

    warning = scheduler.detect_conflicts(tasks)

    assert warning is not None
    assert "overlap" in warning.lower()
