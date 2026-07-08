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
        core actions: -add owner, add owner schedule, add pet task prority, add pet, schedule pet tasks, edit pet task priority
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

=============================================
 TODAY'S SCHEDULE FOR CARLENE'S PETS 
=============================================

🐾 Rio (Dog):
  ⏰ 08:00 - 08:15 | [HIGH] Feed Breakfast
  ⏰ 08:15 - 08:30 | [HIGH] Feed Dinner
  ⏰ 08:30 - 09:15 | [MEDIUM] Afternoon Walk
  ⏰ 09:15 - 09:35 | [MEDIUM] Play Time
  ⏰ 09:35 - 10:00 | [LOW] Bath Time

🐾 Lupin (Dog):
  ⏰ 08:00 - 08:15 | [HIGH] Feed Breakfast
  ⏰ 08:15 - 08:30 | [HIGH] Feed Dinner
  ⏰ 08:30 - 09:15 | [MEDIUM] Afternoon Walk
  ⏰ 09:15 - 09:35 | [MEDIUM] Play Time
  ⏰ 09:35 - 10:00 | [LOW] Bath Time

🐾 Coco (Dog):
  ⏰ 08:00 - 08:15 | [HIGH] Feed Breakfast
  ⏰ 08:15 - 08:30 | [HIGH] Feed Dinner
  ⏰ 08:30 - 08:40 | [HIGH] Give Medicine
  ⏰ 08:40 - 09:00 | [MEDIUM] Play Time
  ⏰ 09:00 - 09:25 | [LOW] Bath Time

=============================================

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

These tests cover the core scheduling behaviors for PawPal+, including sorting tasks in chronological order, creating the next occurrence for recurring daily tasks, and detecting conflicts when two tasks share the same time. My confidenc level is about a 3.5 stars because so far the tests are like below and the 77% has me worried.

=================================== test session starts ====================================
platform win32 -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\carle\AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 9 items                                                                           

tests\test_pawpal_system.py .......                                                   [ 77%]
tests\tests\test_pawpal.py ..                                                         [100%]

==================================== 9 passed in 0.06s =====================================

## 📐 Smarter Scheduling

The scheduler now uses a small set of methods to turn a pet's task list into a practical daily plan.

- Sorting behavior: `Scheduler.sort_tasks()` orders tasks by priority, then duration, and `Scheduler.sort_by_time()` orders them by clock time so the plan can be reviewed chronologically.
- Filtering behavior: `Scheduler.filter_tasks()` can narrow tasks by completion status or by matching a pet name or category keyword, which helps the owner focus on the right tasks.
- Conflict detection logic: `Scheduler.detect_conflicts()` compares tasks in time order and returns a warning when one task would overlap another.
- Recurring task logic: `Task.mark_complete()` marks a task complete and, when the task is marked recurring with a daily or weekly recurrence, creates the next occurrence for the pet.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
