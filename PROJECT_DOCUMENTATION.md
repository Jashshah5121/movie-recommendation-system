# 🏛️ System Design & User Flow: MovieHub AI

This document details the architectural decisions, data flow, and user journey that power MovieHub AI. The objective of this system is to bridge raw machine learning (NLP/Embeddings) with a seamless, highly responsive web interface.

## 1. High-Level Architecture

The system enforces a strict separation of concerns. The React frontend never communicates directly with TMDB or the AI models; all traffic is routed through the FastAPI backend to ensure security, rate-limiting, and data enrichment.

```text
                      [ USER ]
                         │
                 (React Frontend)
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
 [Search API]     [Discover API]   [Recommendation API]
      │                  │                  │
      └──────────────────┼──────────────────┘
                         │
                 (FastAPI Backend)
                         │
     ┌───────────┬───────┴─────┬────────────┐
     │           │             │            │
[TMDB API]  [SQLite DB]   [AI Models]  [Similarity Engine]
```
## 2. The User Journey & System Data Flow

The application is designed around specific user flows, ensuring that every interaction is backed by either real-time TMDB data or our custom machine learning pipeline.

### A. Onboarding Flow (Cold Start Solution)
To solve the "cold start" problem for new users, the application utilizes a soft-onboarding process.
* **Initial Visit:** When a user first opens MovieHub, the React frontend initializes a local session state.
* **Preference Gathering:** The user is prompted to select 3-5 favorite genres or benchmark movies.
* **State Storage:** These initial preferences are stored via the React Context API and `localStorage`.
* **Immediate Value:** The frontend immediately dispatches these preferences to the FastAPI backend, which returns a curated initial feed, bypassing an empty state.

### B. Homepage Flow
The Homepage is designed to be highly dynamic, acting as the primary discovery hub.
* **Hero Banner Initialization:** Upon loading, the backend fetches the current most popular movie from TMDB and serves it to the frontend as the Hero Banner (including hi-res backdrop, rating, and trailer links).
* **Category Fetching:** Concurrent Axios requests are dispatched to fetch distinct categories: Trending, Popular, Upcoming, and Top Rated.
* **Rendering:** The React UI renders these as horizontal scrollable carousels.
* **Interaction:** Clicking any movie card pushes the TMDB ID to the Details route, where the backend fetches full cast, crew, and similar movie metadata.

### C. Discover Flow (Advanced Filtering)
The Discover page bypasses standard API limitations by querying the local, cleaned dataset.
* **User Input:** The user adjusts filters on the React UI (e.g., Genre = "Sci-Fi", Minimum Rating = 8.0, Language = "English").
* **API Request:** Axios sends a parameterized `GET` request to the `/discover` endpoint.
* **Database Query:** FastAPI intercepts the request, sanitizes the inputs, and executes a dynamic SQL query against the local SQLite database.
* **Response:** Results are paginated and sent back to the frontend to render the movie cards, ensuring instantaneous filtering without relying on third-party API rate limits.

### D. AI Recommendation Search Flow
This is the core engineering feature of MovieHub AI, allowing semantic, natural language searches.
* **Natural Language Query:** The user enters a descriptive query (e.g., "Movies about space travel and time dilation").
* **Vectorization:** The backend receives the text and passes it through `SentenceTransformers`, converting the English string into a high-dimensional vector array (e.g., `[0.23, 0.71, 0.55...]`).
* **Matrix Comparison:** This query vector is compared against the pre-computed cosine similarity matrix (`similarity.pkl`) containing every movie in the local dataset.
* **Hybrid Scoring:** Matches are ranked by semantic similarity, then weighted by TMDB popularity to ensure high-quality suggestions.
* **Explainable AI:** The backend cross-references the metadata of the matched movies against the query to generate "Why?" tags (e.g., *95% Match: Space Adventure, Psychological*).
* **Delivery:** The enriched payload is sent to the frontend, displaying highly accurate, context-aware results.

### E. Wishlist System
The Wishlist is engineered for speed and persistence without requiring user authentication.
* **State Management:** Built entirely on the React Context API.
* **Interaction:** When a user clicks the "Heart" icon on a movie card, the movie object is immediately pushed to the global state array.
* **UI Updates:** The navigation bar's Wishlist counter increments instantly, and the heart icon animates to a filled state.
* **Persistence:** The Context provider is synced with the browser's `localStorage`. If the user refreshes or closes the tab, the wishlist is rehydrated upon the next visit.

