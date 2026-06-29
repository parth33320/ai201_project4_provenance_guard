import re

def calculate_template_conformity(alt_text):
    """
    Measures how formulaic/templated the Alt-text is.
    AI often starts with 'A photo of...', 'An image showing...', etc.
    Returns a score from 0.0 (Human) to 1.0 (AI).
    """
    ai_templates = [
        r"^a photo of",
        r"^an image of",
        r"^a picture of",
        r"^this image shows",
        r"^the image displays",
        r"^a high-quality photo of",
        r"^a close up of",
        r"^an illustration of"
    ]

    text_lower = alt_text.lower().strip()

    match_count = 0
    for template in ai_templates:
        if re.search(template, text_lower):
            match_count += 1

    # Simple binary/weighted match for template conformity
    if match_count > 0:
        return 0.8  # Strong AI signal

    return 0.2 # Lower likelihood if it doesn't follow a template

def calculate_descriptive_verbosity(alt_text):
    """
    Measures 'clinical detail' vs human subjectivity.
    AI-generated alt-text tends to be longer and more exhaustive.
    Returns a score from 0.0 (Human) to 1.0 (AI).
    """
    words = alt_text.split()
    word_count = len(words)

    # 1. Length analysis: Human alt-text is often brief (e.g., 5-15 words).
    # AI often goes for 20-50+ words of clinical description.
    if word_count > 30:
        length_score = 0.9
    elif word_count > 15:
        length_score = 0.6
    else:
        length_score = 0.3

    # 2. Adjective density: AI uses many adjectives for 'exhaustive' description.
    # Simple proxy: words ending in 'ly', 'ing', 'ed' or just word length.
    descriptive_words = [w for w in words if len(w) > 7]
    density = len(descriptive_words) / word_count if word_count > 0 else 0

    # Typical AI density for clinical description is higher
    density_score = min(density / 0.3, 1.0)

    return (length_score * 0.7) + (density_score * 0.3)
