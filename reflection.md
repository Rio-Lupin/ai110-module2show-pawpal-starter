# PawPal+ Project 4: Reflection on AI Collaboration and System Design

## 1. Student explains how they used AI during development (prompting, debugging, design).

        I used AI during development by asking the Ai for a review of the code before i made the optimizations to remind me of the structure of the older project and to help me design the new optimizations. one thing that i also did use AI for was for debugging the streamlit connection when i added json storage. I was really helpful in figuring out what was wrong and what were my options to fix the problem.

## 2. Student identifies at least one helpful and one flawed AI suggestion.
        One helpful suggestion was helping me decide what Ai enhancements would be best for the type of program i was creating it allowed me to move on quickly to the next step. one flawed suggestion would have to be the code suggestions though they they worked and made the program function they were not user friendly. For example for entering tasks it asked the user to type each task for each pet. i had to specifically give it a list of specific tasks to make into a drop down. In addition, though the base code it gave me did create a schedule it did things like make the same task for two different pets at a different time so i had to specifically tell it that if the task, time it takes and priority are the same for 2 pets just schedule them together. 

## 3. Student reflects on system limitations and future improvements.

- The current system can schedule tasks for multiple pets and detect overlaps, but it is still fairly simple. It saves task and owner data in the JSON file, so plans can be reused after the app restarts.
- The planner uses a rule-based approach and groups similar tasks together rather than using a full optimization engine. Because of this, it may miss more complex tradeoffs such as task dependencies, transition time between activities, or partial overlaps between different task types.
- The UI allows users to enter pet tasks manually, but it still lacks edit and delete controls and only has basic validation for times, durations, and owner availability.

Future improvements:
- I have to improve the history file that saves the data because it is saving the data what is happening is the tasks from the past are also being shown. (I dont have time to fix this bug)
- Add task editing, deletion, and stronger input validation in the Streamlit interface.
- Improve the scheduling logic with blocked time ranges, task dependencies, transition time between tasks, and better multi-pet conflict resolution.
- Provide clearer planning explanations so users can understand why a task was grouped or scheduled at a specific time.

__________________________________________________________________________________________
# PawPal+ Project Reflection (Unoptimized version)

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

Yes, the design did change during implementation. one change was making the scheduler more explicit and detecting conflicts between over lapping time. This was done because it would make the design and =behavior of the app more realist to a person's physical time availablity.. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

the scheduler considers time, task priority and task duration. it also considers overlaps and avoiding scheduling conflicts. these constraints mattered the most because in order to create a simple daily schedule knowing the daily time what is the priority for these tasks and whether there were confilicts that day you would need all this information. If you were creating a schedule for a calender year you might include blocked off times, maybe a daily non-neggociable task priority for certain tasks and a way to be flexable with other tasks on a weekly basis. 

**b. Tradeoffs**

- One tradeoff my scheduler makes is that it currently checks for simple time overlaps using the start time of each task and its duration, rather than fully modeling every possible overlap pattern across multiple tasks and pets.
- - i decieded the constraints based on the fact that this program is meant to be a simple program creating a daily schedule rater than a full calender year schedule. this makes the program easier to follow, plan implement and test.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools for design brainstoming and skeleton coding. the kind of propts i found helpful were ones that were explicit to the AI on what tasks i wanted it to complete so it would not assume that i wanted it to complete tasks. I also found it helpful to ask where certain logic was located when i lost track of it.  

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment when i did not accept the AI suggestion as is is when i was developing main py. It wished to complicate the data being entered by adding multiple species when i just wished to just keep it at 1 species with the possiblity of others. If i had added other species i may have specified tasks for those specific species and that would complicate he program more.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Behaviors i tested were  sorting tasks, ordering tasks by clock time, filtering tasks by completion and detecting conflicts. These tests were important to verify if the features in scheduler were useful, to organize tasks clearly an to avoid scheduling conflicts.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident that my schedule works correctly (4 out of 5). i test the out put and the py.test does come sucessful. i think to feel more confident i would need to review the code slowly and consider other cases that might brake the program.

Some edge cases would be if there are different tasks that start at the same time, tasks that pass the availablity of the owner, different tasks that have the same priority and confirming that schedulers handles conflicts predictably.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

this the part of the project i was most satisfied with was that i was able to follow along with the UML in the begining of the project. i think this was the most pivtol task to do so that i would be able to implement the program and follow the suggestions made by the Ai and understand what what being suggested.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If i had to do another itteration of this project i would probably make it a bit more complicated by making specific tasks corrospond with specific species of pets ad having more time differences between these different species tasks to see how time cobnflict/ scheduling would be resolved in this case.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One this i learned while designing systems is the connecting of UI and backend intergation. This is one of the skills i have been really wishing to learn since it has not been taught to me in my Schooling yet. And iit is something i wish to continue practicing for my goal as a full stack developer. As for working with AI, i have learned to be more explicit in my propts though i still need to practice because some times i give vague propts.
