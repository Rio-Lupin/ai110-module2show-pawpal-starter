from pawpal_system import Owner, Pet, Task, Scheduler, Priority

def main():
    # 1. Create Owner and Pets matching your class definitions
    owner = Owner(name="Carlene", available_start="08:00", available_end="20:00")
    dog = Pet(name="Rio", species="Dog")
    dog2 = Pet(name="Lupin", species="Dog")
    dog3 = Pet(name="Coco", species="Dog")
    
    owner.add_pet(dog)
    owner.add_pet(dog2)
    owner.add_pet(dog3)
    
    # 2. Create tasks with your system's exact required fields
    task1 = Task(title="Afternoon Walk", category="Exercise", duration_minutes=45, priority=Priority.MEDIUM, time="16:00")
    task2 = Task(title="Feed Breakfast", category="Feeding", duration_minutes=15, priority=Priority.HIGH, time="08:00")
    task3 = Task(title="Give Medicine", category="Medical", duration_minutes=10, priority=Priority.HIGH, time="09:00")
    task4 = Task(title="Feed Dinner", category="Feeding", duration_minutes=15, priority=Priority.HIGH, time="18:00")
    task5 = Task(title="Play Time", category="Enrichment", duration_minutes=20, priority=Priority.MEDIUM, time="14:00")
    task6 = Task(title="Bath Time", category="Grooming", duration_minutes=25, priority=Priority.LOW, time="19:00")
    
    # Assign tasks to pets out of order to demonstrate sorting and filtering
    dog.add_task(task6)
    dog.add_task(task1)
    dog.add_task(task5)
    dog.add_task(task2)
    dog.add_task(task4)

    dog2.add_task(task4)
    dog2.add_task(task2)
    dog2.add_task(task6)
    dog2.add_task(task1)
    dog2.add_task(task5)

    dog3.add_task(task5)
    dog3.add_task(task4)
    dog3.add_task(task2)
    dog3.add_task(task6)
    dog3.add_task(task3)
    
    # 3. Instantiate your system's Scheduler
    scheduler = Scheduler()
    
    print("=" * 45)
    print(f" TODAY'S SCHEDULE FOR {owner.name.upper()}'S PETS ")
    print("=" * 45)
    
    # 4. Generate daily plans via your Scheduler logic
    for pet in owner.pets:
        print(f"\n🐾 {pet.name} ({pet.species}):")

        unsorted_tasks = pet.get_tasks()
        print("  Unsorted tasks:")
        for task in unsorted_tasks:
            print(f"    - {task.title} ({task.time})")

        sorted_by_time = scheduler.sort_by_time(unsorted_tasks)
        print("  Sorted by time:")
        for task in sorted_by_time:
            print(f"    - {task.title} ({task.time})")

        filtered = scheduler.filter_tasks(unsorted_tasks, pet_name="feed")
        print("  Filtered by pet-name keyword 'feed':")
        for task in filtered:
            print(f"    - {task.title}")
        
        pet_schedule = scheduler.build_daily_plan(owner, pet, unsorted_tasks)
        
        if not pet_schedule.time_blocks:
            print("  No tasks scheduled.")
        else:
            print("  Scheduled plan:")
            for block in pet_schedule.time_blocks:
                print(f"    ⏰ {block.start_time} - {block.end_time} | [{block.task.priority.value.upper()}] {block.task.title}")
                
    print("\n" + "=" * 45)

if __name__ == "__main__":
    main()