# Week 6 Assignment — RAG Codelab + Your Own Documents

**Chapter:** Huyen, *AI Engineering*, Ch. 6 — RAG (pg. 253–274)
**External lesson:** Google \& Kaggle *5-Day Gen AI Intensive*, Day 2: Embeddings and Vector Stores — https://www.kaggle.com/learn-guide/5-day-genai
**Points:** 100
**Due:** End of Week 6

\---

## Submission Instructions

1. Copy this file into your Assignment 1 repo, keeping the filename **`week6-rag-lab.md`**.
2. Fill in every blank (`\_\_\_\_\_`) and bracketed placeholder directly in the file.
3. Make sure your Kaggle notebook is saved with its outputs showing, and that it's either public or shared with me.
4. Push your commit, then submit a link to the file as instructed for this course.

**Name:** Luis Cruz Sanchez
**Link to your completed Kaggle notebook:** https://www.kaggle.com/code/luiscruzsanchez/day-2-document-q-a-with-rag-b809ac

\---

## Overview

This week you'll work through a RAG lesson built by Google and Kaggle, then make it your own. Part 1 is completing their RAG question-answering codelab as written. In Part 2, you'll point that same pipeline at your own documents and test it with questions you write yourself. The reflection connects what you built back to Huyen's Chapter 6.

## Learning Objectives

* Build and run a working RAG pipeline: embed documents, store them, retrieve relevant passages, and generate grounded answers.
* Adapt an existing pipeline to a new set of documents.
* Evaluate retrieval separately from generation, so you can tell which part failed.
* Connect a hands-on implementation to the RAG architecture described in the textbook.

\---

## Setup

1. Open the Kaggle Learn Guide linked above and go to **Day 2**.
2. Create a free Kaggle account if you don't have one. Kaggle may ask you to verify your account with a phone number before it allows internet access in notebooks, which the codelabs need.
3. Get a free Gemini API key from Google AI Studio.
4. Store your key using **Kaggle Secrets**, as the codelab instructs. **Never paste your key into a notebook cell.** Your notebook will be shared, and anyone who sees the key can use it.

If a cell fails, check the course's troubleshooting guide for the codelabs before spending a long time debugging.

\---

## Part 1: Complete the RAG Codelab (30 pts)

Find the Day 2 codelab that builds a **RAG question-answering system over documents**. Copy it into your own Kaggle account and run it from top to bottom, with every cell executing successfully.

Record what the pipeline uses:

||Value|
|-|-|
|Embedding model|gemini-embedding-001|
|Where the embeddings are stored (vector store/database)|Chroma (an in-memory database, collection named googlecardb)|
|Generation model|gemini-3.6-flash|
|Number of passages retrieved per query|1|

**In 2–3 sentences, describe what happens between the moment a question is asked and the moment an answer comes back:** When I ask a question, the pipeline turns it into an embedding using the query mode of the embedding model. Chroma compares that embedding to the stored document embeddings and returns the closest passage. That passage gets put into a prompt along with my question and some instructions, and Gemini writes the final answer using that passage. The codelab originally used text-embedding-004 and gemini-2.0-flash, but those are no longer available, so I used gemini-embedding-001 and gemini-3.6-flash instead.

\---

## Part 2: Make It Yours (40 pts)

In your copy of the notebook, **replace the sample documents with 3–5 short documents of your own.** Documents related to your term project are recommended. Course materials, public documentation for a tool you use, or articles on a topic you know well also work. Avoid anything private or sensitive.

Keep the rest of the pipeline the same. Your notebook should show your documents, your questions, and the outputs.

**Your documents:**

||Value|
|-|-|
|What the documents are|Five short documents I wrote about Dragon Ball. They cover how the manga was made, the anime series, the main characters and their ki, behind-the-scenes facts, and the series' sales and live-action movie.|
|Number of documents|5|
|Why you chose them|Dragon Ball is a topic I know and enjoy. The documents have exact names, dates, and numbers, which made it easy to write keyword questions.|

Write **5 test questions** and run each through the pipeline. Your set must include:

* **2 keyword questions** that use exact names, terms, numbers, or codes from your documents
* **2 paraphrase questions** that ask about something in your documents without using its wording
* **1 unanswerable question** whose answer is **not** in your documents

|#|Question (short)|Type|Retrieved the right passage? (Yes / No / N/A)|Generated answer (correct / partly / wrong / correctly declined)|
|-|-|-|-|-|
|1|Vegeta's max ki|keyword|Yes|correct|
|2|Chapters in the manga|keyword|Yes|correct|
|3|Show not based on the comic|paraphrase|Yes|correct|
|4|Real-world people the alien emperor was modeled after|paraphrase|No|partly|
|5|Gohan's ki|unanswerable|N/A|correctly declined|

**Pick one question where the result wasn't fully correct (or, if everything worked, the one that came closest to failing). Was the weak point retrieval or generation? How can you tell from the notebook's output?** Question 4 was the weak point, and it was a retrieval problem. The notebook printed "Retrieved doc id: 0," which is the origins document, but the Frieza fact is in DOCUMENT4. Gemini still said Frieza was modeled after real estate speculators, which is correct, but it also added a quote about "the worst kind of people" that is not in any of my documents. So the model answered from its own knowledge and not from the retrieved passage. I could tell from the retrieval output, which showed doc id 0 and a passage starting with "Dragon Ball was created by Akira Toriyama," not the behind-the-scenes document.

