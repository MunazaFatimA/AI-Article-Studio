import hashlib
import re
import math
from collections import Counter

def check_plagiarism(text):
    """
    Advanced Plagiarism Detection
    Returns: 0% = 100% Unique, 100% = Fully Copied
    """
    if not text:
        return 0
    
    score = 0
    text_lower = text.lower()
    words = text.split()
    
    if len(words) < 50:
        return 0
    
    # ============================================================
    # 1. CHECK FOR AI-GENERATED PATTERNS
    # ============================================================
    
    ai_patterns = [
        # AI Clichés
        ("in conclusion", 5),
        ("furthermore", 4),
        ("moreover", 4),
        ("additionally", 3),
        ("it is important to note", 5),
        ("it should be noted", 5),
        ("on the other hand", 4),
        ("as a result", 3),
        ("consequently", 3),
        ("firstly", 2),
        ("secondly", 2),
        ("thirdly", 2),
        ("in this article", 3),
        ("we will explore", 3),
        ("we will discuss", 3),
        ("this paper", 2),
        ("delve into", 4),
        ("tapestry", 5),
        ("testament", 5),
        ("beacon", 5),
        ("paramount", 5),
        ("seamless", 4),
        ("elevated", 4),
        ("vital role", 5),
        ("crucial", 4),
        ("landscape", 3),
        ("harness", 4),
        ("game-changer", 5),
        ("unlock", 3),
        ("dive deep", 4),
        ("demystify", 4),
        ("holistic", 4),
        ("realm", 3),
        ("nestled", 4),
        ("vibrant", 3),
    ]
    
    ai_score = 0
    for pattern, weight in ai_patterns:
        if pattern in text_lower:
            ai_score += weight
    
    # Normalize AI score (max 50%)
    ai_score = min(ai_score, 50)
    score += ai_score
    
    # ============================================================
    # 2. CHECK FOR COPYRIGHTED/PLAGIARIZED PATTERNS
    # ============================================================
    
    plagiarized_patterns = [
        "lorem ipsum",
        "sample text",
        "the quick brown",
        "this is a test",
        "generated content",
        "dolor sit amet",
        "consectetur adipiscing",
        "sed do eiusmod",
        "tempor incididunt",
        "ut labore et dolore",
        "placeholder text",
        "dummy text",
        "example text",
    ]
    
    plag_score = 0
    for pattern in plagiarized_patterns:
        if pattern in text_lower:
            plag_score += 15
    
    # Normalize plag score (max 30%)
    plag_score = min(plag_score, 30)
    score += plag_score
    
    # ============================================================
    # 3. CHECK DUPLICATE SENTENCES (Self-Plagiarism) - IMPROVED
    # ============================================================
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 15]
    
    if sentences and len(sentences) > 3:
        unique_sentences = set(sentences)
        duplicate_ratio = 1 - (len(unique_sentences) / len(sentences))
        
        if duplicate_ratio > 0.10:
            dup_score = 10 + (duplicate_ratio * 25)
            score += min(dup_score, 25)
        
        # Additional: Check for very similar sentences (fuzzy duplicate)
        if len(sentences) > 5:
            similar_count = 0
            for i in range(len(sentences)):
                for j in range(i+1, len(sentences)):
                    if len(sentences[i]) > 10 and len(sentences[j]) > 10:
                        # Check if one sentence is subset of another
                        if sentences[i] in sentences[j] or sentences[j] in sentences[i]:
                            similar_count += 1
            if similar_count > 3:
                score += 10
    
    # ============================================================
    # 4. CHECK REPETITIVE N-GRAMS
    # ============================================================
    
    if len(words) > 100:
        ngram_count = Counter()
        for i in range(len(words) - 3):
            ngram = " ".join(words[i:i+3]).lower()
            ngram_count[ngram] += 1
        
        repeated_ngrams = sum(1 for v in ngram_count.values() if v > 2)
        total_ngrams = len(ngram_count)
        
        if total_ngrams > 0:
            ngram_ratio = repeated_ngrams / total_ngrams
            if ngram_ratio > 0.05:
                score += min(ngram_ratio * 50, 15)
    
    # ============================================================
    # 5. CHECK SPIN SYNTAX (Spin content indicator)
    # ============================================================
    
    spin_patterns = [
        r'\{[^}]+\}',   # {word1|word2}
        r'\[[^\]]+\]',   # [word1|word2]
        r'<[^>]+>',      # <word>
        r'\|',           # Pipe symbol
        r'\(.*?\|.*?\)'  # (word1|word2)
    ]
    
    for pattern in spin_patterns:
        if re.search(pattern, text):
            score += 20
            break
    
    # ============================================================
    # 6. CHECK FAKE CITATIONS
    # ============================================================
    
    citation_patterns = [
        r'\(Source:.*?\)',
        r'\[Source:.*?\]',
        r'According to \[.*?\]',
        r'According to .*? \(.*?\)',
        r'\(.*? \d{4}\)',
        r'\[.*? \d{4}\]'
    ]
    
    for pattern in citation_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            score += 5
    
    # ============================================================
    # 7. CHECK FOR PERFECT GRAMMAR (AI Signature)
    # ============================================================
    
    # Count punctuation variety (AI uses limited punctuation)
    punctuation_counts = {
        '.': text.count('.'),
        ',': text.count(','),
        ';': text.count(';'),
        ':': text.count(':'),
        '?': text.count('?'),
        '!': text.count('!'),
        '—': text.count('—'),
        '(': text.count('('),
        ')': text.count(')'),
    }
    
    total_punct = sum(punctuation_counts.values())
    if total_punct > 10:
        unique_punct = sum(1 for v in punctuation_counts.values() if v > 0)
        if unique_punct < 4:
            score += 10
    
    # ============================================================
    # 8. CHECK SENTENCE LENGTH VARIATION
    # ============================================================
    
    sent_lengths = [len(s.split()) for s in sentences if len(s.split()) > 5]
    if len(sent_lengths) > 5:
        avg_len = sum(sent_lengths) / len(sent_lengths)
        max_len = max(sent_lengths)
        min_len = min(sent_lengths)
        variation = max_len - min_len
        
        # Low variation = AI
        if variation < 10:
            score += 5
    
    # ============================================================
    # 9. CHECK REPETITIVE PHRASES
    # ============================================================
    
    common_phrases = [
        "AI-powered", "machine learning", "artificial intelligence",
        "data-driven", "cutting-edge", "state-of-the-art",
        "game-changing", "transformative", "in the realm of",
        "world of", "rich cultural heritage", "natural beauty",
        "warm hospitality", "diverse culture", "breathtaking",
        "pristine", "vibrant", "nestled", "landscape",
        "treasure trove", "must-visit", "top tourist",
        "unforgettable", "once in a lifetime",
         "you won't regret", "a must-see", "well worth",
        "a trip to remember", "once you visit"
    ]
    
    phrase_count = sum(1 for p in common_phrases if p in text_lower)
    if phrase_count > 8:
        score += 15
    elif phrase_count > 5:
        score += 10
    elif phrase_count > 3:
        score += 5
    
    # ============================================================
    # FINAL: CLAMP SCORE BETWEEN 0-100
    # ============================================================
    
    final_score = min(100, max(0, score))
    return final_score


