# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## Smarter Scheduling
Scheduling & task selection

Greedy budget-aware scheduling with fit_within_constraints()

Tasks ranked by a weighted task_score() combining:
1. priority
2. urgency/frequency
3. duration

Time-aware ordering

sort_by_time() supports:
- exact preferred_start_time in HH:MM
- fallback to preferred_time_of_day buckets
- tasks are scheduled in time order when possible

Recurring task support

- Task.mark_completed() now rolls over daily and weekly tasks
- creates a next occurrence automatically with due_date advanced by 1 day or 1 week
- expand_recurring_tasks() turns twice-a-day tasks into separate AM/PM instances

Dependency and pet-aware ordering

- order_tasks_with_dependencies() preserves simple task dependency relationships
- Owner.find_pet_for_task() tracks which pet owns a task

Conflict detection and warnings

- DailyPlan.detect_conflicts() detects overlapping scheduled tasks
- DailyPlan.conflict_warnings() returns lightweight human-readable warnings
- scheduler does not crash on conflict; it reports issues instead

Filtering helpers

Owner-level task filters:
1. get_tasks_by_pet()
2. get_tasks_by_status()
3. get_pending_tasks_by_pet()
4. filter_tasks()

Explanation and reasoning

- Scheduler.provide_reasoning() now includes:

1. plan summary
2. conflict warnings
3. deferred task list


## Testing PawPal+
To run tests: 
```bash
python -m pytest
```

It covers the following tests:
- task completion toggles completed
- adding a task to a pet increases its task list
- scheduler selects tasks that fit a time budget
- daily plan separates scheduled vs deferred tasks
- completing a daily recurring task creates the next day’s occurrence
- owner filters work by pet and completion status
- sorting respects exact HH:MM preferences and morning/afternoon/evening buckets
- twice-a-day tasks expand into AM/PM instances
- DailyPlan detects overlapping scheduled tasks
- conflict warnings are generated when tasks share the same start time

My confidence level: 3/5 stars


## Features
- Greedy budget-aware task selection: fit_within_constraints() chooses pending tasks that fit the owner's daily time budget using a score-based greedy heuristic.

- Weighted task scoring: task_score() combines priority, urgency, and duration to rank tasks.

- Priority sorting: sort_by_priority() orders tasks from high to low priority.

- Time-aware ordering: sort_by_time() respects exact preferred_start_time in HH:MM, then falls back to preferred_time_of_day buckets (morning, afternoon, evening).

- Recurring task expansion: expand_recurring_tasks() converts twice-a-day tasks into separate AM/PM instances for scheduling.

- Dependency-aware ordering: order_tasks_with_dependencies() preserves simple task dependency relationships while keeping heuristic order.

- Daily plan construction: generate_daily_plan() schedules selected tasks with concrete start/end times and defers overflow tasks.

- Conflict detection: DailyPlan.detect_conflicts() finds overlapping scheduled tasks.

- Human-readable warnings: DailyPlan.conflict_warnings() and Scheduler.provide_reasoning() surface overlap warnings and reasoning for scheduling decisions.

- Pet/owner task management: Owner, Pet, and Task classes support task assignment, filtering, completion, and recurring task creation.


## Screenshot of demo
Screenshot 1
<a href="C:\Users\kawoo\OneDrive\Pictures\Screenshots\pawpal_1.png" target="_blank"><img src='C:\Users\kawoo\OneDrive\Pictures\Screenshots\pawpal_1.png' title='PawPal App 1' width='' alt='PawPal App 1' class='center-block' /></a>

Screenshot 2
<a href="C:\Users\kawoo\OneDrive\Pictures\Screenshots\pawpal_2.png" target="_blank"><img src='C:\Users\kawoo\OneDrive\Pictures\Screenshots\pawpal_2.png' title='PawPal App 2' width='' alt='PawPal App 2' class='center-block' /></a>