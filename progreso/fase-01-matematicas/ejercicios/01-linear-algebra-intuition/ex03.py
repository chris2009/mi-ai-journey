import random

from vector import Vector

random.seed(42)

# 5 vectores aleatorios de dimensión 50 (simulando "embeddings")
words = [Vector([random.gauss(0, 1) for _ in range(50)]) for _ in range(5)]
labels = ["word_0", "word_1", "word_2", "word_3", "word_4"]

print(f"words: {words}\n")
print(f"labels: {labels}\n")
# TU CÓDIGO:
# Compara cada par (i, j) con i < j usando cosine_similarity
# Encuentra el par con la similitud más alta y muestra:
#   - todas las similitudes calculadas
#   - cuál par es el más similar y su score
max_similarity = -1
most_similar_pair = None
similarities = []
for i in range(len(words)):
    for j in range(i + 1, len(words)):
        sim = words[i].cosine_similarity(words[j])
        similarities.append((labels[i], labels[j], sim))
        if sim > max_similarity:
            max_similarity = sim
            most_similar_pair = (labels[i], labels[j])
print("Similitudes calculadas:")
for w1, w2, sim in similarities:
    print(f"  {w1} vs {w2}: {sim:.4f}")
print(f"\nPar más similar: {most_similar_pair[0]} y {most_similar_pair[1]} con similitud {max_similarity:.4f}") # type: ignore
