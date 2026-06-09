# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Off-campus housing experiences at the University of Chicago. This knowledge is valuable because official university resources provide minimal guidance on the actual experience of renting in Hyde Park and nearby neighborhoods. They don't cover landlord quality, lease gotchas, neighborhood safety nuances, utility costs, or the unwritten norms that students learn only after moving in. The information is scattered across Reddit threads, student newspapers, and niche housing platforms, making it hard to find through any single official channel.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #   | Source         | Description                                       | URL or location                                                                                                                                                                                                              |
| --- | -------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Chicago Maroon | Article guide to navigating off-campus housing    | [https://chicagomaroon.com/40981/news/navigating-the-maze-a-guide-to-off-campus-housing/](https://chicagomaroon.com/40981/news/navigating-the-maze-a-guide-to-off-campus-housing/)                                           |
| 2   | Apartments.com | Listings and reviews near UChicago                | [https://www.apartments.com/off-campus-housing/il/chicago/university-of-chicago/](https://www.apartments.com/off-campus-housing/il/chicago/university-of-chicago/)                                                           |
| 3   | Maroon Housing | Off-campus life guide                             | [https://maroonhousing.com/off-campus-life](https://maroonhousing.com/off-campus-life)                                                                                                                                       |
| 4   | Maroon Housing | Hyde Park neighborhood guide                      | [https://maroonhousing.com/neighborhood-guide/hyde-park](https://maroonhousing.com/neighborhood-guide/hyde-park)                                                                                                             |
| 5   | Prked.com      | Ultimate guide to UChicago off-campus housing     | [https://prked.com/post/your-ultimate-guide-to-university-of-chicago-off-campus-housing](https://prked.com/post/your-ultimate-guide-to-university-of-chicago-off-campus-housing)                                             |
| 6   | Casita         | Student accommodation guide for UChicago          | [https://www.casita.com/student-accommodation/usa/chicago/university-of-chicago](https://www.casita.com/student-accommodation/usa/chicago/university-of-chicago)                                                             |
| 7   | Uhomes         | UChicago off-campus listings and tips             | [https://en.uhomes.com/us/chicago/university-of-chicago](https://en.uhomes.com/us/chicago/university-of-chicago)                                                                                                             |
| 8   | Domu           | Hyde Park apartments near UChicago                | [https://www.domu.com/chicago/neighborhoods/hyde-park/apartments-near-university-of-chicago](https://www.domu.com/chicago/neighborhoods/hyde-park/apartments-near-university-of-chicago)                                     |
| 9   | Reddit         | What are good places to live near campus          | [https://www.reddit.com/r/uchicago/comments/1k1uoz3/what_are_some_good_places_to_live/](https://www.reddit.com/r/uchicago/comments/1k1uoz3/what_are_some_good_places_to_live/)                                               |
| 10  | UChicago GRAD  | Chicago neighborhoods guide for incoming students | [https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/other-chicago-neighborhoods/](https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/other-chicago-neighborhoods/) |
| 11  | UChicago GRAD  | Apartment listings for grad students              | [https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/apartment-listings/](https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/apartment-listings/)                   |


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 tokens (~2,000 characters)

**Overlap:** 50 tokens (~200 characters)

**Why these choices fit your documents:** The corpus mixes short Reddit-style comments (a few sentences) with longer article sections and neighborhood guides. A 500-token chunk is large enough to capture a full thought or recommendation from a guide article without losing context, but small enough that a Reddit comment or review fits within a single chunk rather than being split. The 50-token overlap prevents key advice from being severed at a chunk boundary (for example, a sentence that starts a recommendation in one chunk and finishes it in the next will appear in both, so retrieval won't miss half the idea). HTML and boilerplate (nav menus, footers, cookie banners) will be stripped before chunking so chunks contain only substantive text.

In addition to the cleaning pipeline, I also manually processed the documents by removing irrelevant passages and cleaning the text (especially for the Reddit forum) so only the relevant part remains. 

**Final chunk count:** 264

**Sample chunks with sources**:
Chunk #238 | ID: uhomes_51 | Source: Uhomes
in UChicago, so it is not easy to rent UChicago graduate student housing . Most people rent their University of Chicago graduate housing with friends or classmates. Here are the search processes for finding UChicago graduate housing . Once you decide how much you can afford and what kinds of housing near University of Chicago you are looking for, the easiest place to start is with online listings, uhomes.com provides apartments near UChicago Hyde Park or other neighbourhoods. Size, location,

Chunk #167 | ID: ugrad_guide_10 | Source: Ugrad Guide
Transportation Besides walking or biking, the University offers a variety of transit options. During the day, the Chicago Transit Authority (CTA) operates two routes (#171 and #172), which are free to University students and employees. In addition, the University provides several shuttle routes, distinctive white buses which start from the center of campus and run various routes around Hyde Park, North Woodlawn, and South Kenwood. A convenient transit app

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast and lightweight but was trained on general web text, so it may not capture UChicago-specific terminology as well as a larger model. A model like text-embedding-3-large (OpenAI) or e5-large-v2 would retrieve more semantically precise chunks at the cost of higher latency and API expense. Context length is not a major concern here since chunks are short (500 tokens), so models with 512-token limits are fine. Multilingual support is irrelevant for this corpus. For production I'd also consider re-ranking retrieved chunks with a cross-encoder before passing them to the LLM, which improves precision without changing the embedding model.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

I added system prompt to ensure grounding (only use the context instead of general knowledge). I also ensured that citations were included with every response. 

**System prompt grounding instruction:** Answer questions about UChicago off-campus housing using only the references provided in the context below. Do not use your general knowledge. Always state which source the information comes from, using the source name shown in brackets in the context. Example: 'According to Chicago Maroon, ...' If the answer is not present in the provided excerpts, say: 'I don't see that covered in the loaded rules.'

**How source attribution is surfaced in the response:** Each response includes a note like "According to..." as well as the name of the source file in brackets at the end of the sentence. 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Does everyone live off-campus at UChicago? | Most people do, but not every | According to [Maroon Housing Life] and [Maroon Housing Hyde Park], living off campus is a common part of life for people connected to the University of Chicago, but it is not stated that everyone lives off-campus. The texts indicate that there is a mix of students, professionals, families, and long-time residents living in the neighborhoods surrounding the university, suggesting that off-campus housing is an option, but not necessarily the only option. | relevant | accurate |
| 2 | What are some of the attractions near Hyde Park? | Jackson Park, Promontory Point, etc. | According to Maroon Housing Hyde Park, some attractions near Hyde Park include Valois Restaurant, Jackson Park (which is home to the Osaka Garden and SKYLANDING, Yoko Ono's first permanent public art installation in the United States), and Promontory Point. Additionally, according to Uhomes, attractions in the area include museums, restaurants, the 57th Street Art Fair, historical sights, the Hyde Park Jazz Festival, movies, concerts, and plays. Furthermore, according to Ugrad Guide, the area is also home to the Museum of Art, the Renaissance Society, and the Oriental Institute. | relevant | accurate |
| 3 | How do students get groceries at Hyde Park? | Hyde park produce, trader joes, target, etc.| According to Chicago Maroon, students can get groceries at stores such as Hyde Park Produce, Target, Trader Joe's, Whole Foods, or Open Produce. [Chicago Maroon] Additionally, Ugrad Guide mentions that 53rd Street, Hyde Park's main retail district, has stores including Hyde Park Produce. [Ugrad Guide] | relevant | accurate |
| 4 | What is the average price of a studio apartment in Hyde Park? | ~\$1100/month | According to Chicago Maroon, the average rent for a studio apartment in Hyde Park is \$1,119. Additionally, Prked Com states that the average rent for a studio apartment in Hyde Park is ~\$1,100 - \$1,600/month. | relevant | accurate |
| 5 | Is it safe to live off-campus in Hyde Park? | generally yes | According to [Prked Com], thousands of students live off-campus in Hyde Park and have a perfectly safe and positive experience, as long as they use common sense and take advantage of the university's safety resources. Additionally, [Maroon Housing Hyde Park] states that Hyde Park is generally considered a safe, residential neighborhood with a strong community presence. [Uhomes] also mentions that Hyde Park is a safe neighborhood near the University of Chicago. Therefore, it appears that living off-campus in Hyde Park can be safe. | relevant | accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What is the most popular off-campus apartment at UChicago?

**What the system returned:** I don't see that covered in the loaded rules. The provided excerpts do not mention the most popular off-campus apartment at UChicago. According to Uhomes, they offer a range of affordable UChicago off-campus housing options, but they do not specify which one is the most popular.

**Root cause (tied to a specific pipeline stage):** Retrieval. The UGrad guide does mention that Vue53 is the most popular off-campus apartment. There are also other apartment names that are frequently mentioned, but the relevant chunks were not retrieved. 

**What you would change to fix it:** I would implement hybrid search with semantic + keyword match so words like "popular" can be pinpointed exactly. Because generic words like "apartments" are frequently seen throughout all the sources, they could lead to confusion and irrelevant search results if a question isn't super specific or require deeper understanding of the context. 

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The architecture of the RAG pipeline helped with structuring the parsing the code. I modeled the process off of the tinker lab but had to make adjustments due to the manual verification needed during the retrieval stage and the chunking stage. Having the spec helped with keeping everything organized. 

**One way your implementation diverged from the spec, and why:** I generally followed the spec, except I came up with better eval questions after the initial planning. The chunking size and overlap I came up with initially turned out to work quite well. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I asked Claude to help implement the chunking function, given the chunking size and the overlap. 
- *What it produced:* It suggested using the RecursiveCharacterTextSplitter from LangChain which was very helpful. It also helped write a function that saved the chunks in a readable format for verification purposes. 
- *What I changed or overrode:* I added a main function so the chunks can be processed and saved for the next stage. 

**Instance 2**

- *What I gave the AI:* I asked Claude to help build the chatbot interface with Gradio. I fed the general structure, the system prompt I was looking for, and the model I chose to use. 
- *What it produced:* I had a simple interface and a working chatbot pipeline. 
- *What I changed or overrode:* I added sample questions to the Gradio interface and supplemented the pipeline with an ingestion script (whic includes a cache) so the entire process can be run from beginning to end in `app.py`. 