### F. Wishlist-Driven AI Recommendations
MovieHub AI leverages the user's saved items to generate personalized suggestions.
* **Trigger:** When the user navigates to their profile or a specific "Recommended for You" tab, the frontend gathers all Movie IDs currently in the Wishlist.
* **Batch Request:** A `POST` request is sent to the backend containing this array of IDs.
* **Centroid Calculation:** The FastAPI backend retrieves the vector embeddings for all wishlisted movies and calculates the centroid (the mathematical average of all vectors). This creates a unique "User Taste Vector."
* **Similarity Search:** The engine runs a cosine similarity search comparing this custom Taste Vector against the entire movie database.
* **Filtering:** Movies already in the user's Wishlist are stripped from the results.
* **Delivery:** A highly personalized list of movies that blend the genres, themes, and tones of everything they have liked is returned to the UI.

---

## 3. DevOps & Deployment Architecture

### The 100MB Git Limit & Automated Cloud Fetching
A major challenge in deploying ML projects via version control is the file size limit. The pre-computed cosine similarity matrix (`similarity.pkl`) is ~400MB.

Instead of compromising on model complexity, the Dockerized backend features a boot-time safety check:
1. `docker-compose up` triggers the backend container.
2. An initialization script checks for the existence of `similarity.pkl`.
3. If missing, a Python stream pulls the `.pkl` file from a hosted cloud environment (Google Drive).
4. Once downloaded and verified, the Uvicorn FastAPI server starts.

This ensures the repository remains lightweight while supporting heavy-duty ML inference in a fully containerized, plug-and-play environment.

## 4. Data Architecture & Preprocessing

The performance of any AI recommendation system fundamentally depends on the quality of its underlying data. MovieHub AI utilizes a **hybrid data strategy**, combining static pre-processed datasets with real-time API integrations.

