import re
import math
from collections import Counter

def calculate_stylometrics(text):
    """
    Calculates stylometric features of the text.
    Returns a score between 0.0 (uniform/AI) and 1.0 (variable/Human).
    """
    # 1. Prepare text
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    words = re.findall(r'\w+', text.lower())

    if not sentences or not words:
        return 0.5

    # 2. Sentence Length Variance
    sentence_lengths = [len(s.split()) for s in sentences]
    avg_len = sum(sentence_lengths) / len(sentence_lengths)
    if len(sentence_lengths) > 1:
        variance = sum((x - avg_len) ** 2 for x in sentence_lengths) / len(sentence_lengths)
        # Normalize variance (Human writing has high variance)
        # 0 to 100+ variance maps to 0 to 1 score
        var_score = min(variance / 50.0, 1.0)
    else:
        var_score = 0.5

    # 3. Type-Token Ratio (TTR) - Vocabulary Diversity
    unique_words = set(words)
    ttr = len(unique_words) / len(words)
    # TTR typically ranges from 0.4 to 0.8. Normalize to 0-1.
    ttr_score = min(max((ttr - 0.3) / 0.4, 0.0), 1.0)

    # 4. Punctuation Density
    punctuation = re.findall(r'[.,!?;:]', text)
    punc_density = len(punctuation) / len(words)
    # Human writing often has higher punctuation density (commas, semi-colons).
    # Typical density 0.05 to 0.15
    punc_score = min(max((punc_density - 0.05) / 0.1, 0.0), 1.0)

    # 5. Sentence Complexity (Average syllables/word proxy or word length)
    avg_word_len = sum(len(w) for w in words) / len(words)
    # AI tends to use medium-complex words consistently.
    # Human complexity varies. For this proxy, we'll use avg_word_len.
    # 4.5 to 6.5 range
    comp_score = min(max((avg_word_len - 4.0) / 2.5, 0.0), 1.0)

    # Weighted combination of stylometric scores
    # Human writing = High score
    stylo_human_score = (var_score * 0.4) + (ttr_score * 0.3) + (punc_score * 0.1) + (comp_score * 0.2)

    return stylo_human_score

def calculate_burstiness(text):
    """
    Stretch Feature: Ensemble Detection (Signal 3)
    Measures 'Burstiness' - variation in sentence structure (length of clauses)
    and paragraph-level variation.
    High variation = Human.
    """
    # 1. Clause-level variation
    clauses = re.split(r'[,;:]', text)
    clause_lengths = [len(c.split()) for c in clauses if len(c.split()) > 0]

    if len(clause_lengths) < 2:
        var_clause_score = 0.5
    else:
        avg_clause = sum(clause_lengths) / len(clause_lengths)
        var_clause = sum((x - avg_clause) ** 2 for x in clause_lengths) / len(clause_lengths)
        var_clause_score = min(var_clause / 30.0, 1.0)

    # 2. Paragraph-level variation
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    paragraph_lengths = [len(p.split()) for p in paragraphs]

    if len(paragraph_lengths) < 2:
        var_para_score = 0.5
    else:
        avg_para = sum(paragraph_lengths) / len(paragraph_lengths)
        var_para = sum((x - avg_para) ** 2 for x in paragraph_lengths) / len(paragraph_lengths)
        # Normalize variance for paragraphs (higher range usually)
        var_para_score = min(var_para / 100.0, 1.0)

    # Ensemble of structural variation
    return (var_clause_score * 0.5) + (var_para_score * 0.5)

def calculate_weighted_veto_score(llm_ai_score, stylo_human_score, burst_score=0.5, content_type='text', multimodal_scores=None):
    """
    Implements the "Human Defense Veto" logic.
    - Routes scoring based on content_type.
    - If either Stylometric or Burstiness Human score is very high, it vetos high AI scores.
    - Final score is 0.0 (Human) to 1.0 (AI).
    """
    if content_type == 'image_description' and multimodal_scores:
        template_score = multimodal_scores.get('template_score', 0.5)
        verbosity_score = multimodal_scores.get('verbosity_score', 0.5)

        # For Alt-text, we use different weights and signals.
        # Template conformity is a strong AI marker.
        # Descriptive verbosity is a secondary marker.
        # LLM semantic analysis still has the highest weight.

        combined_ai_score = (llm_ai_score * 0.5) + (template_score * 0.3) + (verbosity_score * 0.2)

        # We still respect the LLM if it's very certain about human
        if llm_ai_score < 0.2:
            return min(combined_ai_score, 0.3)

        return combined_ai_score

    # Default Text Logic
    # 1. The Veto: If human signals are extremely strong, push score towards 0 (Human tier)
    # Using relative reduction capped at 0.3
    if stylo_human_score > 0.85 or burst_score > 0.85:
        strongest_human_signal = max(stylo_human_score, burst_score)
        return min(llm_ai_score * (1.0 - strongest_human_signal), 0.3)

    # 2. Conflicting Signals: If LLM says AI but human markers are present
    if llm_ai_score > 0.7 and (stylo_human_score > 0.6 or burst_score > 0.6):
        # Move towards uncertain
        return 0.5

    # 3. Standard weighting
    # We invert human-leaning scores to get AI-leaning components
    stylo_ai_score = 1.0 - stylo_human_score
    burst_ai_score = 1.0 - burst_score

    # Weight LLM more heavily for semantic markers, but give Stylo and Burstiness a say
    combined_ai_score = (llm_ai_score * 0.6) + (stylo_ai_score * 0.2) + (burst_ai_score * 0.2)

    return combined_ai_score
