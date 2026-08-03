import os
import streamlit as st
from datetime import datetime
import json
import sys

workspace_root = os.getcwd()
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

import pawpal_system
from pawpal_system import (
    DataStore,
    ExplanationEngine,
    Owner,
    Pet,
    PlannerAgent,
    PlanningWorkflow,
    Priority,
    ReliabilityManager,
    Scheduler,
    Task,
    TaskHistory,
    TaskRecord,
)

DataStore = getattr(pawpal_system, "DataStore", None)
if DataStore is None:
    debug_import_error = "DataStore not found on pawpal_system module after import"
else:
    debug_import_error = None


def _debug_pawpal_system():
    return {
        "cwd": __import__("os").getcwd(),
        "sys_path_0": sys.path[0],
        "sys_path": sys.path[:5],
        "pawpal_system_file": getattr(pawpal_system, "__file__", None),
        "has_DataStore_attr": hasattr(pawpal_system, "DataStore"),
        "DataStore_value": repr(DataStore),
        "import_error": debug_import_error,
    }

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This page now uses the backend classes to create a pet, add care tasks, and build a daily plan.
"""
)

with st.expander("Debug: pawpal_system import info"):
    debug_info = _debug_pawpal_system()
    st.json(debug_info)

data_store = DataStore()
loaded = data_store.load()
st.session_state.last_loaded_date = None
if "owner" not in st.session_state or st.session_state.owner is None:
    if loaded is not None:
        st.session_state.owner, st.session_state.history, metadata = loaded
        st.session_state.last_loaded_date = metadata.get("last_date")
    else:
        st.session_state.owner = Owner(name="Jordan")

if "current_pet" not in st.session_state or st.session_state.current_pet is None:
    st.session_state.current_pet = None

if "schedule" not in st.session_state:
    st.session_state.schedule = None

if "history" not in st.session_state:
    if loaded is not None:
        st.session_state.owner, st.session_state.history, metadata = loaded
        st.session_state.last_loaded_date = metadata.get("last_date")
    else:
        st.session_state.history = TaskHistory()

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

current_date = datetime.now().strftime("%Y-%m-%d")
if st.session_state.last_loaded_date and st.session_state.last_loaded_date != current_date:
    for pet in st.session_state.owner.pets:
        for task in pet.tasks:
            if task.last_completed_date == st.session_state.last_loaded_date:
                task.is_complete = False
    st.session_state.last_loaded_date = current_date

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
col_a, col_b = st.columns(2)
with col_a:
    available_start = st.time_input(
        "Available start",
        value=datetime.strptime(st.session_state.owner.available_start, "%H:%M").time(),
    )
with col_b:
    available_end = st.time_input(
        "Available end",
        value=datetime.strptime(st.session_state.owner.available_end, "%H:%M").time(),
    )

if st.button("Save owner"):
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_start = available_start.strftime("%H:%M")
    st.session_state.owner.available_end = available_end.strftime("%H:%M")
    st.session_state.schedule = None
    st.success(f"Owner updated to {st.session_state.owner.name}.")

if st.button("Save data"):
    current_date = datetime.now().strftime("%Y-%m-%d")
    data_store.save(st.session_state.owner, st.session_state.history, last_date=current_date)
    st.session_state.last_loaded_date = current_date
    st.success("Saved owner, pets, tasks, and history to pawpal_data.json.")

if st.button("Load saved data"):
    loaded_data = data_store.load()
    if loaded_data is None:
        st.warning("No saved data found or file was invalid.")
    else:
        st.session_state.owner, st.session_state.history, metadata = loaded_data
        st.session_state.current_pet = st.session_state.owner.pets[0] if st.session_state.owner.pets else None
        st.session_state.schedule = None
        st.session_state.last_loaded_date = metadata.get("last_date")
        st.success("Loaded saved owner and pet data from pawpal_data.json.")

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat"])

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(new_pet)
    st.session_state.current_pet = new_pet
    st.session_state.schedule = None
    st.success(f"Added {new_pet.name} to {st.session_state.owner.name}'s pets.")

if st.session_state.current_pet is not None:
    st.info(f"Current pet: {st.session_state.current_pet.name} ({st.session_state.current_pet.species})")
else:
    st.info("Add a pet to begin building tasks.")

st.divider()

st.subheader("Add a Task")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.selectbox(
        "Task title",
        [
            "Morning Walk",
            "Breakfast",
            "Dinner",
            "Afternoon Walk",
            "Medicine",
            "Grooming",
            "Play Time",
            "Bath",
            "Nail Trim",
            "Litter Change",
            "Clean Litter",
        ],
        index=0,
    )
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.current_pet is None:
        st.warning("Please add a pet before adding tasks.")
    else:
        task = Task(
            title=task_title,
            category="general",
            duration_minutes=int(duration),
            priority=Priority[priority.upper()],
        )
        st.session_state.current_pet.add_task(task)
        st.session_state.schedule = None
        st.success(f"Added task: {task.title}")

if st.session_state.current_pet is not None and st.session_state.current_pet.get_tasks():
    scheduler = Scheduler()
    sorted_tasks = scheduler.sort_by_time(st.session_state.current_pet.get_tasks())
    filtered_tasks = scheduler.filter_tasks(sorted_tasks, pet_name="feed")

    st.success(f"{len(sorted_tasks)} task(s) loaded for {st.session_state.current_pet.name}.")
    st.caption("Tasks are sorted by time and grouped for review.")

    st.subheader("Scheduled Tasks")
    task_rows = [
        {
            "title": task.title,
            "time": task.time,
            "duration_minutes": task.duration_minutes,
            "priority": task.priority.value,
        }
        for task in sorted_tasks
    ]
    st.table(task_rows)

    if filtered_tasks:
        st.subheader("Feeding Focus")
        st.table(
            [
                {
                    "title": task.title,
                    "time": task.time,
                    "priority": task.priority.value,
                }
                for task in filtered_tasks
            ]
        )
    else:
        st.info("No feeding-related tasks to display.")

    conflict_warning = scheduler.detect_conflicts(sorted_tasks)
    if conflict_warning:
        st.warning(conflict_warning)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("The planner now uses a multistep workflow with history-aware prioritization and overlap repair.")
if st.button("Generate schedule"):
    if st.session_state.current_pet is None and not st.session_state.owner.pets:
        st.warning("Please add a pet before generating a schedule.")
    else:
        agent = PlannerAgent()
        if len(st.session_state.owner.pets) > 1:
            st.session_state.schedule = agent.plan_owner_schedule(
                st.session_state.owner,
                st.session_state.history,
            )
            st.session_state.explanation = agent.explain_plan(st.session_state.schedule, st.session_state.history)
            st.success("AI-enhanced owner-wide schedule generated for all pets.")
        else:
            pet = st.session_state.current_pet or st.session_state.owner.pets[0]
            st.session_state.schedule = agent.plan_daily_schedule(
                st.session_state.owner,
                pet,
                pet.get_tasks(),
                st.session_state.history,
            )
            st.session_state.explanation = agent.explain_plan(st.session_state.schedule, st.session_state.history)
            st.success("AI-enhanced schedule generated.")

if st.session_state.schedule is not None:
    st.write(st.session_state.schedule.summarize())
    if st.session_state.explanation:
        st.info(st.session_state.explanation)

    grouped_blocks = {}
    for block in st.session_state.schedule.time_blocks:
        key = (block.start_time, block.end_time, block.task.title, block.task.priority.value)
        if key not in grouped_blocks:
            grouped_blocks[key] = []
        if block.pet is not None:
            grouped_blocks[key].append(block.pet.name)

    for (start_time, end_time, title, priority_value), pet_names in grouped_blocks.items():
        pet_label = ""
        if pet_names:
            pet_label = " · " + ", ".join(sorted(set(pet_names)))
        st.write(f"{start_time} - {end_time} | [{priority_value}] {title}{pet_label}")
else:
    st.info("Generate a schedule to see planned tasks here.")

st.divider()
st.subheader("Planning Notes")
if st.button("Record completed task"):
    if st.session_state.current_pet is None:
        st.warning("Please add a pet before recording task history.")
    else:
        latest_task = st.session_state.current_pet.get_tasks()[-1] if st.session_state.current_pet.get_tasks() else None
        if latest_task is None:
            st.warning("No task to record yet.")
        else:
            st.session_state.history.add_record(
                TaskRecord(
                    task_title=latest_task.title,
                    completed_date=pawpal_system.datetime.now().strftime("%Y-%m-%d"),
                    category=latest_task.category,
                    pet_name=st.session_state.current_pet.name,
                )
            )
            st.success(f"Recorded {latest_task.title} in task history.")

if st.session_state.history.records:
    st.caption("Recent planning history")
    history_rows = [
        {
            "pet": record.pet_name,
            "task": record.task_title,
            "date": record.completed_date,
        }
        for record in st.session_state.history.records
    ]
    st.table(history_rows)