\---

## Part 3: Reflection (30 pts, 250–350 words)

Answer all four:

* Huyen describes two families of retrievers: term-based and embedding-based. Which kind does the codelab use? Based on your keyword questions, where might the other kind have done better or worse?
* How did the pipeline handle your unanswerable question? What would happen in a real application if it handled that badly, and what would you change to fix it?
* The codelab was designed to work well on its own sample documents. What, if anything, got harder when you switched to yours?
* Your project evaluation plan is due next week with Milestone 1. Does your project need RAG? If so, what would the documents be, and if not, why not?

**Your reflection:**

**The codelab uses an embedding-based retriever, which is one of the two families Huyen describes. Gemini turns the question and each document into vectors, and Chroma returns the closest one. My keyword questions worked, but a term-based retriever would probably have handled them too, since words like "max ki" and "chapters" appear in the documents. It would likely do worse on question 3, where I said "shows" and "comic" but the document says "anime" and "manga." The embedding retriever still found it. It missed on question 4, though. It returned the origins document, maybe because "modeled" also appears there. A term-based retriever might have made the same mistake.**



**The pipeline handled the unanswerable question well. Gemini said the text did not give Gohan's exact ki, then listed Piccolo's, Vegeta's, and Goku's ki, which were all in the passage. But the prompt only says the model may ignore the passage, so it can use its own knowledge. Question 4 showed this, because Gemini added a quote that is not in any of my documents. In a real app, a confident made-up answer could mislead people. I would change the prompt to say answer only from the passages and say "I don't know" otherwise.**



**Switching to my documents made retrieval harder. The car documents were very different from each other, but mine share words like "Toriyama" and "manga," and only one passage was retrieved. The notebook's two models were also retired, so I had to swap them, and Gemini sometimes gave different wording on different runs.**



**My project does not need RAG. It is a voice message generator that takes a short audio sample and a typed message and creates new speech in that voice. That is closer to prompting a pretrained voice model than to retrieval, because the reference clip works like the prompt. The app is not looking anything up, and the user writes the whole message, so there are no documents to retrieve from.**

\---

\---

## Part 4: Graduate Extension — Term-Based Retrieval Comparison (20 pts)

*Graduate students required.*

In the same notebook, add a **BM25 retriever** (for example, with the `rank\_bm25` library) over the same documents. Run your 4 answerable questions through it and compare which passages it retrieves against the codelab's embedding retriever.

|#|Question (short)|Embedding retriever found it?|BM25 found it?|
|-|-|-|-|
|1|\_\_\_\_\_|\_\_\_\_\_|\_\_\_\_\_|
|2|\_\_\_\_\_|\_\_\_\_\_|\_\_\_\_\_|
|3|\_\_\_\_\_|\_\_\_\_\_|\_\_\_\_\_|
|4|\_\_\_\_\_|\_\_\_\_\_|\_\_\_\_\_|

In 200–300 words: where did the two retrievers agree and disagree, and does the pattern match what Huyen predicts for keyword versus paraphrase queries? If you were building this for real, would you use one, the other, or both?

**Your analysis:** \_\_\_\_\_

\---

## Optional (Not Graded)

If you want to go further, the rest of Day 2 is worth your time: the **Embeddings and Vector Stores whitepaper**, the summary podcast, the other two codelabs (text similarity and embedding-based classification), and the recorded livestream with Google engineers.

\---

## Grading

|Component|Undergraduate|Graduate|
|-|-|-|
|Complete the RAG codelab (Part 1)|30 pts|20 pts|
|Make it yours (Part 2)|40 pts|40 pts|
|Reflection (Part 3)|30 pts|20 pts|
|Graduate extension (Part 4)|—|20 pts|
|**Total**|**100 pts**|**100 pts**|

### Rubric

|Level|Criteria|
|-|-|
|**Full credit**|The codelab runs completely with outputs showing, and the pipeline summary is accurate. The notebook uses the student's own documents. All 5 questions are present with the required mix of types, and the retrieval-vs-generation diagnosis is supported by evidence from the notebook. Reflection connects the student's own results to Huyen Ch. 6.|
|**Partial credit**|The codelab is incomplete or outputs are missing. Sample documents were not replaced, or fewer than 5 questions are included, or the required question types are missing. The diagnosis is a guess without evidence. Reflection restates the chapter instead of the results.|
|**No credit**|Not submitted, the notebook link doesn't work or isn't shared, or results appear fabricated (e.g., table entries that don't match the notebook's outputs).|

\---

## A Note on Scope

Your pipeline won't answer everything correctly on your own documents, and that's expected. What's being graded is whether you can look at a failure and say which part of the pipeline caused it.

Also note: **Quiz 3 is this week too.** Start the codelab early, since setup (accounts, API key, phone verification) can take longer than you'd expect.

