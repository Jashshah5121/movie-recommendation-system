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

## 4. Data Source 
# Data Collection and Preprocessing

The performance of any recommendation system depends on the quality of its data. Therefore, before developing the recommendation engine, a comprehensive movie dataset was collected and preprocessed.

MovieHub AI uses **two different sources of data**:

1. Local Movie Dataset (for AI recommendations)
2. Live TMDB APIs (for real-time movie information)

---

# Data Crawling and Collection

Instead of manually entering movie information, the project uses data collected from **The Movie Database (TMDB)**.

TMDB provides a rich collection of movie metadata through both downloadable datasets and REST APIs.

During development, movie information was collected from TMDB, including:

- Titles
- Genres
- Movie descriptions
- Cast
- Crew
- Posters
- Ratings
- Languages
- Release dates

The downloaded datasets were cleaned and converted into a structured format suitable for building the recommendation engine.

For movie information that changes frequently, such as trending movies, trailers, ratings, and recommendations, the application fetches the latest data directly from the TMDB API whenever a user interacts with the system.

This hybrid approach ensures that the recommendation engine has a stable local dataset while still displaying the latest movie information.

---

# Data Preprocessing

The raw datasets contained multiple columns that were not directly useful for recommendation.

Therefore, several preprocessing steps were performed.

These include:

- Removing duplicate movies
- Handling missing values
- Cleaning text
- Extracting important features
- Standardizing metadata
- Combining multiple columns

The following movie attributes were merged into a single textual representation:

- Overview
- Genres
- Keywords
- Cast
- Director

This combined metadata better represents the content of each movie and improves semantic similarity calculations.


## Dataset Files

The project initially used multiple CSV files containing movie information.
but after calculating vectors and similarity we only need to store .pkl files, metdata.csv and movies.db


# SQLite Database

After preprocessing, the cleaned movie dataset was stored inside a local SQLite database.

The database is primarily used by the Discover module.

SQLite stores information such as:

- Movie ID
- Title
- Genres
- Language
- Ratings
- Release Date

Using SQLite instead of repeatedly calling TMDB APIs provides:

- Faster filtering
- Offline support
- Lower API usage
- Better performance

---

