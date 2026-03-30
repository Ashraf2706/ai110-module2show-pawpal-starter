from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskCategory(Enum):
    WALK = "walk"
    FEED = "feed"
    MEDS = "meds"
    GENERAL = "general"

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    category: TaskCategory = TaskCategory.GENERAL
    frequency: str = "once"  # daily, weekly, twice-a-day, etc.
    preferred_time_of_day: Optional[str] = None  # morning, afternoon, evening, any
    preferred_start_time: Optional[str] = None  # HH:MM formatted preferred start time
    due_date: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    source_title: Optional[str] = None
    completed: bool = False
    notes: Optional[str] = None

    def mark_completed(self) -> Optional[Task]:
        """Mark the task as completed and return the next occurrence if recurring."""
        self.completed = True
        if self.frequency in {"daily", "weekly"}:
            return self.clone_for_next_occurrence()
        return None

    def clone_for_next_occurrence(self) -> Task:
        """Create a new task instance for the next recurring occurrence."""
        if self.frequency == "daily":
            next_due = (self.due_date or datetime.now()) + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = (self.due_date or datetime.now()) + timedelta(weeks=1)
        else:
            next_due = self.due_date

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            preferred_time_of_day=self.preferred_time_of_day,
            preferred_start_time=self.preferred_start_time,
            due_date=next_due,
            dependencies=list(self.dependencies),
            source_title=self.source_title or self.title,
            completed=False,
            notes=self.notes,
        )

    def urgency_value(self) -> int:
        """Estimate urgency from the task frequency."""
        mapping = {
            "twice-a-day": 4,
            "daily": 3,
            "weekly": 2,
            "once": 1,
        }
        return mapping.get(self.frequency, 1)

    def to_dict(self) -> Dict[str, str]:
        """Convert task details to a dictionary."""
        return {
            "title": self.title,
            "duration_minutes": str(self.duration_minutes),
            "priority": self.priority.value,
            "category": self.category.value,
            "frequency": self.frequency,
            "preferred_time_of_day": self.preferred_time_of_day or "any",
            "preferred_start_time": self.preferred_start_time or "",
            "due_date": self.due_date.isoformat() if self.due_date else "",
            "dependencies": ", ".join(self.dependencies),
            "completed": str(self.completed),
            "notes": self.notes or "",
        }

    def mark_pending(self) -> None:
        """Set the task status back to pending."""
        self.completed = False

    def update_duration(self, minutes: int) -> None:
        """Update the task duration in minutes."""
        self.duration_minutes = minutes

    def update_priority(self, priority: Priority) -> None:
        """Update the task priority."""
        self.priority = priority

    def update_category(self, category: TaskCategory) -> None:
        """Update the task category."""
        self.category = category

    def is_recurring(self) -> bool:
        """Return whether the task should recur in a plan."""
        return self.frequency in {"daily", "twice-a-day", "weekly"}

    def clone_for_slot(self, suffix: str, preferred_time_of_day: Optional[str]) -> Task:
        """Create a copy of the task for a specific time slot."""
        return Task(
            title=f"{self.title} {suffix}",
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            preferred_time_of_day=preferred_time_of_day,
            preferred_start_time=self.preferred_start_time,
            due_date=self.due_date,
            dependencies=list(self.dependencies),
            source_title=self.title,
            completed=self.completed,
            notes=self.notes,
        )

