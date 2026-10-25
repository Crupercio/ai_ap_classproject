# Week 7 Assignment — Agents Course + Your Own Agent

**Chapter:** Huyen, *AI Engineering*, Ch. 6 — Agents & Memory (pg. 275–305)
**External lesson:** Hugging Face *AI Agents Course*, Unit 1: Introduction to Agents — https://huggingface.co/learn/agents-course/unit1
**Points:** 100
**Due:** End of Week 7

---

**Name:** Luis Cruz Sanchez
**Link to your Hugging Face Space:** Hugging Face Spaces was not working for me, so I ran the agent locally with Ollama (qwen2.5:7b). Code: https://github.com/Crupercio/ai_ap_classproject/blob/main/week7/agent.py. The full step logs are in the same folder (task1_log.txt, task2_log.txt, task3_log.txt).
**Link to (or screenshot of) your Unit 1 certificate:** https://github.com/Crupercio/ai_ap_classproject/blob/main/week7/cert_agentlab.png

---

## Overview

This week you'll work through the first unit of Hugging Face's free AI Agents Course, then build on it. Unit 1 covers what agents are, how LLMs act as an agent's "brain," how agents use tools, and the Think → Act → Observe cycle. It ends with building a first agent using `smolagents`, publishing it as a Hugging Face Space, and taking a quiz that earns the course's **Certificate of Fundamentals of Agents**.

Then you'll make the agent your own: give it tools that do something you care about, push it on multi-step tasks, and study how it fails.

## Learning Objectives

* Explain how an agent plans, calls tools, and uses observations to decide its next step.
* Build a working agent with multiple tools, including one you write yourself.
* Identify and categorize agent failures using the failure modes in Huyen Ch. 6.
* Decide whether an agent (as opposed to RAG or a single prompt) is the right design for a given problem.

---

## Setup

1. Create a free Hugging Face account if you don't have one.
2. Start at the Unit 1 link above and work through the unit in order.
3. When you reach the hands-on tutorial ("Let's Create Our First Agent Using smolagents"), duplicate the template Space as instructed and follow along.

If you store any access token or API key, add it as a **Space secret**, never in your code. Your Space is public, and anyone can read its files.

---

## Part 1: Complete Unit 1 and Earn the Certificate (25 pts)

Work through all of Unit 1, including the tutorial, and **pass the end-of-unit quiz** to earn the Certificate of Fundamentals of Agents. Follow the quiz link in the course itself, since the certification app has moved before.

Put the certificate link or screenshot at the top of this file.

**In 2–3 sentences, explain the Think → Act → Observe cycle in your own words, using something your agent actually did as the example:** In the Think, Act, Observe cycle, the agent first thinks about what it needs, then acts by calling a tool, then looks at the result to decide what to do next. In my Task 2, the agent thought it needed the value of a B+, so it acted by calling web_search and observed that a B+ is worth 3.3. Then it thought it was time to calculate, acted by calling gpa_calculator, observed "GPA: 3.72," and finished with final_answer.

---

## Part 2: Build Your Agent (40 pts)

Extend the agent in your duplicated Space so that it has:

* **At least 2 tools** in total
* **At least 1 custom tool that you write yourself** (not a pre-made one). Tools related to your term project are recommended, but anything useful works: a unit converter, a calculator for a formula from another class, a lookup over a small dataset, a text formatter, etc.

**Your custom tool:**

||Value|
|-|-|
|Tool name|gpa_calculator|
|What it does|Calculates a weighted GPA on a 4.0 scale from a list of letter grades and credit hours|
|Inputs and output|Inputs are two strings, grades (like "A,B+,A-") and credits (like "3,4,3"). Output is a string like "GPA: 3.72", or an error message if the lists don't match or a grade is unknown|

Paste your custom tool's code here:

