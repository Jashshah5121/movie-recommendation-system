import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "dataset" / "movies.db"

OUTPUT_PATH = Path(__file__).parent / "combined_features.csv"


def repeat(text, n):

    if not text:
        return ""

    return (" " + text) * n


def clean(text):

    if text is None:
        return ""

    text = str(text).lower()

    text = text.replace("|", " ")

    text = " ".join(text.split())

    return text


# ---------------------------------------------------------
# TF-IDF FEATURES
# ---------------------------------------------------------

def build_tfidf_features(row):

    text = ""

    text += repeat(clean(row["title"]), 2)

    text += repeat(clean(row["director"]), 4)

    text += repeat(clean(row["genres"]), 3)

    text += repeat(clean(row["keywords"]), 3)

    text += repeat(clean(row["movie_cast"]), 2)

    text += repeat(clean(row["tagline"]), 2)

    text += repeat(clean(row["collection"]), 2)

    text += repeat(clean(row["production_companies"]), 1)

    text += repeat(clean(row["overview"]), 1)

    return text.strip()


# ---------------------------------------------------------
# SEMANTIC FEATURES
# ---------------------------------------------------------

def build_semantic_features(row):

    text = ""

    text += repeat(clean(row["title"]), 2)

    text += repeat(clean(row["overview"]), 2)

    text += repeat(clean(row["genres"]), 2)

    text += repeat(clean(row["keywords"]), 2)

    text += repeat(clean(row["tagline"]), 1)

    return text.strip()


def main():

    print("=" * 60)
    print("Loading database...")

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(

        "SELECT * FROM movies WHERE scraped = 1",

        conn

    )

    conn.close()

    print(f"Movies Loaded : {len(df)}")

    print()
    print("Building Features...")

    df["tfidf_features"] = df.apply(

        build_tfidf_features,

        axis=1

    )

    df["semantic_features"] = df.apply(

        build_semantic_features,

        axis=1

    )

    df["year"] = pd.to_datetime(

        df["release_date"],

        errors="coerce"

    ).dt.year

    df["genres_list"] = df["genres"]

    df["keywords_list"] = df["keywords"]

    df["cast_list"] = df["movie_cast"]

    print()
    print("Saving CSV...")

    df.to_csv(

        OUTPUT_PATH,

        index=False

    )

    print()
    print("=" * 60)
    print("Feature Engineering Complete!")
    print("=" * 60)
    print(f"Movies : {len(df)}")
    print(f"Saved : {OUTPUT_PATH}")


if __name__ == "__main__":

    main()