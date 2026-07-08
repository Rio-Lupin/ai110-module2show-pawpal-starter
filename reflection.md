# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
MY Initial design:
UML will have  class owner with the responisbility of inputing schedule and adding/editing priority of pet tasks (walk, feed, bath)  under this class will be the pet class where the pet will be entered (ie name, breed and time takes for each task) Under this should be the task class where the responisiblitiies would be scheduling pet tasks based on owner class schedule/priority.

Afterwards i changed it to:

UML has  an owner class that will have their name, add availablity, add/edit preferences  and have the ablity to add a pet.
The Pet class will have the pet name, species,age and have the ablity to add a task or get the list of tasks.

The task class will have the title, category duration of the task, ppriority, whether it is reoccuring  and will get the priority score from the class priority.

There is a Time block class which will check the sart/end time, the task and if time is available

There is a schedule class will have the time blocks add tasks  while the scheduler class will build the daily plan, sort the tasks filter by the time and resolve conflicts

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- One tradeoff my scheduler makes is that it currently checks for simple time overlaps using the start time of each task and its duration, rather than fully modeling every possible overlap pattern across multiple tasks and pets.
- - i decieded the constraints based on the fact that this program is meant to be a simple program creating a daily schedule rater than a full calender year schedule. this makes the program easier to follow, plan implement and test.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