def get_plagiarism_report(text):
    """
    Detailed plagiarism report with percentages
    """
    if not text:
        return {
            'total': 0,
            'ai_patterns': 0,
            'plagiarized_patterns': 0,
            'duplicate_sentences': 0,
            'repetitive_ngrams': 0,
            'spin_syntax': 0,
            'fake_citations': 0,
            'perfect_grammar': 0,
            'low_variation': 0,
            'repetitive_phrases': 0
        }
    
    words = text.split()
    if len(words) < 50:
        return {
            'total': 0,
            'ai_patterns': 0,
            'plagiarized_patterns': 0,
            'duplicate_sentences': 0,
            'repetitive_ngrams': 0,
            'spin_syntax': 0,
            'fake_citations': 0,
            'perfect_grammar': 0,
            'low_variation': 0,
            'repetitive_phrases': 0
        }
    
    text_lower = text.lower()
    
    # AI patterns count
    ai_patterns_list = [
        "in conclusion", "furthermore", "moreover", "additionally",
        "it is important to note", "on the other hand", "as a result",
        "consequently", "delve into", "tapestry", "testament", "beacon",
        "paramount", "seamless", "elevated", "vital role", "crucial",
        "landscape", "harness", "game-changer", "unlock", "dive deep",
        "demystify", "holistic", "realm"
    ]
    ai_count = sum(1 for p in ai_patterns_list if p in text_lower)
    ai_percent = min(ai_count * 2, 50)
    
    # Plagiarized patterns
    plag_list = [
        "lorem ipsum", "sample text", "the quick brown",
        "this is a test", "generated content", "dolor sit amet",
        "consectetur adipiscing", "sed do eiusmod", "tempor incididunt"
    ]
    plag_count = sum(1 for p in plag_list if p in text_lower)
    plag_percent = min(plag_count * 15, 30)
    
    # Duplicate sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 20]
    dup_percent = 0
    if sentences and len(sentences) > 1:
        unique_sentences = set(sentences)
        dup_ratio = 1 - (len(unique_sentences) / len(sentences))
        dup_percent = min(10 + (dup_ratio * 20), 20)
    
    # Spin syntax
    spin_patterns = [r'\{[^}]+\}', r'\[[^\]]+\]', r'<[^>]+>', r'\|']
    spin_count = sum(1 for p in spin_patterns if re.search(p, text))
    spin_percent = min(spin_count * 20, 20)
    
    # Fake citations
    citation_patterns = [r'\(Source:.*?\)', r'\[Source:.*?\]', r'According to \[.*?\]']
    citation_count = sum(1 for p in citation_patterns if re.search(p, text, re.IGNORECASE))
    citation_percent = min(citation_count * 5, 10)
    
    # Perfect grammar
    punct_counts = {
        '.': text.count('.'), ',': text.count(','),
        ';': text.count(';'), ':': text.count(':'),
        '?': text.count('?'), '!': text.count('!')
    }
    total_punct = sum(punct_counts.values())
    punct_percent = 0
    if total_punct > 10:
        unique_punct = sum(1 for v in punct_counts.values() if v > 0)
        if unique_punct < 4:
            punct_percent = 10
    
    # Low variation
    sent_lengths = [len(s.split()) for s in sentences if len(s.split()) > 5]
    var_percent = 0
    if len(sent_lengths) > 5:
        variation = max(sent_lengths) - min(sent_lengths)
        if variation < 10:
            var_percent = 5
    
    # Repetitive phrases
    common_phrases = [
        "AI-powered", "machine learning", "artificial intelligence",
        "data-driven", "cutting-edge", "state-of-the-art"
    ]
    phrase_count = sum(1 for p in common_phrases if p in text_lower)
    phrase_percent = min(phrase_count * 2, 10)
    
    total = min(100, ai_percent + plag_percent + dup_percent + spin_percent + 
                citation_percent + punct_percent + var_percent + phrase_percent)
    
    return {
        'total': total,
        'ai_patterns': ai_percent,
        'plagiarized_patterns': plag_percent,
        'duplicate_sentences': dup_percent,
        'repetitive_ngrams': 0,
        'spin_syntax': spin_percent,
        'fake_citations': citation_percent,
        'perfect_grammar': punct_percent,
        'low_variation': var_percent,
        'repetitive_phrases': phrase_percent
    }