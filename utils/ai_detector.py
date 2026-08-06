# utils/ai_detector.py

import re
import math
import random
from collections import Counter
from statistics import stdev, mean

# ============================================================
# PART OF SPEECH TAGS (Simple POS Tagger)
# ============================================================

def simple_pos_tagger(text):
    """Simple POS tagger using common suffixes"""
    words = text.split()
    tags = []
    
    for word in words:
        word_lower = word.lower()
        
        # Common suffixes
        if word_lower.endswith('ing'):
            tags.append('VERB')
        elif word_lower.endswith('ed'):
            tags.append('VERB')
        elif word_lower.endswith('ion'):
            tags.append('NOUN')
        elif word_lower.endswith('tion'):
            tags.append('NOUN')
        elif word_lower.endswith('ment'):
            tags.append('NOUN')
        elif word_lower.endswith('ness'):
            tags.append('NOUN')
        elif word_lower.endswith('ity'):
            tags.append('NOUN')
        elif word_lower.endswith('ly'):
            tags.append('ADV')
        elif word_lower.endswith('ful'):
            tags.append('ADJ')
        elif word_lower.endswith('ous'):
            tags.append('ADJ')
        elif word_lower.endswith('ive'):
            tags.append('ADJ')
        elif word_lower.endswith('able'):
            tags.append('ADJ')
        else:
            # Common words
            if word_lower in ['the', 'a', 'an', 'of', 'to', 'for', 'with', 'on', 'at', 'from', 'by']:
                tags.append('DET')
            elif word_lower in ['i', 'you', 'we', 'they', 'he', 'she', 'it', 'my', 'your', 'our']:
                tags.append('PRON')
            elif word_lower in ['is', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'did']:
                tags.append('AUX')
            else:
                tags.append('NOUN')
    
    return tags


# ============================================================
# MAIN DETECTION FUNCTION
# ============================================================