```python
@tool
def gpa_calculator(grades: str, credits: str) -> str:
    """Calculates a weighted GPA on a 4.0 scale from letter grades and credit hours.
    Use this when the user wants a GPA or asks what their GPA would be.

    Args:
        grades: Comma-separated letter grades, like "A,B+,A-"
        credits: Comma-separated credit hours in the same order, like "3,4,3"
    """
    points = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
              "C+": 2.3, "C": 2.0, "C-": 1.7, "D": 1.0, "F": 0.0}
    g = [x.strip().upper() for x in grades.split(",")]
    c = [float(x) for x in credits.split(",")]
    if len(g) != len(c):
        return "Error: number of grades and credits must match."
    if any(x not in points for x in g):
        return "Error: unknown letter grade."
    total = sum(points[a] * b for a, b in zip(g, c))
    return f"GPA: {total / sum(c):.2f}"
```

**What did you write in the tool's name, description, and argument descriptions to help the agent know when and how to use it? Did you have to revise them?** I wrote the name and description to be plain about the job: the name says what it does, the first line says it calculates a weighted GPA, and the second line says when to use it. The Args section shows an example format for each input ("A,B+,A-" and "3,4,3"). I did not revise the description after testing, but I did have to revise my prompt. In all three tasks the agent formatted the inputs correctly, which suggests the example formats in the Args section worked. It did once use the calculator to look up the value of an A-, so the line about when to use it could be stronger. The weak spot was the agent's other tool. In Task 1 it made up a tool called wikipedia_search, and in Task 2 it worked once I named web_search in the prompt.

Now give your agent **3 multi-step tasks**, meaning tasks that require more than one tool call or more than one step to complete. At least one task should require using **two different tools** together.

|#|Task (short)|Tools the agent called, in order|Number of steps|Succeeded? (yes / partly / no)|
|-|-|-|-|-|
|1|Search the value of an A-, then calculate GPA for A-,B+,A with credits 3,4,3 |wikipedia_search (does not exist, failed), gpa_calculator, gpa_calculator, final_answer|4 |partly |
|2|Use web_search for the value of a B+, then calculate GPA for B+,A,A with credits 4,3,3 |web_search, gpa_calculator, final_answer |3 |yes |
|3|Use web_search for the value of a C+, then compare GPA for C+,B,A- with credits 3,3,4 and 4,4,4|web_search, (Step 2 syntax error), gpa_calculator twice, final_answer|4 |no |

---

## Part 3: Failure Analysis (15 pts)

Find **one clear failure**. If none of your tasks failed, try to make the agent fail: give it an ambiguous request, a task no tool can handle, bad input for your custom tool, or a task that needs many steps.

Paste the relevant part of the agent's step log here (trim it to the steps that matter):

```
Task: Use web_search to find the GPA value of a C+ at US colleges. Then calculate my GPA for grades C+,B,A- with credits 3,3,4, and also for grades C+,B,A- with credits 4,4,4. Tell me which GPA is higher.
----------------------------------- Step 3 ------------------------------------
+- Executing parsed code: ----------------------------------------------------+
| c_plus_gpa = 2.3                                                            |
|                                                                             |
| gpa_3_3_4 = gpa_calculator(grades="C+,C+,A-", credits="3,3,4")              |
| gpa_4_4_4 = gpa_calculator(grades="C+,B,A-", credits="4,4,4")               |
|                                                                             |
| if gpa_3_3_4 > gpa_4_4_4:                                                   |
|     higher_gpa = gpa_3_3_4                                                  |
| else:                                                                       |
|     higher_gpa = gpa_4_4_4                                                  |
|                                                                             |
| print(f"GPA for 3, 3, 4 credits: {gpa_3_3_4}")                              |
| print(f"GPA for 4, 4, 4 credits: {gpa_4_4_4}")                              |
| print(f"The higher GPA is: {higher_gpa}")                                   |
+-----------------------------------------------------------------------------+
Execution logs:
GPA for 3, 3, 4 credits: GPA: 2.86
GPA for 4, 4, 4 credits: GPA: 3.00
The higher GPA is: GPA: 3.00

Out: None
[Step 3: Duration 2.89 seconds| Input tokens: 9,808 | Output tokens: 561]
----------------------------------- Step 4 ------------------------------------
+- Executing parsed code: ----------------------------------------------------+
| final_answer("The higher GPA is 3.00")                                      |
+-----------------------------------------------------------------------------+
Final answer: The higher GPA is 3.00
[Step 4: Duration 1.13 seconds| Input tokens: 14,776 | Output tokens: 646]
```

