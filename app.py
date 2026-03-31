import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler, Priority, TaskCategory

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner_vault" not in st.session_state:
    st.session_state.owner_vault = {}

if owner_name not in st.session_state.owner_vault:
    st.session_state.owner_vault[owner_name] = Owner(name=owner_name)

owner = st.session_state.owner_vault[owner_name]
scheduler = Scheduler(owner)

st.markdown("### Pets")
st.caption("Add a pet to the current owner before adding tasks.")

if st.button("Add pet"):
    if owner.get_pet(pet_name) is None:
        owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added pet {pet_name}.")
    else:
        st.warning(f"Pet {pet_name} already exists.")

pet_options = [pet.name for pet in owner.pets]
selected_pet_name = st.selectbox("Select pet", pet_options or ["No pets yet"])
selected_pet = owner.get_pet(selected_pet_name) if owner.pets else None

st.markdown("### Tasks")
st.caption("Add a few tasks and assign them to the selected pet.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if selected_pet is None:
        st.error("Please add a pet first before adding tasks.")
    else:
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=Priority[priority.upper()],
            category=TaskCategory.GENERAL,
        )
        selected_pet.add_task(task)
        st.success(f"Added task '{task_title}' to {selected_pet.name}.")

if owner.pets:
    st.write("Current pet task list:")
    for pet in owner.pets:
        st.write(f"**{pet.name} ({pet.species})**")
        tasks = pet.tasks

        sorted_tasks = None
        if hasattr(scheduler, "sort_tasks"):
            sorted_tasks = scheduler.sort_tasks(tasks)
        elif hasattr(scheduler, "get_sorted_tasks"):
            sorted_tasks = scheduler.get_sorted_tasks(tasks)
        if sorted_tasks is not None and sorted_tasks != tasks:
            tasks = sorted_tasks
            st.success(f"Tasks for {pet.name} sorted by scheduler rules.")

        filtered_tasks = None
        if hasattr(scheduler, "filter_tasks"):
            filtered_tasks = scheduler.filter_tasks(tasks)
        if filtered_tasks is not None and filtered_tasks != tasks:
            tasks = filtered_tasks
            st.success(f"Tasks for {pet.name} filtered by scheduler rules.")

        conflicts = []
        if hasattr(scheduler, "find_conflicts"):
            conflicts = scheduler.find_conflicts(tasks)
        elif hasattr(scheduler, "detect_conflicts"):
            conflicts = scheduler.detect_conflicts(tasks)
        if conflicts:
            st.warning(
                f"Task conflicts detected for {pet.name}: "
                + ", ".join(
                    [c.title if hasattr(c, "title") else str(c) for c in conflicts]
                )
            )

        if tasks:
            task_rows = [
                {
                    "No.": idx,
                    "title": t.title,
                    "duration": t.duration_minutes,
                    "priority": t.priority.value,
                    "completed": t.completed,
                }
                for idx, t in enumerate(tasks, start=1)
            ]
            st.table(task_rows)
        else:
            st.info("No tasks yet for this pet.")
else:
    st.info("No pets found. Add a pet above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule from the current owner's tasks.")

if st.button("Generate schedule"):
    if not owner.pets:
        st.error("Add at least one pet with tasks before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        if "daily_time_budget" not in owner.preferences:
            owner.update_time_budget(120)
        plan = scheduler.generate_daily_plan()
        st.success("Schedule generated.")
        st.text(scheduler.provide_reasoning(plan))
