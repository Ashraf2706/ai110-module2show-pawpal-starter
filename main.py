from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler, Priority, TaskCategory


def main():
    owner = Owner(name="Jordan")
    owner.update_time_budget(120)  # for scheduler budget reference

    # Create two pets
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # Add tasks in a deliberately out-of-order way
    tasks = [
        Task(
            title="Morning walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            category=TaskCategory.WALK,
            frequency="daily",
            preferred_start_time="08:00",
        ),
        Task(
            title="Wake-up feeding",
            duration_minutes=10,
            priority=Priority.MEDIUM,
            category=TaskCategory.FEED,
            preferred_start_time="08:00",
        ),
        Task(
            title="Administer meds",
            duration_minutes=15,
            priority=Priority.HIGH,
            category=TaskCategory.MEDS,
            frequency="daily",
            preferred_start_time="09:30",
        ),
    ]

    mochi.add_task(tasks[0])
    whiskers.add_task(tasks[1])
    mochi.add_task(tasks[2])

    scheduler = Scheduler(owner)

    print("Raw task order after insertion:")
    for pet in owner.pets:
        print(f"- {pet.name} tasks:")
        for task in pet.tasks:
            print(f"  * {task.title} ({task.preferred_start_time or 'no time'})")

    sorted_tasks = scheduler.sort_by_time(owner.pending_tasks())
    print("\nTasks sorted by preferred start time:")
    for task in sorted_tasks:
        print(f"- {task.preferred_start_time or task.preferred_time_of_day}: {task.title}")

    print("\nFiltered tasks for Mochi (pending):")
    for task in owner.get_pending_tasks_by_pet("Mochi"):
        print(f"- {task.title} ({task.preferred_start_time})")

    print("\nFiltered completed tasks:")
    for task in owner.get_tasks_by_status(completed=True):
        print(f"- {task.title}")

    plan = scheduler.generate_daily_plan(start_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0))
    print("\nToday's Schedule")
    print("================")
    print(scheduler.provide_reasoning(plan))


if __name__ == "__main__":
    main()