def detect_ai(text):
    """
    ADVANCED AI DETECTOR - Uses 7+ techniques for accurate detection
    """
    if not text or not text.strip():
        return 0
    
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)
    
    if word_count < 30:
        return 0
    
    score = 0
    details = {}
    
    # ============================================================
    # 1. SYNTACTIC DIVERSITY (0-15)
    # ============================================================
    
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip().split()) > 2]
    
    if len(sentences) >= 5:
        # 1a. Sentence structure patterns
        sentence_structures = []
        for s in sentences:
            words_in_s = s.split()
            if len(words_in_s) >= 3:
                # Pattern: Subject-Verb-Object (simplified)
                has_svo = False
                for i in range(len(words_in_s) - 1):
                    if words_in_s[i][0].isupper() and words_in_s[i+1] in ['is', 'are', 'was', 'were', 'has', 'have']:
                        has_svo = True
                        break
                sentence_structures.append('SVO' if has_svo else 'OTHER')
        
        if sentence_structures:
            unique_structures = len(set(sentence_structures))
            structure_ratio = unique_structures / len(sentence_structures)
            
            # AI has low syntactic diversity
            if structure_ratio < 0.3:
                score += 12
                details['syntactic'] = 'low'
            elif structure_ratio < 0.5:
                score += 8
                details['syntactic'] = 'medium'
            else:
                score += 3
                details['syntactic'] = 'high'
    
    # ============================================================
    # 2. VOCABULARY RICHNESS - TYPE-TOKEN RATIO (0-15)
    # ============================================================
    
    if word_count > 50:
        # 2a. Type-Token Ratio
        unique_words = set(w.lower() for w in words if len(w) > 2)
        ttr = len(unique_words) / word_count
        
        # Human: 0.5-0.7, AI: 0.3-0.5
        if ttr < 0.35:
            score += 12
            details['ttr'] = 'low (AI)'
        elif ttr < 0.45:
            score += 9
            details['ttr'] = 'medium-low'
        elif ttr < 0.55:
            score += 5
            details['ttr'] = 'medium'
        else:
            score += 2
            details['ttr'] = 'high (Human)'
        
        # 2b. Hapax Legomena (words that appear only once)
        word_freq = Counter(w.lower() for w in words)
        hapax = sum(1 for count in word_freq.values() if count == 1)
        hapax_ratio = hapax / len(words)
        
        # AI has fewer rare words
        if hapax_ratio < 0.3:
            score += 3
            details['hapax'] = 'low'
        else:
            details['hapax'] = 'high'
    
    # ============================================================
    # 3. REPETITION PATTERNS (0-15)
    # ============================================================
    
    if word_count > 50:
        # 3a. Word repetition
        word_freq = Counter(w.lower() for w in words if len(w) > 2)
        repeated_words = sum(1 for count in word_freq.values() if count > 3)
        repeat_ratio = repeated_words / len(word_freq) if word_freq else 0
        
        # AI repeats words more
        if repeat_ratio > 0.3:
            score += 10
            details['repetition'] = 'high (AI)'
        elif repeat_ratio > 0.2:
            score += 6
            details['repetition'] = 'medium'
        else:
            score += 2
            details['repetition'] = 'low (Human)'
        
        # 3b. Phrase repetition (3-gram)
        trigrams = []
        for i in range(len(words) - 2):
            trigram = ' '.join(words[i:i+3]).lower()
            trigrams.append(trigram)
        
        if trigrams:
            unique_trigrams = len(set(trigrams))
            trigram_ratio = unique_trigrams / len(trigrams)
            
            # AI repeats phrases
            if trigram_ratio < 0.4:
                score += 5
                details['phrase'] = 'repetitive'
            else:
                details['phrase'] = 'diverse'
    
    # ============================================================
    # 4. SEMANTIC COHERENCE ACROSS PARAGRAPHS (0-10)
    # ============================================================
    
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    
    if len(paragraphs) >= 2:
        # Measure transition words between paragraphs
        transition_words = [
            'however', 'furthermore', 'moreover', 'additionally', 
            'consequently', 'therefore', 'thus', 'hence', 
            'meanwhile', 'subsequently', 'ultimately', 'finally',
            'in addition', 'on the other hand', 'in conclusion',
            'first', 'second', 'third', 'next', 'then'
        ]
        
        transition_count = 0
        for para in paragraphs:
            if any(tw in para.lower() for tw in transition_words):
                transition_count += 1
        
        transition_ratio = transition_count / len(paragraphs)
        
        # AI uses too many predictable transitions
        if transition_ratio > 0.6:
            score += 8
            details['coherence'] = 'overly structured (AI)'
        elif transition_ratio > 0.4:
            score += 5
            details['coherence'] = 'moderate'
        else:
            score += 2
            details['coherence'] = 'natural (Human)'
    
    # ============================================================
    # 5. STYLOMETRIC FEATURES (0-20)
    # ============================================================
    
    # 5a. Punctuation usage
    punctuation = {
        '!': text.count('!'),
        '?': text.count('?'),
        ';': text.count(';'),
        ':': text.count(':'),
        '...': text.count('...'),
        '--': text.count('--'),
    }
    
    punc_ratio = sum(punctuation.values()) / word_count * 100
    
    # AI uses less varied punctuation
    if punc_ratio < 2.0:
        score += 8
        details['punctuation'] = 'low (AI)'
    elif punc_ratio < 4.0:
        score += 4
        details['punctuation'] = 'medium'
    else:
        details['punctuation'] = 'high (Human)'
    
    # 5b. Function Word Usage
    function_words = ['the', 'of', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 
                     'in', 'into', 'through', 'during', 'including', 'without',
                     'i', 'you', 'we', 'they', 'he', 'she', 'it', 'my', 'your',
                     'our', 'their', 'him', 'her', 'us', 'them']
    
    func_count = sum(1 for w in words if w.lower() in function_words)
    func_ratio = func_count / word_count * 100
    
    # Human: 40-50%, AI: 30-40%
    if func_ratio < 35:
        score += 8
        details['function_words'] = 'low (AI)'
    elif func_ratio < 48:
        score += 5
        details['function_words'] = 'medium-low'
    elif func_ratio < 45:
        score += 3
        details['function_words'] = 'medium'
    else:
        details['function_words'] = 'high (Human)'
    
    # 5c. POS Tag Distribution
    pos_tags = simple_pos_tagger(text)
    if pos_tags:
        pos_counts = Counter(pos_tags)
        total_pos = len(pos_tags)
        
        noun_ratio = pos_counts.get('NOUN', 0) / total_pos
        verb_ratio = pos_counts.get('VERB', 0) / total_pos
        pron_ratio = pos_counts.get('PRON', 0) / total_pos
        det_ratio = pos_counts.get('DET', 0) / total_pos
        
        # AI uses more nouns, fewer pronouns
        if noun_ratio > 0.4 and pron_ratio < 0.05:
            score += 4
            details['pos'] = 'noun-heavy (AI)'
        elif pron_ratio > 0.1:
            details['pos'] = 'balanced (Human)'
        else:
            details['pos'] = 'neutral'
    
    # ============================================================
    # 6. PERPLEXITY (0-10)
    # ============================================================
    
    # Calculate perplexity using n-gram probability
    def get_perplexity(text):
        words = text.lower().split()
        if len(words) < 3:
            return 0
        
        # Simple n-gram probability
        bigrams = []
        for i in range(len(words) - 1):
            bigrams.append((words[i], words[i+1]))
        
        if not bigrams:
            return 0
        
        unique_bigrams = set(bigrams)
        bigram_freq = Counter(bigrams)
        
        # Calculate probability (simplified)
        total_bigrams = len(bigrams)
        prob_sum = 0
        for gram, count in bigram_freq.items():
            prob = count / total_bigrams
            if prob > 0:
                prob_sum += math.log2(prob)
        
        if total_bigrams > 0:
            perplexity = 2 ** (-prob_sum / total_bigrams)
            return perplexity
        return 0
    
    perplexity = get_perplexity(text)
    
    # Lower perplexity = more predictable = AI
    if perplexity < 10:
        score += 8
        details['perplexity'] = 'low (AI)'
    elif perplexity < 15:
        score += 5
        details['perplexity'] = 'medium'
    else:
        details['perplexity'] = 'high (Human)'
    
    # ============================================================
    # 7. BURSTINESS (0-10)
    # ============================================================
    
    if len(sentences) >= 5:
        lengths = [len(s.split()) for s in sentences]
        
        if len(lengths) > 1:
            avg_len = mean(lengths)
            std_dev = stdev(lengths) if len(lengths) > 1 else 0
            
            # Burstiness = standard deviation / mean
            if avg_len > 0:
                burstiness = std_dev / avg_len
            else:
                burstiness = 0
            
            # Human: high burstiness (0.5-0.8), AI: low burstiness (0.1-0.3)
            if burstiness < 0.2:
                score += 8
                details['burstiness'] = 'low (AI)'
            elif burstiness < 0.3:
                score += 5
                details['burstiness'] = 'medium-low'
            elif burstiness < 0.5:
                score += 3
                details['burstiness'] = 'medium'
            else:
                details['burstiness'] = 'high (Human)'
    
    # ============================================================
    # 8. AI SIGNALS & CLICHÉS (0-10)
    # ============================================================
    
    ai_signals = [
        'in today\'s world', 'it is important to note', 'it is worth noting',
        'plays a crucial role', 'plays a vital role', 'plays an important role',
        'in conclusion', 'furthermore', 'moreover', 'additionally',
        'delve', 'tapestry', 'testament', 'beacon', 'paramount',
        'seamless', 'harness', 'unlock', 'demystify', 'holistic',
        'in the modern era', 'as a result', 'consequently',
        'on the other hand', 'this article will', 'we will explore',
        'generated using', 'fallback'
    ]
    
    signal_count = sum(1 for signal in ai_signals if signal in text_lower)
    score += min(10, signal_count * 2)
    details['ai_signals'] = signal_count
    
    # ============================================================
    # 9. BONUS: Supervised Classifier (Simulated)
    # ============================================================
    
    # This simulates what a real ML model would do
    # Uses all features above to make a final prediction
    
    features = {
        'ttr': ttr if 'ttr' in details else 0.5,
        'func_ratio': func_ratio if 'func_ratio' in details else 40,
        'repetition': repeat_ratio if 'repeat_ratio' in details else 0.2,
        'burstiness': burstiness if 'burstiness' in details else 0.3,
        'perplexity': perplexity if 'perplexity' in details else 15,
    }
    
    # Simple weighted classifier
    ml_score = 0
    
    # Feature 1: TTR (low = AI)
    if features['ttr'] < 0.4:
        ml_score += 15
    elif features['ttr'] < 0.5:
        ml_score += 8
    
    # Feature 2: Function word ratio (low = AI)
    if features['func_ratio'] < 35:
        ml_score += 15
    elif features['func_ratio'] < 40:
        ml_score += 8
    
    # Feature 3: Repetition (high = AI)
    if features['repetition'] > 0.3:
        ml_score += 10
    elif features['repetition'] > 0.2:
        ml_score += 5
    
    # Feature 4: Burstiness (low = AI)
    if features['burstiness'] < 0.2:
        ml_score += 10
    elif features['burstiness'] < 0.35:
        ml_score += 5
    
    # Feature 5: Perplexity (low = AI)
    if features['perplexity'] < 10:
        ml_score += 10
    elif features['perplexity'] < 20:
        ml_score += 5
    
    # Add ML score to total
    score += min(10, ml_score // 10)
    details['ml_score'] = ml_score
    
    # ============================================================
    # FINAL ADJUSTMENT
    # ============================================================
    
    # Adjust for short texts
    if word_count < 100:
        score = score * 0.8
    elif word_count < 200:
        score = score * 0.9
    
    # Final score
    final_score = min(100, max(0, int(score)))
    details['total'] = final_score
    
    return final_score


# ============================================================
# DETAILED REPORT FUNCTION
# ============================================================

def get_detailed_report(text):
    """Get comprehensive report with all metrics"""
    if not text or not text.strip():
        return {"total": 0, "error": "No text provided"}
    
    words = text.split()
    word_count = len(words)
    
    if word_count < 30:
        return {"total": 0, "error": "Text too short"}
    
    # Calculate all metrics
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip().split()) > 2]
    
    # Type-Token Ratio
    unique_words = set(w.lower() for w in words if len(w) > 2)
    ttr = len(unique_words) / word_count if word_count > 0 else 0
    
    # Function Word Ratio
    function_words = ['the', 'of', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 
                     'in', 'into', 'through', 'during', 'including', 'without',
                     'i', 'you', 'we', 'they', 'he', 'she', 'it', 'my', 'your',
                     'our', 'their', 'him', 'her', 'us', 'them']
    func_count = sum(1 for w in words if w.lower() in function_words)
    func_ratio = func_count / word_count * 100 if word_count > 0 else 0
    
    # Burstiness
    if len(sentences) >= 3:
        lengths = [len(s.split()) for s in sentences if len(s.split()) > 2]
        if len(lengths) > 1:
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std_dev = math.sqrt(variance)
            burstiness = std_dev / avg_len if avg_len > 0 else 0
        else:
            burstiness = 0
    else:
        burstiness = 0
    
    # Perplexity (simplified)
    perplexity = get_perplexity(text) if 'get_perplexity' in globals() else 0
    
    # AI Signals
    ai_signals = [
        'in today\'s world', 'it is important to note', 'plays a crucial role',
        'in conclusion', 'furthermore', 'moreover', 'additionally',
        'delve', 'tapestry', 'testament', 'beacon', 'paramount'
    ]
    signal_count = sum(1 for signal in ai_signals if signal in text.lower())
    
    # POS Tags
    pos_tags = simple_pos_tagger(text)
    if pos_tags:
        pos_counts = Counter(pos_tags)
        total_pos = len(pos_tags)
        noun_ratio = pos_counts.get('NOUN', 0) / total_pos if total_pos > 0 else 0
        pron_ratio = pos_counts.get('PRON', 0) / total_pos if total_pos > 0 else 0
        verb_ratio = pos_counts.get('VERB', 0) / total_pos if total_pos > 0 else 0
    else:
        noun_ratio = pron_ratio = verb_ratio = 0
    
    # Final score
    ai_score = detect_ai(text)
    
    return {
        "total": ai_score,
        "word_count": word_count,
        "sentence_count": len(sentences),
        "unique_words": len(unique_words),
        "type_token_ratio": round(ttr, 3),
        "function_word_ratio": round(func_ratio, 1),
        "burstiness": round(burstiness, 3),
        "perplexity": round(perplexity, 1) if perplexity else 0,
        "ai_signals_found": signal_count,
        "noun_ratio": round(noun_ratio, 2),
        "pronoun_ratio": round(pron_ratio, 2),
        "verb_ratio": round(verb_ratio, 2),
        "interpretation": "AI-generated" if ai_score > 50 else "Human-written"
    }


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_perplexity(text):
    """Calculate perplexity for a given text"""
    words = text.lower().split()
    if len(words) < 3:
        return 0
    
    # Simple n-gram probability
    bigrams = []
    for i in range(len(words) - 1):
        bigrams.append((words[i], words[i+1]))
    
    if not bigrams:
        return 0
    
    unique_bigrams = set(bigrams)
    bigram_freq = Counter(bigrams)
    
    # Calculate probability (simplified)
    total_bigrams = len(bigrams)
    prob_sum = 0
    for gram, count in bigram_freq.items():
        prob = count / total_bigrams
        if prob > 0:
            prob_sum += math.log2(prob)
    
    if total_bigrams > 0:
        perplexity = 2 ** (-prob_sum / total_bigrams)
        return perplexity
    return 0