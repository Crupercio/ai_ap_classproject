# Week 6 Assignment — RAG Codelab + Your Own Documents


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

The codelab uses an embedding-based retriever, which is one of the two families Huyen describes. Gemini turns the question and each document into vectors, and Chroma returns the closest one. My keyword questions worked, but a term-based retriever would probably have handled them too, since words like "max ki" and "chapters" appear in the documents. It would likely do worse on question 3, where I said "shows" and "comic" but the document says "anime" and "manga." The embedding retriever still found it. It missed on question 4, though. It returned the origins document, maybe because "modeled" also appears there. A term-based retriever might have made the same mistake.



The pipeline handled the unanswerable question well. Gemini said the text did not give Gohan's exact ki, then listed Piccolo's, Vegeta's, and Goku's ki, which were all in the passage. But the prompt only says the model may ignore the passage, so it can use its own knowledge. Question 4 showed this, because Gemini added a quote that is not in any of my documents. In a real app, a confident made-up answer could mislead people. I would change the prompt to say answer only from the passages and say "I don't know" otherwise.



Switching to my documents made retrieval harder. The car documents were very different from each other, but mine share words like "Toriyama" and "manga," and only one passage was retrieved. The notebook's two models were also retired, so I had to swap them, and Gemini sometimes gave different wording on different runs.



My project does not need RAG. It is a voice message generator that takes a short audio sample and a typed message and creates new speech in that voice. That is closer to prompting a pretrained voice model than to retrieval, because the reference clip works like the prompt. The app is not looking anything up, and the user writes the whole message, so there are no documents to retrieve from.

\---

\---

