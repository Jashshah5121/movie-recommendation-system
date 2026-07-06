from pipeline.ai_pipeline import AIPipeline

queries = [

    "Interstellar",

    "movies like Interstellar",

    "Tom Cruise movies",

    "Christopher Nolan movies",

    "Science Fiction",

    "2014",

    "movie where toys come alive",

    "space movie with black hole"

]

for query in queries:

    print("=" * 80)

    print(query)

    result = AIPipeline.search(query)

    print(result)