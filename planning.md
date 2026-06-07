# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Off-campus housing experiences at the University of Chicago. This knowledge is valuable because official university resources provide minimal guidance on the actual experience of renting in Hyde Park and nearby neighborhoods. They don't cover landlord quality, lease gotchas, neighborhood safety nuances, utility costs, or the unwritten norms that students learn only after moving in. The information is scattered across Reddit threads, student newspapers, and niche housing platforms, making it hard to find through any single official channel.

---

## Documents


| #   | Source              | Description                                       | URL or location                                                                                                                                                                                                              |
| --- | ------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Chicago Maroon      | Article guide to navigating off-campus housing    | [https://chicagomaroon.com/40981/news/navigating-the-maze-a-guide-to-off-campus-housing/](https://chicagomaroon.com/40981/news/navigating-the-maze-a-guide-to-off-campus-housing/)                                           |
| 2   | Apartments.com      | Listings and reviews near UChicago                | [https://www.apartments.com/off-campus-housing/il/chicago/university-of-chicago/](https://www.apartments.com/off-campus-housing/il/chicago/university-of-chicago/)                                                           |
| 3   | Facebook Group      | UChicago Housing community posts                  | [https://www.facebook.com/groups/uchicagohousing/](https://www.facebook.com/groups/uchicagohousing/)                                                                                                                         |
| 4   | Maroon Housing      | Off-campus life guide                             | [https://maroonhousing.com/off-campus-life](https://maroonhousing.com/off-campus-life)                                                                                                                                       |
| 5   | Maroon Housing      | Hyde Park neighborhood guide                      | [https://maroonhousing.com/neighborhood-guide/hyde-park](https://maroonhousing.com/neighborhood-guide/hyde-park)                                                                                                             |
| 6   | For Rent University | UChicago off-campus listings and info             | [https://www.forrentuniversity.com/University-of-Chicago](https://www.forrentuniversity.com/University-of-Chicago)                                                                                                           |
| 7   | Prked.com           | Ultimate guide to UChicago off-campus housing     | [https://prked.com/post/your-ultimate-guide-to-university-of-chicago-off-campus-housing](https://prked.com/post/your-ultimate-guide-to-university-of-chicago-off-campus-housing)                                             |
| 8   | Casita              | Student accommodation guide for UChicago          | [https://www.casita.com/student-accommodation/usa/chicago/university-of-chicago](https://www.casita.com/student-accommodation/usa/chicago/university-of-chicago)                                                             |
| 9   | Uhomes              | UChicago off-campus listings and tips             | [https://en.uhomes.com/us/chicago/university-of-chicago](https://en.uhomes.com/us/chicago/university-of-chicago)                                                                                                             |
| 10  | Domu                | Hyde Park apartments near UChicago                | [https://www.domu.com/chicago/neighborhoods/hyde-park/apartments-near-university-of-chicago](https://www.domu.com/chicago/neighborhoods/hyde-park/apartments-near-university-of-chicago)                                     |
| 11  | Reddit              | What are good places to live near campus          | [https://www.reddit.com/r/uchicago/comments/1k1uoz3/what_are_some_good_places_to_live/](https://www.reddit.com/r/uchicago/comments/1k1uoz3/what_are_some_good_places_to_live/)                                               |
| 12  | UChicago GRAD       | Chicago neighborhoods guide for incoming students | [https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/other-chicago-neighborhoods/](https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/other-chicago-neighborhoods/) |
| 13  | UChicago GRAD       | Apartment listings for grad students              | [https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/apartment-listings/](https://grad.uchicago.edu/admissions/relocating-to-chicago/finding-an-apartment/apartment-listings/)                   |


---

## Chunking Strategy

**Chunk size:** 500 tokens (~2,000 characters)

**Overlap:** 50 tokens (~200 characters)

**Reasoning:** The corpus mixes short Reddit-style comments (a few sentences) with longer article sections and neighborhood guides. A 500-token chunk is large enough to capture a full thought or recommendation from a guide article without losing context, but small enough that a Reddit comment or review fits within a single chunk rather than being split. The 50-token overlap prevents key advice from being severed at a chunk boundary (for example, a sentence that starts a recommendation in one chunk and finishes it in the next will appear in both, so retrieval won't miss half the idea). HTML and boilerplate (nav menus, footers, cookie banners) will be stripped before chunking so chunks contain only substantive text.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** accuracy vs. latency. all-MiniLM-L6-v2 is fast and lightweight but was trained on general web text, so it may not capture UChicago-specific terminology as well as a larger model. A model like text-embedding-3-large (OpenAI) or e5-large-v2 would retrieve more semantically precise chunks at the cost of higher latency and API expense. Context length is not a major concern here since chunks are short (500 tokens), so models with 512-token limits are fine. Multilingual support is irrelevant for this corpus. For production I'd also consider re-ranking retrieved chunks with a cross-encoder before passing them to the LLM, which improves precision without changing the embedding model.


---

## Evaluation Plan


| #   | Question                                               | Expected answer                                                                                |
| --- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| 1   | What is the university-approved apartment near campus? | Vue53 (source: UChicago GRAD)                                                                  |
| 2   | What are the most popular apartments?                  | 5252, etc (source: Chicago Maroon)                                                             |
| 3   | Does everyone move off-campus?                         | No, some people stay on dorm (source: Chicago Maroon or Prked)                                 |
| 4   | What is the best place to live?                        | Hyde Park, most convenient and close to campus, but higher rent (source: Prked, UChicago GRAD) |
| 5   | Is it safe to live off campus?                         | Generally yes, but be aware of your surroundings (source: Maroon Housing)                      |


---

## Anticipated Challenges

1. Noisy web content can key information across chunks. Many sources (Apartments.com, Domu) intersperse listing metadata (price, sqft, amenity icons) between substantive sentences. After stripping HTML, these fragments can end up glued to real advice, diluting the semantic signal of a chunk. A retrieval query about "safety in Hyde Park" might surface a chunk that's mostly price tables with one safety-related sentence attached. It's possible that the retrieved context looks relevant by similarity score but contains little usable information.

2. Short Reddit comments can product low-density chunks. Reddit replies are often 1–3 sentences with implicit context. Because the referent lives in a parent comment that may be in a different chunk, the retrieved text will be hard for the LLM to ground into a useful answer. The model may either hallucinate the missing context or produce a vague non-answer, and it's difficult to detect this failure from retrieval scores alone.

---

## Architecture

┌─────────────────────────────────────┐
│          RAG Pipeline               │
└─────────────────────────────────────┘

  1. Document Ingestion
     ┌──────────────────────────────────┐
     │  requests + BeautifulSoup        │
     │  • Fetch HTML from 13 URLs       │
     │  • Strip nav/footer/boilerplate  │
     │  • Save raw text per source      │
     └────────────────┬─────────────────┘
                      │
  2. Chunking
     ┌────────────────▼─────────────────┐
     │  LangChain RecursiveCharacter-   │
     │  TextSplitter                    │
     │  • chunk_size = 500 tokens       │
     │  • chunk_overlap = 50 tokens     │
     │  • Attach source URL metadata    │
     └────────────────┬─────────────────┘
                      │
  3. Embedding + Vector Store
     ┌────────────────▼─────────────────┐
     │  sentence-transformers           │
     │  (all-MiniLM-L6-v2)              │
     │  • Embed each chunk              │
     │  • Store in ChromaDB (local)     │
     └────────────────┬─────────────────┘
                      │
  4. Retrieval
     ┌────────────────▼─────────────────┐
     │  ChromaDB similarity search      │
     │  • Embed user query              │
     │  • Return top-k=5 chunks         │
     │  • Include source URL metadata   │
     └────────────────┬─────────────────┘
                      │
  5. Generation
     ┌────────────────▼─────────────────┐
     │  Claude API (claude-haiku-4-5)   │
     │  • System prompt enforces        │
     │    grounding to retrieved chunks │
     │  • Response cites source URLs    │
     │  • CLI interface via input()     │
     └──────────────────────────────────┘

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**