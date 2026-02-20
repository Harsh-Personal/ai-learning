# embeddings_experiment.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model... (takes 30 seconds first time)")
model = SentenceTransformer("all-MiniLM-L6-v2")

# EXPERIMENT 1: Basic similarity
print("\n" + "=" * 60)
print("EXPERIMENT 1: Do similar sentences have similar embeddings?")
print("=" * 60)


def print_pairwise_similarities(items, similarities, title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            score = similarities[i][j]
            print(f"{score:.3f} | '{items[i]}' ↔ '{items[j]}'")


def experiment_basic_similarity(model):
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Do similar sentences have similar embeddings?")
    print("=" * 60)

    sentences = [
        "I love pizza",
        "Pizza is my favorite food",
        "I hate vegetables",
        "The weather is nice today",
    ]

    embeddings = model.encode(sentences)
    similarities = cosine_similarity(embeddings)
    print_pairwise_similarities(sentences, similarities, "Basic Similarity")


def experiment_synonyms(model):
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Are synonyms more similar?")
    print("=" * 60)

    words = ["happy", "joyful", "sad"]
    word_embeddings = model.encode(words)
    word_sims = cosine_similarity(word_embeddings)
    print_pairwise_similarities(words, word_sims, "Synonyms")


def experiment_domain_specific(model):
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Domain relevance")
    print("=" * 60)

    topics = [
        "diabetes treatment",
        "insulin injection",
        "machine learning algorithms",
        "neural networks",
    ]

    topic_embeddings = model.encode(topics)
    topic_sims = cosine_similarity(topic_embeddings)
    print_pairwise_similarities(topics, topic_sims, "Domain-specific")


def experiment_sdet_domain(model):
    print("\n" + "=" * 60)
    print("YOUR TURN: Test something from your work domain")
    print("=" * 60)

    topics = ["python", "pytest", "Javascript", "Playwright"]
    topic_embeddings = model.encode(topics)
    topic_sims = cosine_similarity(topic_embeddings)
    print_pairwise_similarities(topics, topic_sims, "SDET domain")


if __name__ == "__main__":
    print("Loading model... (takes 30 seconds first time)")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    experiment_basic_similarity(model)
    experiment_synonyms(model)
    experiment_domain_specific(model)
    experiment_sdet_domain(model)