@dataclass
class Pet:
    name: str
    species: str
    requirements: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_requirement(self, requirement: str) -> None:
        """Add a requirement to the pet if not already present."""
        if requirement not in self.requirements:
            self.requirements.append(requirement)

    def remove_requirement(self, requirement: str) -> None:
        """Remove a requirement from the pet."""
        if requirement in self.requirements:
            self.requirements.remove(requirement)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet if not already assigned."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def all_tasks(self) -> List[Task]:
        """Return all tasks for the pet."""
        return list(self.tasks)

    def pending_tasks(self) -> List[Task]:
        """Return pending tasks for the pet."""
        return [task for task in self.tasks if not task.completed]

    def completed_tasks(self) -> List[Task]:
        """Return completed tasks for the pet."""
        return [task for task in self.tasks if task.completed]

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Get a pet by name."""
        return next((pet for pet in self.pets if pet.name == name), None)

    def find_pet_for_task(self, task: Task) -> Optional[Pet]:
        """Return the pet that owns a given task."""
        return next((pet for pet in self.pets if task in pet.tasks), None)

    def get_tasks_by_pet(self, name: str) -> List[Task]:
        """Return tasks for a given pet name."""
        pet = self.get_pet(name)
        return pet.all_tasks() if pet else []

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [task for task in self.all_tasks() if task.completed == completed]

    def get_pending_tasks_by_pet(self, name: str) -> List[Task]:
        """Return pending tasks for a given pet."""
        pet = self.get_pet(name)
        return pet.pending_tasks() if pet else []

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        tasks = self.get_pet(pet_name).all_tasks() if pet_name and self.get_pet(pet_name) else self.all_tasks()
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks

    def all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def pending_tasks(self) -> List[Task]:
        """Return all pending tasks across pets."""
        return [task for task in self.all_tasks() if not task.completed]

    def completed_tasks(self) -> List[Task]:
        """Return all completed tasks across pets."""
        return [task for task in self.all_tasks() if task.completed]

    def set_preference(self, key: str, value: str) -> None:
        """Set an owner preference.

        """
        self.preferences[key] = value

    def update_time_budget(self, minutes: int) -> None:
        """Update owner's daily time budget preference."""
        self.preferences["daily_time_budget"] = str(minutes)

@dataclass
class ScheduledTask:
    task: Task
    start_time: datetime
    end_time: datetime
    pet_name: Optional[str] = None
    reasoning: Optional[str] = None

@dataclass
class DailyPlan:
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
    unscheduled_tasks: List[Task] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

    def total_duration(self) -> int:
        """Return total duration of scheduled tasks."""
        return sum(st.task.duration_minutes for st in self.scheduled_tasks)

    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        """Append a scheduled task to the plan."""
        self.scheduled_tasks.append(scheduled_task)

    def summary(self) -> str:
        """Get a text summary of the daily plan."""
        lines = [f"Daily plan created at {self.generated_at.isoformat()}"]
        if self.scheduled_tasks:
            lines.append("Scheduled tasks:")
            for st in self.scheduled_tasks:
                lines.append(
                    f"{st.start_time.strftime('%H:%M')}-{st.end_time.strftime('%H:%M')}: {st.task.title} ({st.task.priority.value})"
                )
        else:
            lines.append("No tasks were scheduled.")

        if self.unscheduled_tasks:
            lines.append("Deferred tasks:")
            for task in self.unscheduled_tasks:
                lines.append(f"- {task.title} ({task.priority.value}, {task.duration_minutes} min)")

        return "\n".join(lines)

    def detect_conflicts(self) -> List[tuple[ScheduledTask, ScheduledTask]]:
        """Detect overlapping scheduled tasks in a produced DailyPlan.

        Returns a list of task pairs that overlap in time. This is used for
        lightweight warning generation rather than failing the planner.
        """
        conflicts: List[tuple[ScheduledTask, ScheduledTask]] = []
        for index, first in enumerate(self.scheduled_tasks):
            for second in self.scheduled_tasks[index + 1 :]:
                if first.start_time < second.end_time and second.start_time < first.end_time:
                    conflicts.append((first, second))
        return conflicts

    def conflict_warnings(self) -> List[str]:
        """Return lightweight warning messages for detected schedule conflicts.

        The warnings are human-readable and do not raise exceptions. They help the
        owner see overlapping tasks for the same or different pets.
        """
        warnings: List[str] = []
        for first, second in self.detect_conflicts():
            pet_info = ""
            if first.pet_name or second.pet_name:
                pet_info = f" [{first.pet_name or 'unknown'} vs {second.pet_name or 'unknown'}]"
            warnings.append(
                f"Conflict{pet_info}: {first.task.title} ({first.start_time.strftime('%H:%M')} - {first.end_time.strftime('%H:%M')}) "
                f"overlaps with {second.task.title} ({second.start_time.strftime('%H:%M')} - {second.end_time.strftime('%H:%M')})"
            )
        return warnings