**What went wrong?** In Step 3, I asked for the GPA of grades C+,B,A- with credits 3,3,4, but the agent called gpa_calculator with grades "C+,C+,A-". It changed the B to a C+ on its own. That gave 2.86 instead of the correct 3.07. Because of that, the agent decided the 4,4,4 credits scenario (3.00) was higher, and the real answer is that the 3,3,4 scenario is higher. The final answer looked believable, and there was no error message, so I only caught it by checking the math by hand. The agent also had a syntax error in Step 2 from naming a variable gpa_3, 3, 4, and it compared the text strings "GPA: 2.86" and "GPA: 3.00" instead of numbers.

**Which kind of failure is it, using the categories in Huyen Ch. 6? Explain why it fits that category.** This is a planning failure, and more specifically a tool use failure of the type Huyen calls "valid tool, incorrect parameter values." The agent picked a tool that exists (gpa_calculator) and gave it the right kind of parameters, a grades string and a credits string. But one value was wrong, because the B became a C+. This matches the book's own example, where lbs_to_kg is called with 100 when it should be 120. It is different from the "invalid tool" type, which is what happened in my Task 1 when the agent called wikipedia_search, a tool that does not exist. It is also different from a tool failure, because gpa_calculator did its job correctly with the input it was given. The mistake happened in the plan, before the tool ran. Printing each call's parameters, which the book recommends, is what made it visible in the log.

**What change would you make to prevent it (tool description, prompt, a new tool, a limit on steps, etc.)?** I would make three changes. First, I would add a line to the tool description that says to pass the grades exactly as the user gave them. Second, I would build a second tool that takes both scenarios in one call, so the agent does not have to retype the grades twice. Third, I would try a bigger model like qwen2.5:14b, since a 7b model is more likely to slip when it has to repeat values. I could also have the tool return a number instead of the text "GPA: 3.00," so the agent can compare results without comparing strings.

---

## Part 4: Reflection (20 pts, 250–350 words)

Answer all four:

* What did the course's explanation of agents make clearer than the textbook did, or vice versa? Point to something specific.
* How much did your tool's description matter to whether the agent used it correctly? What does that suggest about designing tools for agents?
* Last week you built a RAG pipeline. For a question like "what does our policy say about X?" versus "book me a meeting with X," which design fits each, and why?
* Your Milestone 1 is due this week. Would your project benefit from being an agent, or is a simpler design better? Justify your answer.

**Your reflection:**

Running the agent myself made the Think, Act, Observe loop clearer than reading about it. I could see the agent write code, look at what came back, and pick its next move. In Task 2 it searched first, saw that a B+ is 3.3, then moved on to the calculator. The Huyen failure categories also gave me words for what went wrong in Task 3.



My tool's description mattered, but the bigger lesson was how the agent finds tools at all. The agent always formatted the inputs to gpa_calculator the right way, and the description had example inputs. The search tool was different. In Task 1 the agent made up a tool called wikipedia_search, and in Task 2 it worked once I named web_search in the prompt. Agents only know what tool names and descriptions say, so they should be written like instructions for someone who can't ask questions.



For "what does our policy say about X?" I would use RAG, because the answer is already in documents and the system just needs to find the right passage. For "book me a meeting with X" I would use an agent, because it has to take actions like checking a calendar and creating an event, and each step depends on the last one.



For my Milestone 1 project, a simpler design is better. My app takes a typed message and a short voice sample and turns them into one audio clip. That is one model call with nothing to look up and no decisions along the way. Task 3 showed me that every extra step is another chance for a mistake, since the agent quietly changed a B to a C+ and gave me a believable wrong answer. An agent could do the same to a kid's name before the voice model hears it, so I want the exact text to go straight to the model.

---
