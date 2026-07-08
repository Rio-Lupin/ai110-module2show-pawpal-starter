from pawpal_system import Pet, Priority, Task


def test_mark_complete_changes_task_status():
    task = Task(
        title="Walk",
        category="Exercise",
        duration_minutes=20,
        priority=Priority.MEDIUM,
    )

    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_adding_task_to_pet_increases_task_count():
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.get_tasks())

    pet.add_task(
        Task(
            title="Feed",
            category="Feeding",
            duration_minutes=10,
            priority=Priority.HIGH,
        )
    )

    assert len(pet.get_tasks()) == initial_count + 1
