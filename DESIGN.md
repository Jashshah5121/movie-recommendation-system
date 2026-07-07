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

