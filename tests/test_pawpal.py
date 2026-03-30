import pytest

from datetime import datetime

from pawpal_system import DailyPlan, Owner, Pet, ScheduledTask, Task, Priority, TaskCategory, Scheduler


def test_task_completion_marks_completed():
    task = Task(
        title="Test task",
        duration_minutes=10,
        priority=Priority.MEDIUM,
        category=TaskCategory.GENERAL,
    )

    assert task.completed is False

    task.mark_completed()

    assert task.completed is True


def test_pet_add_task_increases_task_count():
    pet = Pet(name="Buddy", species="dog")
    initial_count = len(pet.tasks)

    new_task = Task(
        title="Play fetch",
        duration_minutes=15,
        priority=Priority.LOW,
        category=TaskCategory.WALK,
    )

    pet.add_task(new_task)

    assert len(pet.tasks) == initial_count + 1
    assert pet.tasks[0] == new_task


def test_scheduler_best_value_selection_fits_budget():
    owner = Owner(name="Alex")
    owner.update_time_budget(30)
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(
        title="Walk",
        duration_minutes=20,
        priority=Priority.HIGH,
        category=TaskCategory.WALK,
        frequency="daily",
    ))
    pet.add_task(Task(
        title="Play",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        category=TaskCategory.GENERAL,
        frequency="once",
    ))

    scheduler = Scheduler(owner)
    selected = scheduler.fit_within_constraints()

    assert any(task.title == "Walk" for task in selected)
    assert all(task.duration_minutes <= 30 for task in selected)


def test_generate_daily_plan_tracks_deferred_tasks():
    owner = Owner(name="Alex")
    owner.update_time_budget(30)
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(
        title="Walk",
        duration_minutes=20,
        priority=Priority.HIGH,
        category=TaskCategory.WALK,
        frequency="daily",
    ))
    pet.add_task(Task(
        title="Play",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        category=TaskCategory.GENERAL,
        frequency="once",
    ))

    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan(start_time=datetime(2026, 1, 1, 8, 0))

    assert len(plan.scheduled_tasks) == 1
    assert len(plan.unscheduled_tasks) == 1
    assert plan.unscheduled_tasks[0].title == "Play"


def test_complete_daily_task_creates_next_occurrence():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        category=TaskCategory.WALK,
        frequency="daily",
        preferred_start_time="08:00",
        due_date=datetime(2026, 1, 1, 8, 0),
    )
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.title == "Morning walk"
    assert next_task.completed is False
    assert next_task.due_date == datetime(2026, 1, 2, 8, 0)
    assert owner.pending_tasks()[-1].title == "Morning walk"
    assert len(owner.all_tasks()) == 2


def test_owner_filters_tasks_by_pet_and_status():
    owner = Owner(name="Alex")
    pet1 = Pet(name="Buddy", species="dog")
    pet2 = Pet(name="Whiskers", species="cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(
        title="Walk",
        duration_minutes=20,
        priority=Priority.HIGH,
        category=TaskCategory.WALK,
        frequency="daily",
    )
    task2 = Task(
        title="Feed",
        duration_minutes=10,
        priority=Priority.MEDIUM,
        category=TaskCategory.FEED,
        frequency="twice-a-day",
    )
    task2.mark_completed()

    pet1.add_task(task1)
    pet2.add_task(task2)

    assert owner.get_tasks_by_pet("Buddy") == [task1]
    assert owner.get_tasks_by_status(completed=False) == [task1]
    assert owner.get_tasks_by_status(completed=True) == [task2]
    assert owner.get_pending_tasks_by_pet("Whiskers") == []


def test_sort_by_time_uses_hh_mm_string():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(
        title="Late",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        category=TaskCategory.GENERAL,
        preferred_start_time="15:30",
    ))
    pet.add_task(Task(
        title="Early",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        category=TaskCategory.GENERAL,
        preferred_start_time="08:05",
    ))
    pet.add_task(Task(
        title="Mid",
        duration_minutes=15,
        priority=Priority.MEDIUM,
        category=TaskCategory.GENERAL,
        preferred_start_time="12:00",
    ))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(scheduler.retrieve_pending_tasks())

    assert [task.title for task in sorted_tasks] == ["Early", "Mid", "Late"]


def test_recurring_tasks_expand_for_twice_a_day():
    owner = Owner(name="Alex")
    owner.update_time_budget(60)
    pet = Pet(name="Buddy", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(
        title="Feed",
        duration_minutes=10,
        priority=Priority.MEDIUM,
        category=TaskCategory.FEED,
        frequency="twice-a-day",
    ))

    scheduler = Scheduler(owner)
    selected = scheduler.fit_within_constraints()

    assert any("(AM)" in task.title for task in selected)
    assert any("(PM)" in task.title for task in selected)
    assert len(selected) == 2


def test_daily_plan_conflict_detection():
    plan = DailyPlan()

    task1 = Task(
        title="Walk",
        duration_minutes=20,
        priority=Priority.HIGH,
        category=TaskCategory.WALK,
    )
    task2 = Task(
        title="Feed",
        duration_minutes=20,
        priority=Priority.MEDIUM,
        category=TaskCategory.FEED,
    )

    plan.add_scheduled_task(ScheduledTask(
        task=task1,
        start_time=datetime(2026, 1, 1, 8, 0),
        end_time=datetime(2026, 1, 1, 8, 20),
    ))
    plan.add_scheduled_task(ScheduledTask(
        task=task2,
        start_time=datetime(2026, 1, 1, 8, 15),
        end_time=datetime(2026, 1, 1, 8, 35),
    ))

    conflicts = plan.detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0][0].task.title == "Walk"
    assert conflicts[0][1].task.title == "Feed"


def test_scheduler_warns_when_tasks_share_start_time():
    owner = Owner(name="Alex")
    owner.update_time_budget(120)
    pet1 = Pet(name="Buddy", species="dog")
    pet2 = Pet(name="Whiskers", species="cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    pet1.add_task(Task(
        title="Walk",
        duration_minutes=20,
        priority=Priority.HIGH,
        category=TaskCategory.WALK,
        preferred_start_time="08:00",
    ))
    pet2.add_task(Task(
        title="Feed",
        duration_minutes=10,
        priority=Priority.MEDIUM,
        category=TaskCategory.FEED,
        preferred_start_time="08:00",
    ))

    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan(start_time=datetime(2026, 1, 1, 8, 0))

    warnings = plan.conflict_warnings()
    assert len(warnings) == 1
    assert "overlaps with" in warnings[0]
