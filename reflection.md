# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

A system where a Scheduler takes owner constraints, pet information, and a set of care Tasks, then produces an optimized plan by respecting time availability and task priorities.


- What classes did you include, and what responsibilities did you assign to each?

Owner: Stores owner name, available daily time budget and manage owner preferneces/ constraints.

Pet: Store pet info (name, species). Track pet-specific requirements

Task: Store task details: name, duration (minutes), priority level, category (walk/feed/med). Support updating task attributes

Scheduler: Accept owner, pet, and list of tasks as input. Implement scheduling algorithm (sort by priority, fit within time constraints). Generate a daily plan with task timing. Provide reasoning for placement decisions

DailyPlan: Store scheduled tasks with assigned times. Track which tasks fit and which were deferred. Provide explanation of scheduling decisions

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Added pet_name: Optional[str] to Task:
Why: explicit owner/pet task linkage, ready for multi-pet support.

Added tasks: List["Task"] to Pet, plus add_task/remove_task stubs:
Why: captures direct Pet-to-Task relationship.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler uses a greedy score-based selection instead of trying to compute a mathematically optimal task subset.

- Why is that tradeoff reasonable for this scenario?

pet care schedules usually have only a handful of tasks each day, so a fast heuristic is more practical than a complex optimizer.

It keeps the system easier to understand and maintain, while still producing a good daily plan for an owner who needs quick, reliable recommendations rather than perfect optimization.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used copilot and its respective tools to build, understand and implement necessary code to build the Pawpal app.

The prompts to explain the code and build test cases were very helpful

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

Suggested some code for sorting which was too complicated and was making extra unnecessary code

- How did you evaluate or verify what the AI suggested?

Used the explain model to explain the code  and helped me evaluate its necessity and accuracy
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

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

- Why were these tests important?
Helped me cover all possible bases and situations the app could be used for

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am about 70% confident my scheduler works correctly

- What edge cases would you test next if you had more time?

I am not too sure

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Comparing my implemented code with the UI to see how related and correctly it works

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

My tasks list is a bit confusing. My schedule as well as is a bit too hard to understand.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is not always right. It tends to overly complicate a simple task and does not have a lot of precision.
