"""
Worked on this for more than 12 hours, and it ended up incorrectly finding the simmilarites and returning wrong results.
Key things: I used torch and bert model for phrase extracting for google search.
remove_similar_phrases is the reason of failing 
"""

import re
import torch
from transformers import AutoModel, AutoTokenizer
import torch.nn.functional as F

# Load the BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def remove_stopwords(input_text, stopwords_file="resources/stopwords"):
    with open(stopwords_file, 'r') as f:
        stopwords = set(f.read().splitlines())
    
    words = input_text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    filtered_text = ' '.join(filtered_words)
    print("Filtered text:", filtered_text)
    return filtered_text

def split_text_into_phrases(text):
    phrases = re.split(r'[,.!?;:]+', text.strip())
    print("Split phrases:", phrases)
    return [phrase.strip() for phrase in phrases if phrase.strip()]

def get_embeddings(phrases):
    inputs = tokenizer(phrases, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    embeddings = outputs.last_hidden_state[:, 0, :]  # Get the [CLS] token representation
    return embeddings

def remove_similar_phrases(phrases, threshold=0.85):
    # Step 1: Get embeddings for all phrases
    embeddings = get_embeddings(phrases)
    unique_phrases = phrases.copy()  # Start with all phrases
    total_words = sum(len(phrase.split()) for phrase in unique_phrases)

    # Step 2: Calculate similarity scores
    similarity_matrix = []
    for i, emb1 in enumerate(embeddings):
        similarity_scores = []
        for j, emb2 in enumerate(embeddings):
            if i != j:
                similarity = F.cosine_similarity(emb1.unsqueeze(0), emb2.unsqueeze(0)).item()
                similarity_scores.append((similarity, j))  # Store (similarity, index)
        similarity_matrix.append(similarity_scores)

    # Step 3: Remove phrases until the word count is 32 or less
    while total_words > 32:
        # Find the phrase with the highest average similarity to others
        avg_similarity = []
        for i, scores in enumerate(similarity_matrix):
            # Only consider scores above the threshold
            valid_scores = [sim for sim, idx in scores if sim > threshold]
            if valid_scores:
                avg_sim = sum(valid_scores) / len(valid_scores)
                avg_similarity.append((avg_sim, i, len(unique_phrases[i])))  # (average similarity, index, word count)

        # Sort by average similarity (highest first) and then by word count (more words first)
        avg_similarity.sort(key=lambda x: (-x[0], -x[2]))  # Sort by avg similarity, then by word count

        # Remove the first entry (highest similarity)
        _, index_to_remove, _ = avg_similarity[0]
        total_words -= len(unique_phrases[index_to_remove].split())
        unique_phrases.pop(index_to_remove)
        
        # Remove the corresponding entry from the similarity matrix
        similarity_matrix.pop(index_to_remove)

        # Update remaining similarity scores
        for i in range(len(similarity_matrix)):
            similarity_matrix[i] = [(sim, idx - 1 if idx > index_to_remove else idx) for sim, idx in similarity_matrix[i] if idx != index_to_remove]

    return unique_phrases

def extract_unique_phrases(text, stopwords_file="resources/stopwords"):
    try:
        cleaned_text = remove_stopwords(text, stopwords_file)
        phrases = split_text_into_phrases(cleaned_text)
        unique_phrases = remove_similar_phrases(phrases)
        
        # Trim to 32 words if necessary
        total_word_count = sum(len(phrase.split()) for phrase in unique_phrases)
        if total_word_count > 32:
            # Remove excess phrases
            while total_word_count > 32:
                # Assuming we want to remove the longest phrase each time
                longest_phrase_index = max(range(len(unique_phrases)), key=lambda i: len(unique_phrases[i].split()))
                total_word_count -= len(unique_phrases[longest_phrase_index].split())
                unique_phrases.pop(longest_phrase_index)

        return unique_phrases
    except Exception as e:
        return [f"Error: {e}"]

# Example usage:
text = (
    "In the heart of an ancient forest, where the trees stretched high into the sky, "
    "a quiet stillness enveloped the land. The sunlight filtered through the leaves, casting dappled shadows on the ground, "
    "while the gentle rustle of the wind whispered secrets of the ages. "
    
    "Among the towering oaks and sturdy pines, a brook meandered, its waters sparkling like diamonds in the daylight. "
    "It sang a melodic tune as it flowed over smooth stones, nourishing the vibrant life surrounding it. "
    "Flowers of every hue bloomed along its banks, their fragrances mingling in the air, creating a symphony of scents that beckoned to the wandering creatures of the woods. "
    
    "As dusk approached, the forest transformed. The warm hues of sunset faded, replaced by the cool tones of twilight. "
    "Fireflies began to flicker, illuminating the darkness with their tiny, glowing lights. "
    "The chirping of crickets filled the air, and the soft hoots of owls echoed from the treetops. "
    
    "In this enchanting place, a young girl named Elara wandered, her curiosity leading her deeper into the woods. "
    "She was drawn to the beauty around her, her heart racing with excitement. Legends spoke of a hidden glade where the moonlight danced upon a silver pond, and she longed to find it. "
    
    "With each step, she discovered new wonders—a cluster of mushrooms forming a perfect circle, a family of deer grazing peacefully in a clearing, "
    "and the distant call of a wolf breaking the silence. The forest felt alive, as if it were watching her every move, guiding her toward her destiny. "
    
    "Finally, as the last rays of sunlight disappeared, Elara stumbled upon the glade. The moon hung high, casting a silvery glow on the pond, "
    "which mirrored the starry sky above. She stood in awe, realizing she had found a sacred place untouched by time, a refuge where magic and reality intertwined."
)
"""The provided text is best classified as a **narrative essay**. It tells a story with descriptive imagery and follows a character, Elara, as she explores an ancient forest, highlighting her experiences and emotions throughout her journey."""

unique_phrases = extract_unique_phrases(text)
print("Final unique phrases (32 words or less):", unique_phrases)
