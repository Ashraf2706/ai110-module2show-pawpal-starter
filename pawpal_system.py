from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict

@dataclass
class Owner:
    name: str
    available_daily_time_budget: int  # minutes
    preferences: Dict[str, str] = field(default_factory=dict)

    def update_time_budget(self, minutes: int) -> None:
        pass

    def set_preference(self, key: str, value: str) -> None:
        pass

@dataclass
class Pet:
    name: str
    species: str
    requirements: List[str] = field(default_factory=list)

    def add_requirement(self, requirement: str) -> None:
        pass

    def remove_requirement(self, requirement: str) -> None:
        pass

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # low, medium, high
    category: str = "general"  # e.g. walk, feed, meds
    notes: Optional[str] = None

    def update_duration(self, minutes: int) -> None:
        pass

    def update_priority(self, priority: str) -> None:
        pass

    def update_category(self, category: str) -> None:
        pass

@dataclass
class ScheduledTask:
    task: Task
    start_time: datetime
    end_time: datetime
    reasoning: Optional[str] = None

@dataclass
class DailyPlan:
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

    def total_duration(self) -> int:
        pass

    def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
        pass

class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task]):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def sort_by_priority(self) -> List[Task]:
        pass

    def fit_within_constraints(self) -> List[Task]:
        pass

    def generate_daily_plan(self, start_time: Optional[datetime] = None) -> DailyPlan:
        pass

    def provide_reasoning(self, plan: DailyPlan) -> str:
        pass