### A. Data Collection Strategy
Instead of relying on manual entry, the system's foundational data is sourced from **The Movie Database (TMDB)**.
* **Static Metadata Collection:** During development, core attributes (Titles, Genres, Overviews, Cast, Crew, Languages, Release Dates) were collected, cleaned, and structured to train the recommendation engine.
* **Dynamic Data Fetching:** For volatile data (Trending Movies, Trailers, Live Ratings, and TMDB's native similar-movie recommendations), the FastAPI backend queries TMDB REST APIs in real-time. This guarantees the UI always reflects the current cinematic landscape without requiring constant local database updates.

### B. Data Preprocessing Pipeline
Raw datasets contain noise and irrelevant columns. A rigorous preprocessing pipeline was executed before generating the AI models:
* **Data Cleaning:** Removed duplicate records, handled missing values (NaNs), and standardized text formatting.
* **Feature Engineering:** Extracted high-value features and dropped redundant data.
* **Metadata Consolidation:** The most critical step for the NLP engine. Attributes like *Overview, Genres, Keywords, Top Cast, and Director* were merged into a single, comprehensive text string for each movie. This dense textual representation provides the `SentenceTransformers` with the context needed to calculate highly accurate semantic similarities.

### C. Artifact Generation & Storage
While development utilized raw, heavy CSV files, production deployment is highly optimized to save space and compute time. Post-processing, the application requires only three core artifacts:
1. `similarity.pkl`: The serialized matrix of cosine similarity scores (fetched dynamically via cloud at boot).
2. `metadata.csv`: A lightweight reference file containing essential mapping data.
3. `movies.db`: The structured relational database.

### D. SQLite Database (The Discover Engine)
The cleaned, structured subset of the movie dataset is loaded into a local SQLite database (`movies.db`).
* **Schema Highlights:** Stores optimized, indexed columns like `Movie ID`, `Title`, `Genres`, `Language`, `Ratings`, and `Release Date`.
* **Purpose:** It acts as the backbone for the Discover page's advanced multi-parameter filtering.
* **System Advantages:** By querying SQLite locally rather than hitting TMDB for complex filters, the system achieves near-zero network latency, bypasses third-party API rate limits, and delivers instantaneous, paginated results to the React frontend.

## 5. APIs Used
 
### TMDB APIs
 
| Purpose | Endpoint |
|---|---|
| Popular Movies | `/movie/popular` |
| Trending | `/trending/movie/week` |
| Upcoming | `/movie/upcoming` |
| Top Rated | `/movie/top_rated` |
| Movie Details | `/movie/{id}` |
| Videos | `/movie/{id}/videos` |
| Credits | `/movie/{id}/credits` |
| Recommendations | `/movie/{id}/recommendations` |
| Search | `/search/movie` |
| Autocomplete | `/search/movie` (top results only) |
 
### Internal Backend APIs
 
```
/movies
/movie/{id}
/discover
/search
/search/autocomplete
/recommendations
/movies/{id}/similar
/ai-recommend
```
 
The frontend only ever talks to these internal endpoints — the backend owns all communication with TMDB and the local database.
 
---

## 6. Search Systems
 
MovieHub AI has **three** distinct search systems:
 
### 6.1 Normal Search
 
```
Search → Backend → TMDB Search → Results
```
 
Uses the TMDB Search API directly.
 
### 6.2 Live Autocomplete
 
```
Typing → Backend → TMDB Search → Top 8 Matches → Dropdown Suggestions
```
 
Features:
- Live typing with debouncing
- Poster + movie year in suggestions
- Keyboard navigation
- Instant navigation on click
- 
### 6.3 AI Search (the project's strongest feature)
 
Instead of typing an exact movie name, users can type things like:
- *"Movie where toys come alive"*
- *"Movies like Avatar"*
- *"Tom Cruise action movie"*
- *"Man living in jungle with animals"*
The backend interprets the query intent and returns intelligent, semantically matched recommendations.
 
### 🖼️ AI Recommend — Natural Language Search
 
Example: querying **"man living in jungle with animals"** correctly resolves intent as `DESCRIPTION` and surfaces *The Jungle Book* with a 98% semantic match, tagged as matched via **Semantic Search**.
  
---
 
## 7. AI Recommendation System (Core Engine)
 
Unlike simple keyword search, MovieHub AI uses a **hybrid recommendation** approach.
 
**Step 1** — User enters a query, e.g. `Interstellar` or `Movie like Inception`.
 
**Step 2** — Backend classifies intent:
- Movie name?
- Actor?
- Director?
- Natural language description?
**Step 3** — Movie metadata is gathered: title, genres, keywords, overview, tagline, cast, director, language, popularity, rating.
 
**Step 4** — Sentence Transformers convert text into embeddings:
 
```
Interstellar → [0.23, 0.71, 0.55, ...]
```
 
**Step 5** — Cosine similarity is calculated between the user's query vector and all movie vectors.
 
**Step 6** — Top similar vectors are selected.
 
**Step 7** — Results are enriched with live TMDB data and returned to the frontend.
 
### AI Models Used
 
| Component | Purpose |
|---|---|
| **Sentence Transformers** | Semantic understanding — converts overview, genre, keywords, and cast into embeddings |
| **Cosine Similarity** | Compares vectors; higher similarity → higher recommendation score |
| **Hybrid Ranking** | Combines semantic score + TMDB popularity + ratings + release recency for final ordering |
 
### Recommendation Pipeline
 
```
Movie Metadata + Overview + Genres + Actors + Keywords + Embeddings
        ↓
  Cosine Similarity
        ↓
     Ranking
        ↓
 Recommendation
```
 
---
 
## 8. Explainable AI
 
Every AI recommendation explains **why** it was suggested — not just a black-box score.
 
Example for a 95% match:
- Same genre
- Similar theme
- Strong female lead
- Space adventure
- Psychological thriller
This transparency helps users trust and understand *why* a movie was recommended, rather than receiving an opaque ranked list.
 
---
 
## 9. Similar Movies Engine
 
```
Movie Details Page → Movie ID → TMDB Similar API → Recommended Movies
```
 
---
 
## 8. Trailer System
 
```
Movie → Video API → YouTube Trailer
```
 
Trailers open in a **new browser tab** rather than an embedded iframe, keeping the main experience uninterrupted.
 
---
 
## 9. Wishlist System
 
Built entirely on the frontend using **React Context API** — no backend required.
 
Features:
- Add / remove movies
- Persistence across sessions
- Heart animation
- Live counter in the nav bar
---
## 15. Dockerization
 
```
Docker Compose
      ↓
Frontend Container + Backend Container
      ↓
  Networked Together
```
 
A single command — `docker compose up` — starts the complete application with the frontend and backend connected automatically.
 
---
 
## 16. Unique Features Summary
 
- Hybrid recommendation engine combining semantic AI with live TMDB data
- Natural language movie search — describe a movie instead of knowing its title
- Explainable recommendations with match percentages and reasoning
- Real-time autocomplete with posters and release years
- Advanced Discover page with multiple filters
- Dynamic hero banner with live movie information
- One-click trailer playback in a new browser tab
- Persistent wishlist with live UI updates
- Similar movie recommendations from the details page
- Modern, Netflix-inspired responsive interface
- Fully Dockerized architecture for easy deployment
- Clear separation between frontend (React) and backend (FastAPI) for scalability and maintainability
---
