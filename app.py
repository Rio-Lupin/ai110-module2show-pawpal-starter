import streamlit as st
import pawpal_system
from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This page now uses the backend classes to create a pet, add care tasks, and build a daily plan.
"""
)

if "owner" not in st.session_state or st.session_state.owner is None:
    st.session_state.owner = Owner(name="Jordan")

if "current_pet" not in st.session_state or st.session_state.current_pet is None:
    st.session_state.current_pet = None

if "schedule" not in st.session_state:
    st.session_state.schedule = None

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

if st.button("Save owner"):
    st.session_state.owner.name = owner_name
    st.success(f"Owner updated to {st.session_state.owner.name}.")

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

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
    task_title = st.text_input("Task title", value="Morning walk")
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
if st.button("Generate schedule"):
    if st.session_state.current_pet is None:
        st.warning("Please add a pet before generating a schedule.")
    else:
        scheduler = Scheduler()
        st.session_state.schedule = scheduler.build_daily_plan(
            st.session_state.owner,
            st.session_state.current_pet,
            st.session_state.current_pet.get_tasks(),
        )
        st.success("Schedule generated.")

if st.session_state.schedule is not None:
    st.write(st.session_state.schedule.summarize())
    for block in st.session_state.schedule.time_blocks:
        st.write(f"{block.start_time} - {block.end_time} | [{block.task.priority.value}] {block.task.title}")
else:
    st.info("Generate a schedule to see planned tasks here.")
