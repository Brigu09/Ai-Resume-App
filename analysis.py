import fitz
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


## Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Minej/bert-base-personality")
model = AutoModelForSequenceClassification.from_pretrained("Minej/bert-base-personality")

## Define Big Five Personality Traits
TRAITS = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]


def extract_text_from_pdf(pdf_path):

    """Read and Extract text from the pdf file."""

    doc = fitz.open(pdf_path)
    text = " "
    for page in doc:
        text += page.get_text()
    return text

def personality_prediction_traits(text):

    """Analyze Personality using Transformer based Hugging Face Model"""
    
    token = tokenizer(text, return_tensors = "pt", truncation = True, padding = True, max_length = 512)
    outputs = model(**token)   ## getting raw score (logists)
    scores = torch.nn.functional.softmax(outputs.logits, dim = 1).detach().numpy()[0]  
    return TRAITS, scores

def plot_personality_traits_scores(scores):
    """Plot a bar chart for personality scores with an enhanced design."""
    
    labels = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    
    # Convert scores to percentages
    scores_percent = [s * 100 for s in scores]

    sns.set_theme(style="whitegrid")

    # ✅ Create a figure explicitly
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = sns.color_palette("coolwarm", len(scores))
    
    # ✅ Plot with explicit figure and axes
    bars = sns.barplot(x=labels, y=scores_percent, palette=colors, ax=ax)

    # ✅ Add value labels on top of bars
    for bar, score in zip(bars.patches, scores_percent):
        ax.text(bar.get_x() + bar.get_width() / 2, 
                bar.get_height() + 1,  # Slightly above the bar
                f"{score:.1f}%", 
                ha='center', fontsize=12, fontweight='bold', color='black')

    # ✅ Labels and title
    ax.set_xlabel("Personality Traits", fontsize=14, fontweight='bold')
    ax.set_ylabel("Score (%)", fontsize=14, fontweight='bold')
    ax.set_title("Big Five Personality Traits Analysis", fontsize=16, fontweight='bold')

    # ✅ Set y-axis limit to 100% (normalized scale)
    ax.set_ylim(0, 100)  

    # ✅ Grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig  # ✅ Return the figure instead of plt.show()