class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner context."""
        self.owner = owner

    def retrieve_all_tasks(self) -> List[Task]:
        """Retrieve every task from the owner's pets."""
        return self.owner.all_tasks()

    def retrieve_pending_tasks(self) -> List[Task]:
        """Retrieve all pending tasks for the owner."""
        return self.owner.pending_tasks()

    def retrieve_by_priority(self, priority: Priority) -> List[Task]:
        """Retrieve tasks filtered by priority."""
        return [t for t in self.owner.all_tasks() if t.priority == priority]

    def sort_by_priority(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted from high to low priority."""
        tasks = tasks if tasks is not None else self.retrieve_pending_tasks()
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority, 3))

    def task_score(self, task: Task) -> float:
        """Compute a weighted score used for task selection.

        The score combines task priority, urgency, and estimated time value so
        higher-priority, more urgent, and shorter tasks are preferred.
        """
        priority_weight = {Priority.HIGH: 30, Priority.MEDIUM: 20, Priority.LOW: 10}
        time_value = max(0, 20 - task.duration_minutes / 5)
        return priority_weight.get(task.priority, 0) + task.urgency_value() * 5 + time_value

    def task_sort_key(self, task: Task) -> tuple:
        """Sort tasks by score, category, and preferred time window."""
        category_order = {
            TaskCategory.MEDS: 0,
            TaskCategory.FEED: 1,
            TaskCategory.WALK: 2,
            TaskCategory.GENERAL: 3,
        }
        time_order = {
            "morning": 0,
            "afternoon": 1,
            "evening": 2,
            None: 3,
            "any": 3,
        }
        return (
            -self.task_score(task),
            category_order.get(task.category, 4),
            time_order.get(task.preferred_time_of_day, 3),
            task.duration_minutes,
        )

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by preferred start time, then by time-of-day bucket.

        If a task has a concrete preferred_start_time, it is ordered by the parsed
        HH:MM value. Otherwise the scheduler falls back to morning/afternoon/evening
        buckets and then by task score.
        """
        tasks = tasks if tasks is not None else self.retrieve_pending_tasks()
        def key(task: Task):
            if task.preferred_start_time:
                return tuple(map(int, task.preferred_start_time.split(":")))
            time_order = {"morning": 0, "afternoon": 1, "evening": 2, "any": 3, None: 3}
            return (99, time_order.get(task.preferred_time_of_day, 3), -self.task_score(task), task.duration_minutes)

        return sorted(tasks, key=key)

    def expand_recurring_tasks(self, tasks: List[Task]) -> List[Task]:
        """Expand recurring tasks into daily schedule instances.

        For example, twice-a-day tasks are converted into distinct AM and PM clones.
        This makes it easier to schedule repeating work on a single-day plan.
        """
        expanded: List[Task] = []
        for task in tasks:
            if task.frequency == "twice-a-day":
                expanded.append(task.clone_for_slot("(AM)", "morning"))
                expanded.append(task.clone_for_slot("(PM)", "evening"))
            else:
                expanded.append(task)
        return expanded

    def order_tasks_with_dependencies(self, tasks: List[Task]) -> List[Task]:
        """Order tasks while respecting simple dependency relationships.

        This performs a depth-first traversal over task dependencies so that a task
        appears after any tasks it depends on, while preserving the heuristic order
        of tasks with no dependency relationship.
        """
        title_map = {task.title: task for task in tasks}
        ordered: List[Task] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(task: Task) -> None:
            if task.title in visited:
                return
            if task.title in visiting:
                return

            visiting.add(task.title)
            for dep_title in task.dependencies:
                dep_task = title_map.get(dep_title)
                if dep_task:
                    visit(dep_task)
            visiting.remove(task.title)
            visited.add(task.title)
            ordered.append(task)

        for task in sorted(tasks, key=self.task_sort_key):
            visit(task)

        return ordered

    def fit_within_constraints(self, max_minutes: Optional[int] = None) -> List[Task]:
        """Pick tasks that fit within a daily time budget using a greedy selection.

        Tasks are sorted by score and scheduled until the remaining budget is exhausted.
        This is a lightweight approximate strategy that is easier to read and maintain
        than exact knapsack optimization for a pet care planner.
        """
        max_minutes = int(self.owner.preferences.get("daily_time_budget", "0")) if max_minutes is None else max_minutes
        if max_minutes <= 0:
            return []

        tasks = [task for task in self.expand_recurring_tasks(self.retrieve_pending_tasks()) if task.duration_minutes > 0]
        if not tasks:
            return []

        tasks.sort(key=lambda task: (-self.task_score(task), task.duration_minutes))

        selected: List[Task] = []
        remaining = max_minutes
        for task in tasks:
            if task.duration_minutes <= remaining:
                selected.append(task)
                remaining -= task.duration_minutes

        return selected

    def generate_daily_plan(self, start_time: Optional[datetime] = None, max_minutes: Optional[int] = None) -> DailyPlan:
        """Build a DailyPlan from selected tasks and start time."""
        if start_time is None:
            start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

        pending_tasks = self.retrieve_pending_tasks()
        selected_tasks = self.fit_within_constraints(max_minutes=max_minutes)
        selected_tasks = self.order_tasks_with_dependencies(selected_tasks)
        selected_tasks = self.sort_by_time(selected_tasks)

        plan = DailyPlan()
        selected_source_titles = {task.source_title or task.title for task in selected_tasks}
        plan.unscheduled_tasks = [task for task in pending_tasks if task.title not in selected_source_titles]

        current = start_time
        start_date = start_time.date()

        for task in selected_tasks:
            if task.preferred_start_time:
                hour, minute = map(int, task.preferred_start_time.split(":"))
                task_start = datetime.combine(start_date, datetime.min.time()).replace(hour=hour, minute=minute)
                if task_start < start_time:
                    task_start = task_start.replace(year=start_time.year, month=start_time.month, day=start_time.day)
                start_time_used = task_start
            else:
                start_time_used = max(current, start_time)

            end = start_time_used + timedelta(minutes=task.duration_minutes)
            pet = self.owner.find_pet_for_task(task)
            reason = (
                f"Scheduled {task.title} at {start_time_used.strftime('%H:%M')} because it has "
                f"priority={task.priority.value}, urgency={task.urgency_value()}, "
                f"duration={task.duration_minutes}."
            )
            plan.add_scheduled_task(
                ScheduledTask(
                    task=task,
                    start_time=start_time_used,
                    end_time=end,
                    pet_name=pet.name if pet else None,
                    reasoning=reason,
                )
            )
            if not task.preferred_start_time:
                current = end

        return plan

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task as completed and schedule the next recurring occurrence if needed.

        If the task is daily or weekly, a new instance is created and added to the
        same pet so the recurrence continues automatically.
        """
        next_task = task.mark_completed()
        if next_task:
            pet = self.owner.find_pet_for_task(task)
            if pet:
                pet.add_task(next_task)
        return next_task

    def provide_reasoning(self, plan: DailyPlan) -> str:
        """Provide a narrative reasoning for a given DailyPlan."""
        lines = ["Scheduler reasoning:"]
        lines.append(f"total planned minutes: {plan.total_duration()}")
        if conflicts := plan.detect_conflicts():
            lines.append("Conflicts detected in schedule:")
            for a, b in conflicts:
                lines.append(
                    f"- {a.task.title} overlaps with {b.task.title} "
                    f"({a.start_time.strftime('%H:%M')} - {a.end_time.strftime('%H:%M')} / "
                    f"{b.start_time.strftime('%H:%M')} - {b.end_time.strftime('%H:%M')})"
                )
        lines.append(plan.summary())
        if warnings := plan.conflict_warnings():
            lines.append("\nWarnings:")
            for warning in warnings:
                lines.append(f"- {warning}")
        if plan.unscheduled_tasks:
            lines.append("\nTasks deferred due to budget or schedule constraints:")
            for task in plan.unscheduled_tasks:
                lines.append(
                    f"- {task.title}: priority={task.priority.value}, "
                    f"frequency={task.frequency}, duration={task.duration_minutes}"
                )
        return "\n".join(lines)


