
import re
import random
import humano  # humano library for NLP-based humanization

HUMANIZER_SYSTEM_PROMPT = """
You are an expert humanizing editor. Your sole job is to rewrite the provided AI-generated text so that it reads naturally, passes AI detection tests (high perplexity and burstiness), and retains 100% of the original factual meaning.
"""

def humanize_text(text, use_humano=True, strength="high", personality="casual"):
    """
    ULTIMATE HUMANIZER - Aims for 0% AI Score and 0% Plagiarism
    Contains 500+ keywords, phrases, and patterns for maximum humanization
    
    Now with humano integration for context-aware NLP-based humanization.
    
    Parameters:
    - text: AI-generated text
    - use_humano: bool - whether to use humano library (default: True)
    - strength: "low", "medium", "high" (default: "high")
    - personality: "balanced", "casual", "confident", "analytical" (default: "casual")
    """
    if not text or not text.strip():
        return text

    # ============================================================
    # STEP 0: HUMANO INTEGRATION (NLP-based humanization)
    # ============================================================
    
    if use_humano:
        try:
            result = humano.humanize(
                text,
                strength=strength,
                personality=personality
            )
            
            if result['success']:
                # Start with humano's output
                text = result['humanized_content']
                print(f" Humano: {result.get('transformations_applied', 0)} transformations applied")
                print(f" Context detected: {result.get('context_detected', 'unknown')}")
            else:
                print(f" Humano failed: {result.get('error')}")
                # Continue with rule-based humanization
                
        except Exception as e:
            print(f" Humano error: {e}. Falling back to rule-based humanization.")
            # Continue with rule-based humanization

    # ============================================================
    # STEP 1: COMPLETELY REMOVE ALL AI SIGNATURES (100+ patterns)
    # ============================================================
    
    ai_signatures = [
        # Article starters
        r'This article provides a comprehensive overview.*?\.',
        r'This article provides a general overview.*?\.',
        r'This guide provides.*?\.',
        r'consider exploring additional resources.*?\.',
        r'For more detailed information.*?\.',
        r'consulting with experts.*?\.',
        r'Key considerations include:?',
        r'Important considerations include:?',
        r'plays an? (important|crucial|vital) role in understanding .*?\.',
        r'there are several important factors to consider when exploring this area\.',
        r'experts agree that .*? is fundamental to grasping the broader context of .*?\.',
        r'is fundamental to grasping the broader context of .*?\.',
        r'Note:.*?\.',
        r'\[.*?\]',
        r'continues to shape our understanding of modern trends and practices\.',
        r'reveals complex interconnections between various components\.',
        r'Understanding these relationships provides deeper insights\.',
        r'\*Generated using.*?technology\*',
        r'---\s*\*Generated using.*?technology\*',
        r'1\. 1\.',
        r'2\. 2\.',
        r'In today\'s world,',
        r'It is important to note that',
        r'Furthermore,',
        r'Moreover,',
        r'Additionally,',
        r'As a result,',
        r'Consequently,',
        r'On the other hand,',
        r'In the modern era,',
        r'It is worth mentioning that',
        r'This article will explore',
        r'In recent years,',
        r'It is essential to',
        r'First and foremost,',
        r'Last but not least,',
        r'Needless to say,',
        r'It goes without saying that',
        r'It should be noted that',
        r'It is worth noting that',
        r'It is interesting to note that',
        r'It is important to understand that',
        r'It is crucial to understand that',
        r'It is vital to understand that',
        r'It is essential to understand that',
        # More signatures
        r'This paper aims to',
        r'This study focuses on',
        r'This research examines',
        r'This analysis explores',
        r'This investigation delves into',
        r'This work seeks to',
        r'This essay argues that',
        r'This report outlines',
        r'This document provides',
        r'This article argues',
        r'This piece explores',
        r'This text examines',
        r'According to recent studies',
        r'Based on the findings',
        r'As demonstrated by research',
        r'As shown in the literature',
        r'Research indicates that',
        r'Studies show that',
        r'Evidence suggests that',
        r'Findings reveal that',
        r'Data indicates that',
        r'Analysis shows that',
        r'Results demonstrate that',
        r'These findings highlight',
        r'The results suggest',
        r'Our analysis reveals',
        r'it\'s essential to',
        r'it is essential to',
        r'essential to ensure',
        r'potential solutions',
        r'crop yields',
        r'it\'s worth noting',
        r'it is worth noting',
        r'plays a vital role',
        r'plays an important role',
        r'plays a crucial role',
        r'plays a key role',
        r'plays a significant role',
        r'serves as a',
        r'acts as a',
        r'functions as a',
        r'can be seen as',
        r'can be viewed as',
        r'can be considered',
        r'is regarded as',
        r'is perceived as',
        r'is viewed as',
        r'is seen as',
        r'is considered',
        r'has been shown to',
        r'has been proven to',
        r'has been found to',
        r'has been demonstrated to',
        r'research has shown',
        r'studies have shown',
        r'evidence suggests',
        r'findings indicate',
        r'data shows',
        r'statistics reveal',
        r'numbers show',
        r'figures indicate',
        r'this suggests that',
        r'this indicates that',
        r'this implies that',
        r'this means that',
        r'this shows that',
        r'this demonstrates that',
        r'this proves that',
        r'in other words',
        r'that is to say',
        r'to put it differently',
        r'to put it simply',
        r'to clarify',
        r'to elaborate',
        r'to explain further',
        r'profound impact',
        r'demands attention',
        r'taking a toll',
        r'it\'s a complex issue',
        r'but one that',
        r'around the globe',
        r'not all doom and gloom',
        r'concerted effort',
        r'payoff will be worth it',
        r'better equipped to withstand',
        r'generations to come',
        r'stable food supply',
        r'optimal temperature ranges',
        r'deviations can impact',
        r'heat stress can reduce',
        r'significant losses',
        r'forcing farmers to adapt',
        r'no longer thrive',
        r'food shortages',
        r'economic disruptions',
        r'already feeling the effects',
        r'suitable growing areas',
        r'moving towards higher altitudes',
        r'favorable conditions',
        r'significantly reduce',
        r'increase pesticide use',
        r'environmental and health concerns',
        r'mitigate the impacts',
        r'adopt innovative',
        r'build resilience',
        r'can help manage risks',
        r'safety net during',
        r'water-scarce periods',
        r'climate-smart technologies',
        r'can significantly aid',
        r'coordinated policy efforts',
    ]
    for pattern in ai_signatures:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)

    # Fix duplicate title in headings
    text = re.sub(r'(# .+?) #', r'\1\n\n## ', text)

    # Remove all robotic introductory phrases
    robotic_starters = [
        r'\bHere\'s the thing:\b',
        r'\bInterestingly,\b',
        r'\bIn my experience,\b',
        r'\bIt is worth mentioning that\b',
        r'\bcontinues to shape\b',
        r'\breveals complex\b',
        r'\bprovides deeper insights\b',
        r'\bworth noting\b',
        r'\bit\'s important to remember\b',
        r'\bnotably,\b',
        r'\bsignificantly,\b',
        r'\bimportantly,\b',
        r'\bcrucially,\b',
        r'\bespecially,\b',
        r'\bparticularly,\b',
        r'\bfundamentally,\b',
        r'\bessentially,\b',
        r'\bsimply put,\b',
        r'\bin other words,\b',
        r'\bthat is to say,\b',
        r'\bin essence,\b',
        r'\bto put it simply,\b',
        r'\bto put it differently,\b',
        r'\bto clarify,\b',
        r'\bto elaborate,\b',
        r'\bto expand,\b',
        r'\bto illustrate,\b',
        r'\bto demonstrate,\b',
        r'\bto emphasize,\b',
        r'\bto highlight,\b',
        r'\bto stress,\b',
        r'\bto underscore,\b',
        r'\bto reiterate,\b',
        r'\bto repeat,\b',
        r'\bto summarize,\b',
    ]
    for starter in robotic_starters:
        text = re.sub(starter, '', text, flags=re.IGNORECASE)
    # ============================================================
    # STEP 2: REPLACE REPETITIVE PHRASES WITH VARIATIONS
    # ============================================================
    
    repetitive_phrases = [
        # "it's essential to" variations
        (r'\bit\'s essential to\b', random.choice(['you need to', 'it helps to', 'it pays to', 'it\'s good to', 'try to', 'make sure to', 'don\'t forget to', 'always remember to', 'it\'s wise to', 'it\'s smart to'])),
        (r'\bit is essential to\b', random.choice(['you need to', 'it helps to', 'it pays to', 'it\'s good to', 'try to', 'make sure to', 'don\'t forget to', 'always remember to'])),
        (r'\bessential to ensure\b', random.choice(['key to making sure', 'important for', 'needed to', 'helps guarantee', 'makes sure', 'ensures'])),
        (r'\bpotential solutions\b', random.choice(['ways to fix', 'possible answers', 'things to try', 'options', 'approaches', 'ideas to explore'])),
        (r'\bcrop yields\b', random.choice(['harvest output', 'farm production', 'agricultural output', 'food production', 'harvest results', 'farming results'])),
        
        # More repetitive patterns
        (r'\bit\'s worth noting\b', random.choice(['remember', 'keep in mind', 'note that', 'it\'s important to know', 'don\'t forget'])),
        (r'\bit is worth noting\b', random.choice(['remember', 'keep in mind', 'note that', 'it\'s important to know'])),
        (r'\bplays a vital role\b', random.choice(['is key to', 'matters a lot', 'is important for', 'helps with', 'affects'])),
        (r'\bplays an important role\b', random.choice(['is key to', 'matters a lot', 'is important for', 'helps with', 'affects'])),
        (r'\bplays a crucial role\b', random.choice(['is key to', 'matters a lot', 'is important for', 'helps with', 'affects'])),
        (r'\bplays a key role\b', random.choice(['is key to', 'matters a lot', 'is important for', 'helps with', 'affects'])),
        (r'\bplays a significant role\b', random.choice(['is key to', 'matters a lot', 'is important for', 'helps with', 'affects'])),
        (r'\bserves as a\b', random.choice(['works as a', 'acts like a', 'is a', 'functions as a'])),
        (r'\bacts as a\b', random.choice(['works as a', 'serves as a', 'is a', 'functions like a'])),
        (r'\bfunctions as a\b', random.choice(['works as a', 'serves as a', 'is a', 'acts like a'])),
        (r'\bcan be seen as\b', random.choice(['looks like', 'seems like', 'appears as', 'is like'])),
        (r'\bcan be viewed as\b', random.choice(['looks like', 'seems like', 'appears as', 'is like'])),
        (r'\bcan be considered\b', random.choice(['could be', 'might be', 'is often', 'is usually'])),
        (r'\bis regarded as\b', random.choice(['is known as', 'is called', 'is seen as', 'is thought of as'])),
        (r'\bis perceived as\b', random.choice(['is seen as', 'is thought of as', 'is viewed as', 'comes across as'])),
        (r'\bis viewed as\b', random.choice(['is seen as', 'is thought of as', 'is regarded as', 'comes across as'])),
        (r'\bis seen as\b', random.choice(['is thought of as', 'is viewed as', 'is regarded as', 'comes across as'])),
        (r'\bis considered\b', random.choice(['is seen as', 'is viewed as', 'is regarded as', 'is thought to be'])),
        (r'\bhas been shown to\b', random.choice(['shows', 'demonstrates', 'proves', 'indicates', 'suggests'])),
        (r'\bhas been proven to\b', random.choice(['shows', 'demonstrates', 'proves', 'indicates', 'suggests'])),
        (r'\bhas been found to\b', random.choice(['shows', 'demonstrates', 'proves', 'indicates', 'suggests'])),
        (r'\bhas been demonstrated to\b', random.choice(['shows', 'demonstrates', 'proves', 'indicates', 'suggests'])),
        (r'\bresearch has shown\b', random.choice(['studies show', 'we know', 'it\'s clear', 'the data shows'])),
        (r'\bstudies have shown\b', random.choice(['research shows', 'we know', 'it\'s clear', 'the data shows'])),
        (r'\bevidence suggests\b', random.choice(['it looks like', 'the signs point to', 'we can see that', 'it seems'])),
        (r'\bfindings indicate\b', random.choice(['we found that', 'the results show', 'it turns out', 'we discovered'])),
        (r'\bdata shows\b', random.choice(['the numbers say', 'statistics show', 'we can see', 'the information proves'])),
        (r'\bstatistics reveal\b', random.choice(['the numbers say', 'data shows', 'we can see', 'the information proves'])),
        (r'\bnumbers show\b', random.choice(['the data says', 'statistics show', 'we can see', 'the information proves'])),
        (r'\bfigures indicate\b', random.choice(['the numbers say', 'data shows', 'we can see', 'the information proves'])),
        (r'\bthis suggests that\b', random.choice(['which means', 'so', 'therefore', 'this tells us', 'in other words'])),
        (r'\bthis indicates that\b', random.choice(['which means', 'so', 'therefore', 'this tells us', 'in other words'])),
        (r'\bthis implies that\b', random.choice(['which means', 'so', 'therefore', 'this tells us', 'in other words'])),
        (r'\bthis means that\b', random.choice(['which means', 'so', 'therefore', 'this tells us', 'in other words'])),
        (r'\bthis shows that\b', random.choice(['which means', 'so', 'therefore', 'this tells us', 'in other words'])),
        (r'\bthis demonstrates that\b', random.choice(['which means', 'so', 'therefore', 'this tells us', 'in other words'])),
        (r'\bthis proves that\b', random.choice(['which means', 'so', 'therefore', 'this tells us', 'in other words'])),
        (r'\bin other words\b', random.choice(['simply put', 'that is', 'meaning', 'so', 'in simpler terms'])),
        (r'\bthat is to say\b', random.choice(['simply put', 'that is', 'meaning', 'so', 'in simpler terms'])),
        (r'\bto put it differently\b', random.choice(['simply put', 'that is', 'meaning', 'so', 'in simpler terms'])),
        (r'\bto put it simply\b', random.choice(['simply put', 'that is', 'meaning', 'so', 'in simpler terms'])),
        (r'\bto clarify\b', random.choice(['to be clear', 'let me explain', 'to be specific', 'to be exact'])),
        (r'\bto elaborate\b', random.choice(['to explain further', 'to add more', 'to go deeper', 'to expand on this'])),
        (r'\bto explain further\b', random.choice(['to elaborate', 'to add more', 'to go deeper', 'to expand on this'])),
    ]
    
    for pattern, replacement in repetitive_phrases:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        # ============================================================
    # STEP 3: ADD SHORT PUNCHY SENTENCES (Reduce sentence length)
    # ============================================================
    
    def add_short_sentences(text):
        """Break long sentences into shorter ones"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        new_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            # If sentence is too long (>25 words), break it
            if len(words) > 25:
                # Split at natural break points
                breaks = [' and ', ' but ', ' so ', ' because ', ' which ', ' that ']
                for br in breaks:
                    if br in sentence.lower():
                        parts = sentence.split(br, 1)
                        if len(parts[0].split()) > 8:
                            # Add first part as short sentence
                            new_sentences.append(parts[0] + '.')
                            # Add second part with connector
                            connector = br.strip()
                            second = parts[1]
                            if second and not second[0].isupper():
                                second = second[0].upper() + second[1:]
                            new_sentences.append(f"{connector.capitalize()} {second}")
                            break
                else:
                    # If no break found, split at midpoint
                    mid = len(words) // 2
                    part1 = ' '.join(words[:mid])
                    part2 = ' '.join(words[mid:])
                    new_sentences.append(part1 + '.')
                    if part2 and not part2[0].isupper():
                        part2 = part2[0].upper() + part2[1:]
                    new_sentences.append(part2 + '.')
            else:
                new_sentences.append(sentence)
        
        return '. '.join(new_sentences)
    
    text = add_short_sentences(text)
        # ============================================================
    # STEP 3.5: BREAK VERY LONG SENTENCES (41+ words)
    # ============================================================
    
    def break_very_long_sentences(text):
        """Break sentences with 41+ words into shorter ones"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        new_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 40:
                # Split at natural break points
                break_points = ['. ', ', ', '; ', ' and ', ' but ', ' so ', ' because ']
                for bp in break_points:
                    if bp in sentence:
                        parts = sentence.split(bp, 1)
                        if len(parts[0].split()) > 10:
                            new_sentences.append(parts[0] + '.')
                            second = parts[1]
                            if second and not second[0].isupper():
                                second = second[0].upper() + second[1:]
                            new_sentences.append(second)
                            break
                else:
                    # Force break at midpoint
                    mid = len(words) // 2
                    part1 = ' '.join(words[:mid])
                    part2 = ' '.join(words[mid:])
                    new_sentences.append(part1 + '.')
                    if part2 and not part2[0].isupper():
                        part2 = part2[0].upper() + part2[1:]
                    new_sentences.append(part2 + '.')
            else:
                new_sentences.append(sentence)
        
        return '. '.join(new_sentences)
    
    text = break_very_long_sentences(text)
        # ============================================================
    # STEP 3.6: REPLACE LONG WORDS (8+ chars) WITH SHORT WORDS
    # ============================================================
    
    long_words = [
        # Long words → Short words
        (r'consequences', 'results'),
        (r'extreme', 'severe'),
        (r'infrastructure', 'buildings'),
        (r'resilience', 'strength'),
        (r'ecological', 'natural'),
        (r'ecofriendly', 'green'),
        (r'fertilizers', 'plant food'),
        (r'overwhelming', 'clear'),
        (r'devastating', 'bad'),
        (r'far-reaching', 'big'),
        (r'significant', 'big'),
        (r'particularly', 'especially'),
        (r'resilient', 'strong'),
        (r'unpredictable', 'unstable'),
        (r'mitigate', 'lessen'),
        (r'interconnected', 'linked'),
        (r'cultivation', 'farming'),
        (r'demonstrate', 'show'),
        (r'comprehensive', 'full'),
        (r'revolutionize', 'change'),
        (r'substantial', 'large'),
        (r'considerable', 'big'),
        (r'ultimately', 'finally'),
        (r'additional', 'extra'),
        (r'alternative', 'other'),
        (r'consistent', 'steady'),
        (r'eventually', 'later'),
        (r'increasingly', 'more'),
        (r'opportunities', 'chances'),
        (r'particularly', 'especially'),
        (r'potential', 'possible'),
        (r'production', 'output'),
        (r'productivity', 'output'),
        (r'remarkable', 'great'),
        (r'sufficient', 'enough'),
        (r'sustainable', 'green'),
        (r'technological', 'tech'),
        (r'traditionally', 'usually'),
        (r'understandably', 'naturally'),
        (r'utilize', 'use'),
    ]
    
    for pattern, replacement in long_words:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # ============================================================
    # STEP 4: REPLACE LONG WORDS WITH SHORTER ONES
    # ============================================================
    
    long_words = [
        (r'particularly concerning', 'especially worrying'),
        (r'significant challenge', 'big challenge'),
        (r'increasingly unpredictable', 'harder to predict'),
        (r'devastating crops', 'destroying crops'),
        (r'far-reaching consequences', 'big consequences'),
        (r'exacerbating existing', 'making worse'),
        (r'leveraging technology', 'using technology'),
        (r'innovation', 'new ideas'),
        (r'conservation agriculture', 'soil-friendly farming'),
        (r'agroforestry', 'tree farming'),
        (r'integrated pest management', 'smart pest control'),
        (r'greenhouse gas emissions', 'carbon emissions'),
        (r'resilient farming systems', 'strong farming systems'),
        (r'precipitation patterns', 'rainfall patterns'),
        (r'global population', 'world population'),
        (r'sustainable farming', 'eco-friendly farming'),
        (r'biodiversity', 'nature variety'),
        (r'mitigate the effects', 'lessen the impact'),
        (r'food security', 'having enough food'),
        (r'climate-resilient', 'weather-strong'),
        (r'economic inequalities', 'money gaps'),
        (r'profound effect', 'big effect'),
        (r'altering the face', 'changing the shape'),
        (r'devastating crops', 'ruining crops'),
        (r'challenging for farmers', 'tough for farmers'),
        (r'unpredictability', 'uncertainty'),
        (r'significant challenge', 'major challenge'),
        (r'particularly concerning', 'very worrying'),
        (r'exacerbating', 'making worse'),
        (r'leveraging', 'using'),
        (r'innovation', 'new ideas'),
    ]
    
    for pattern, replacement in long_words:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # ============================================================
    # STEP 4.5: REMOVE AI SENTENCE STARTERS
    # ============================================================
    
    ai_starters = [
        # Remove or replace formal starters
        (r'One of the most significant', 'A major'),
        (r'The evidence of climate change is', 'Climate change is'),
        (r'The trends are clear:', ''),
        (r'It\'s also essential that', 'We also need to'),
        (r'By working together,', 'Together,'),
        (r'Have you ever wanted to try something new\?', ''),
        (r'Take a moment to think:', ''),
        (r'Here\'s a thought:', ''),
        (r'Let\'s be honest,', ''),
        (r'What most people don\'t realize is,', ''),
        (r'For example,', 'For instance,'),
        (r'Similarly,', 'Also,'),
        (r'Now These events', 'These events'),
        (r'Yet One of the most', 'One of the most'),
        (r'And Find ways', 'Finding ways'),
        (r'But Take a moment', 'Take a moment'),
        (r'Now They', 'They'),
        (r'And For example', 'For example'),
        (r'As we population', 'As the population'),
        (r'we need to we', 'we need to'),
        (r'will require a overall', 'will require an overall'),
        (r'by around', 'by about'),
        (r'some studies suggesting', 'some studies show'),
        (r'we expect', 'is expected'),
        (r'a on agriculture', 'an impact on agriculture'),
        (r'it\'s not just', 'it\'s not only'),
        (r'the trend is clear', ''),
        (r'overall, the trend is clear', 'overall'),
    ]
    
    for pattern, replacement in ai_starters:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # ============================================================
    # STEP 5.5: ADD SHORT PUNCHY SENTENCES (≤8 words)
    # ============================================================
    
    def add_punchy_sentences(text):
        """Add short punchy sentences to mimic human writing"""
        paragraphs = text.split('\n\n')
        punchy_lines = [
            "That's a big problem.",
            "It's getting worse.",
            "We can't ignore this.",
            "Farmers are struggling.",
            "The clock is ticking.",
            "Something must change.",
            "It's simple really.",
            "We need solutions now.",
            "Time is running out.",
            "What can we do?",
            "It's up to us.",
            "No easy answers.",
            "But there's hope.",
            "Change is possible.",
            "We have the tools.",
            "It starts with us.",
            "Every step counts.",
            "Don't wait any longer.",
            "The choice is ours.",
            "We know what to do.",
        ]
        
        for idx, para in enumerate(paragraphs):
            if para.strip() and not para.strip().startswith('#'):
                # Add punchy sentence at end of paragraph (15% chance)
                if random.random() < 0.15:
                    punchy = random.choice(punchy_lines)
                    paragraphs[idx] = para + ' ' + punchy
                
                # Add punchy sentence in middle (10% chance)
                if random.random() < 0.10:
                    sentences = para.split('. ')
                    if len(sentences) > 3:
                        punchy = random.choice(punchy_lines)
                        insert_pos = len(sentences) // 2
                        sentences.insert(insert_pos, punchy)
                        paragraphs[idx] = '. '.join(sentences)
        
        return '\n\n'.join(paragraphs)
    
    text = add_punchy_sentences(text)
    # ============================================================
    # STEP 5: ADD MORE PRONOUNS (Increase function word ratio)
    # ============================================================
    
    # Replace nouns with pronouns where appropriate
    pronoun_replacements = [
        (r'farmers', 'they'),
        (r'climate change', 'it'),
        (r'we', 'we'),
        (r'farmers and policymakers', 'we'),
        (r'these approaches', 'these'),
        (r'this unpredictability', 'this'),
        (r'the weather', 'it'),
    ]
    
    # Add more personal pronouns naturally
    def add_pronouns(text):
        """Add more personal pronouns to text"""
        paragraphs = text.split('\n\n')
        for idx, para in enumerate(paragraphs):
            if para.strip() and not para.strip().startswith('#'):
                # Add "we" or "you" occasionally
                if random.random() < 0.20:
                    sentences = para.split('. ')
                    if len(sentences) > 2:
                        target = random.randint(1, len(sentences) - 1)
                        if 'farmers' in sentences[target].lower() or 'people' in sentences[target].lower():
                            sentences[target] = 'We ' + sentences[target][0].lower() + sentences[target][1:]
                        elif 'climate' in sentences[target].lower():
                            sentences[target] = 'It ' + sentences[target][0].lower() + sentences[target][1:]
                        paragraphs[idx] = '. '.join(sentences)
        return '\n\n'.join(paragraphs)
    
    text = add_pronouns(text)
        # ============================================================
    # STEP 3: ADD HUMAN VOICE (Remove formal AI tone)
    # ============================================================
    
    human_voice = [
        # Remove formal phrases
        (r'profound impact', random.choice(['big effect', 'serious impact', 'major change', 'real difference'])),
        (r'demands attention', random.choice(['needs our focus', 'can\'t be ignored', 'deserves a closer look', 'we need to pay attention'])),
        (r'taking a toll', random.choice(['hurting', 'affecting', 'impacting', 'causing problems for'])),
        (r'around the globe', random.choice(['everywhere', 'all over the world', 'across the planet', 'in many places'])),
        (r'not all doom and gloom', random.choice(['it\'s not all bad', 'there\'s hope', 'things can improve', 'we can make it better'])),
        (r'concerted effort', random.choice(['teamwork', 'working together', 'combined effort', 'everyone pitching in'])),
        (r'payoff will be worth it', random.choice(['it\'ll be worth it', 'the results will pay off', 'it\'s worth the effort', 'good things will come'])),
        (r'better equipped to withstand', random.choice(['stronger against', 'ready for', 'better able to handle', 'more prepared for'])),
        (r'generations to come', random.choice(['our kids and grandkids', 'future generations', 'people in the future', 'our children'])),
        (r'stable food supply', random.choice(['enough food', 'steady food supply', 'reliable food sources', 'food security'])),
        (r'optimal temperature ranges', random.choice(['best temperatures', 'ideal heat levels', 'perfect growing conditions', 'right temperatures'])),
        (r'deviations can impact', random.choice(['changes can affect', 'shifts can hurt', 'differences can change', 'variations can impact'])),
        (r'heat stress can reduce', random.choice(['too much heat can lower', 'high temperatures can cut', 'hot weather can reduce', 'heat can affect'])),
        (r'significant losses', random.choice(['big losses', 'serious damage', 'major setbacks', 'heavy losses'])),
        (r'forcing farmers to adapt', random.choice(['making farmers change', 'pushing farmers to adjust', 'causing farmers to shift', 'farmers have to adapt'])),
        (r'no longer thrive', random.choice(['don\'t grow well anymore', 'struggle to survive', 'can\'t flourish', 'have a hard time'])),
        (r'food shortages', random.choice(['not enough food', 'food scarcity', 'running low on food', 'food gaps'])),
        (r'economic disruptions', random.choice(['money problems', 'financial issues', 'economic trouble', 'business challenges'])),
        (r'already feeling the effects', random.choice(['already seeing changes', 'already affected', 'feeling it now', 'already impacted'])),
        (r'suitable growing areas', random.choice(['good places to grow', 'right areas for farming', 'ideal locations', 'best spots'])),
        (r'moving towards higher altitudes', random.choice(['shifting uphill', 'moving to higher ground', 'going to cooler spots', 'climbing higher'])),
        (r'favorable conditions', random.choice(['good conditions', 'ideal situations', 'perfect weather', 'right environment'])),
        (r'significantly reduce', random.choice(['cut down', 'lower', 'decrease', 'bring down'])),
        (r'increase pesticide use', random.choice(['use more pesticides', 'spray more chemicals', 'apply more pest control', 'use stronger chemicals'])),
        (r'environmental and health concerns', random.choice(['worries about nature and health', 'health and environment issues', 'safety and nature problems', 'health and ecological risks'])),
        (r'mitigate the impacts', random.choice(['lessen the effects', 'reduce the damage', 'soften the blow', 'ease the impact'])),
        (r'adopt innovative', random.choice(['try new', 'use modern', 'adopt fresh', 'implement creative'])),
        (r'build resilience', random.choice(['become stronger', 'build strength', 'get tougher', 'become more resistant'])),
        (r'can help manage risks', random.choice(['helps handle problems', 'can reduce risks', 'helps deal with issues', 'can control challenges'])),
        (r'safety net during', random.choice(['backup when', 'protection during', 'support in', 'help when'])),
        (r'water-scarce periods', random.choice(['dry times', 'when water is low', 'drought periods', 'water shortage times'])),
        (r'climate-smart technologies', random.choice(['smart farming tech', 'climate-friendly tools', 'advanced agriculture', 'new farming methods'])),
        (r'can significantly aid', random.choice(['can really help', 'greatly assists', 'can support', 'helps a lot'])),
        (r'coordinated policy efforts', random.choice(['governments working together', 'united policy action', 'combined government plans', 'joint policy work'])),
        
        # Remove ellipsis (...)
        (r'\.\.\.', random.choice(['.', '.', '.', '...', '—'])),
    ]
    
    for pattern, replacement in human_voice:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # ============================================================
    # STEP 2: REMOVE ALL AI CLICHÉS (150+ patterns)
    # ============================================================
    
    cliches = [
        # Basic AI clichés
        (r'\bdelve\b', 'explore'),
        (r'\btapestry\b', 'mix'),
        (r'\btestament\b', 'proof'),
        (r'\bbeacon\b', 'guide'),
        (r'\bparamount\b', 'very important'),
        (r'\bseamless\b', 'smooth'),
        (r'\belevated\b', 'raised'),
        (r'\bvital role\b', 'key part'),
        (r'\bcrucial\b', 'important'),
        (r'\blandscape\b', 'world'),
        (r'\bharness\b', 'use'),
        (r'\bgame-changer\b', 'big change'),
        (r'\bunlock\b', 'reveal'),
        (r'\bdive deep\b', 'explore'),
        (r'\bdemystify\b', 'explain'),
        (r'\bholistic\b', 'overall'),
        (r'\brealm\b', 'area'),
        (r'\bnestled\b', 'located'),
        (r'\bvibrant\b', 'lively'),
        (r'\bFurthermore,\b', 'Plus,'),
        (r'\bMoreover,\b', 'On top of that,'),
        (r'\bAdditionally,\b', 'And,'),
        (r'\bIn conclusion,\b', 'Bottom line:'),
        (r'\bIt is important to note that\b', 'Keep in mind that'),
        (r'\bOn the other hand,\b', 'That said,'),
        (r'\bAs a result,\b', 'Because of this,'),
        (r'\bConsequently,\b', 'So,'),
        (r'\btreasure trove\b', 'collection'),
        (r'\bhotspot\b', 'destination'),
        (r'\bbreathtaking\b', 'beautiful'),
        (r'\bpristine\b', 'clean'),
        (r'\bdiverse\b', 'varied'),
        (r'\bwarm hospitality\b', 'friendly people'),
        (r'\brich cultural heritage\b', 'deep history'),
        (r'\bmust-visit\b', 'worth visiting'),
        (r'\bunforgettable\b', 'memorable'),
        (r'\bworld of\b', 'field of'),
        (r'\bin the realm of\b', 'in'),
        (r'\bcutting-edge\b', 'advanced'),
        (r'\bstate-of-the-art\b', 'modern'),
        (r'\btransformative\b', 'major'),
        (r'\bdata-driven\b', 'fact-based'),
        (r'\bIn today\'s world\b', 'Today'),
        (r'\bIn the modern era\b', 'Nowadays'),
        (r'\bThis article will explore\b', 'We examine'),
        (r'\bexplore the world of\b', 'discover'),
        (r'\bunlock the potential\b', 'reveal the possibilities'),
        (r'\blet\'s dive into\b', 'let\'s look at'),
        (r'\bit\'s worth noting\b', 'remember'),
        (r'\bwhen it comes to\b', 'in terms of'),
        (r'\bin terms of\b', 'regarding'),
        (r'\bthe key takeaway\b', 'the main point'),
        (r'\bit\'s important to remember\b', 'remember'),
        (r'\bcontinues to shape\b', 'is changing'),
        (r'\breveals complex\b', 'shows how'),
        (r'\bprovides deeper insights\b', 'helps us understand'),
        (r'\bnotable example\b', 'good example'),
        (r'\bsignificant impact\b', 'big impact'),
        (r'\bmeaningful way\b', 'effective way'),
        (r'\bvaluable insights\b', 'useful information'),
        (r'\bplays a important role\b', 'is important'),
        (r'\bplays an important role\b', 'is important'),
        (r'\bis provided by\b', 'comes from'),
        (r'\bare provided by\b', 'come from'),
        (r'\bis used by\b', 'uses'),
        (r'\bare used by\b', 'use'),
        (r'\bis considered\b', 'is seen as'),
        (r'\bcan be seen\b', 'we can see'),
        (r'\bis found in\b', 'you\'ll find in'),
        # Additional clichés
        (r'\ba testament to\b', 'proof of'),
        (r'\ba beacon of\b', 'a guide to'),
        (r'\bparamount importance\b', 'very important'),
        (r'\bseamless integration\b', 'smooth integration'),
        (r'\belevated experience\b', 'better experience'),
        (r'\bharness the power\b', 'use the power'),
        (r'\bunlock the potential\b', 'reveal the potential'),
        (r'\bdive into\b', 'explore'),
        (r'\bdemystify the process\b', 'explain the process'),
        (r'\bholistic approach\b', 'overall approach'),
        (r'\bin the realm of\b', 'in'),
        (r'\bnestled in\b', 'located in'),
        (r'\bvibrant culture\b', 'lively culture'),
        (r'\bpristine beauty\b', 'clean beauty'),
        (r'\bdiverse range\b', 'wide range'),
        (r'\bunforgettable experience\b', 'memorable experience'),
        (r'\bcutting-edge technology\b', 'advanced technology'),
        (r'\bstate-of-the-art facilities\b', 'modern facilities'),
        (r'\btransformative power\b', 'major power'),
        (r'\bdata-driven insights\b', 'fact-based insights'),
        (r'\bmeaningful impact\b', 'real impact'),
        (r'\bvital importance\b', 'key importance'),
        (r'\bcritical factor\b', 'key factor'),
        (r'\bkey component\b', 'important part'),
        (r'\bfundamental aspect\b', 'basic aspect'),
        (r'\bcore principle\b', 'main principle'),
        (r'\bessential element\b', 'key element'),
        (r'\bcrucial step\b', 'important step'),
        (r'\bsignificant advantage\b', 'big advantage'),
        (r'\bmajor benefit\b', 'key benefit'),
        (r'\bprimary reason\b', 'main reason'),
        (r'\bcentral theme\b', 'main theme'),
        (r'\bunderlying concept\b', 'basic concept'),
        (r'\boverarching goal\b', 'main goal'),
        (r'\bunderlying principle\b', 'basic principle'),
        (r'\bdriving force\b', 'main force'),
        (r'\bkey driver\b', 'main driver'),
        (r'\bmajor factor\b', 'key factor'),
        (r'\bcontributing factor\b', 'key factor'),
        (r'\bdetermining factor\b', 'key factor'),
        (r'\bdecisive factor\b', 'key factor'),
        (r'\bcrucial element\b', 'key element'),
        (r'\bessential component\b', 'key component'),
        (r'\bfundamental building block\b', 'basic building block'),
        (r'\bcornerstone of\b', 'basis of'),
        (r'\bfoundation of\b', 'basis of'),
        (r'\bbackbone of\b', 'main part of'),
        (r'\bheart of\b', 'center of'),
        (r'\bcore of\b', 'center of'),
        (r'\bessence of\b', 'main point of'),
        # Academic AI clichés
        (r'\bmoreover,\b', 'plus,'),
        (r'\badditionally,\b', 'also,'),
        (r'\bfurthermore,\b', 'and,'),
        (r'\bsubsequently,\b', 'next,'),
        (r'\baccordingly,\b', 'so,'),
        (r'\bthus,\b', 'so,'),
        (r'\bhence,\b', 'that\'s why,'),
        (r'\btherefore,\b', 'so,'),
        (r'\bconversely,\b', 'on the other hand,'),
        (r'\bmeanwhile,\b', 'at the same time,'),
        (r'\bnevertheless,\b', 'still,'),
        (r'\bnonetheless,\b', 'even so,'),
        (r'\bnotwithstanding,\b', 'despite that,'),
        (r'\bconsequently,\b', 'because of that,'),
        # More AI words
        (r'\bfoster\b', 'encourage'),
        (r'\bfacilitate\b', 'make easier'),
        (r'\boptimize\b', 'improve'),
        (r'\bmaximize\b', 'increase'),
        (r'\bminimize\b', 'reduce'),
        (r'\benhance\b', 'improve'),
        (r'\baccelerate\b', 'speed up'),
        (r'\bstreamline\b', 'make simpler'),
        (r'\brevolutionize\b', 'change'),
        (r'\bdisrupt\b', 'change'),
        (r'\binnovate\b', 'create new'),
        (r'\bpioneer\b', 'lead the way'),
        (r'\bleverage\b', 'use'),
        (r'\bcapitalize\b', 'take advantage'),
        (r'\bempower\b', 'enable'),
        (r'\bengage\b', 'involve'),
        (r'\bencourage\b', 'support'),
        (r'\binspire\b', 'motivate'),
        (r'\bmotivate\b', 'encourage'),
        (r'\bdrive\b', 'push'),
        (r'\bpropel\b', 'push forward'),
        (r'\bcatalyze\b', 'spark'),
        (r'\bignite\b', 'spark'),
        (r'\bspark\b', 'start'),
        (r'\btrigger\b', 'start'),
        (r'\bgenerate\b', 'create'),
        (r'\bproduce\b', 'create'),
        (r'\bdevelop\b', 'create'),
        (r'\bcreate\b', 'make'),
        (r'\bformulate\b', 'create'),
        (r'\bdevise\b', 'create'),
        (r'\bdesign\b', 'create'),
        (r'\bimplement\b', 'put into practice'),
        (r'\bexecute\b', 'carry out'),
        (r'\bperform\b', 'do'),
        (r'\bconduct\b', 'do'),
        (r'\bundertake\b', 'do'),
        (r'\bcarry out\b', 'do'),
    ]
    for pattern, replacement in cliches:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # ============================================================
    # STEP 3: ADD CONTRACTIONS (50+ patterns)
    # ============================================================
    
    contractions = [
        (r'\bcannot\b', "can't"),
        (r'\bwill not\b', "won't"),
        (r'\bshould not\b', "shouldn't"),
        (r'\bis not\b', "isn't"),
        (r'\bare not\b', "aren't"),
        (r'\bdo not\b', "don't"),
        (r'\bdoes not\b', "doesn't"),
        (r'\bdid not\b', "didn't"),
        (r'\bI have\b', "I've"),
        (r'\bwe have\b', "we've"),
        (r'\bthey have\b', "they've"),
        (r'\bI am\b', "I'm"),
        (r'\bwe are\b', "we're"),
        (r'\bthey are\b', "they're"),
        (r'\bit is\b', "it's"),
        (r'\bthat is\b', "that's"),
        (r'\bthere is\b', "there's"),
        (r'\bhave not\b', "haven't"),
        (r'\bhas not\b', "hasn't"),
        (r'\bwere not\b', "weren't"),
        (r'\bwas not\b', "wasn't"),
        (r'\bmight not\b', "mightn't"),
        (r'\bcould not\b', "couldn't"),
        (r'\bwould not\b', "wouldn't"),
        (r'\bI will\b', "I'll"),
        (r'\byou will\b', "you'll"),
        (r'\bwe will\b', "we'll"),
        (r'\bthey will\b', "they'll"),
        (r'\bthat will\b', "that'll"),
        (r'\bthere will\b', "there'll"),
        (r'\bwhat is\b', "what's"),
        (r'\bwho is\b', "who's"),
        (r'\bwhere is\b', "where's"),
        (r'\bwhen is\b', "when's"),
        (r'\bwhy is\b', "why's"),
        (r'\bhow is\b', "how's"),
        (r'\bwhat are\b', "what're"),
        (r'\bwho are\b', "who're"),
        (r'\bI had\b', "I'd"),
        (r'\byou had\b', "you'd"),
        (r'\bwe had\b', "we'd"),
        (r'\bthey had\b', "they'd"),
        (r'\bI would\b', "I'd"),
        (r'\byou would\b', "you'd"),
        (r'\bwe would\b', "we'd"),
        (r'\bthey would\b', "they'd"),
        (r'\bI could\b', "I could"),
        (r'\byou could\b', "you could"),
        (r'\bwe could\b', "we could"),
        (r'\bthey could\b', "they could"),
        (r'\byou have\b', "you've"),
        (r'\bwe have\b', "we've"),
        (r'\bthey have\b', "they've"),
    ]
    for pattern, replacement in contractions:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # ============================================================
    # STEP 4: CONVERT PASSIVE TO ACTIVE VOICE (30+ patterns)
    # ============================================================
    
    passive = [
        (r'\bis provided by\b', 'comes from'),
        (r'\bare provided by\b', 'come from'),
        (r'\bis used by\b', 'uses'),
        (r'\bare used by\b', 'use'),
        (r'\bis considered\b', 'is seen as'),
        (r'\bcan be seen\b', 'we can see'),
        (r'\bis found in\b', 'you\'ll find in'),
        (r'\bwas created by\b', 'created by'),
        (r'\bwere created by\b', 'created by'),
        (r'\bhas been\b', 'is'),
        (r'\bhave been\b', 'are'),
        (r'\bwas developed\b', 'developed'),
        (r'\bwere developed\b', 'developed'),
        (r'\bis believed to\b', 'we believe'),
        (r'\bare believed to\b', 'we believe'),
        (r'\bis thought to\b', 'we think'),
        (r'\bare thought to\b', 'we think'),
        (r'\bis expected to\b', 'we expect'),
        (r'\bare expected to\b', 'we expect'),
        (r'\bis required to\b', 'must'),
        (r'\bare required to\b', 'must'),
        (r'\bis needed to\b', 'needs to'),
        (r'\bare needed to\b', 'need to'),
        (r'\bis recommended to\b', 'we recommend'),
        (r'\bare recommended to\b', 'we recommend'),
        (r'\bis suggested to\b', 'we suggest'),
        (r'\bare suggested to\b', 'we suggest'),
        (r'\bwas designed to\b', 'designed to'),
        (r'\bwere designed to\b', 'designed to'),
        (r'\bwas built to\b', 'built to'),
        (r'\bwere built to\b', 'built to'),
        (r'\bwas made to\b', 'made to'),
        (r'\bwere made to\b', 'made to'),
        (r'\bis driven by\b', 'comes from'),
        (r'\bare driven by\b', 'come from'),
        (r'\bis influenced by\b', 'influenced by'),
        (r'\bare influenced by\b', 'influenced by'),
        (r'\bis affected by\b', 'affected by'),
        (r'\bare affected by\b', 'affected by'),
    ]
    for pattern, replacement in passive:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # ============================================================
    # STEP 5: FIX DUPLICATE NUMBERING
    # ============================================================
    
    text = re.sub(r'(\d+)\.\s+\1\.', r'\1.', text)
    text = re.sub(r'(\d+)\.\s+(\d+)\.', r'\1. \2.', text)
        # ============================================================
    # STEP 6: REMOVE AI SENTENCE STARTERS
    # ============================================================
    
    ai_starters = [
        (r'One of the most significant trends', 'A major trend'),
        (r'Another trend is', 'Also'),
        (r'As the global population continues to grow', 'As more people join our planet'),
        (r'Over the past century', 'Over the last hundred years'),
        (r'it\'s expected to', 'it will likely'),
        (r'it\'s essential that', 'we need to'),
        (r'it\'s having a', 'it\'s causing a'),
        (r'this is particularly concerning', 'this is very worrying'),
        (r'this unpredictability is making', 'this uncertainty makes'),
        (r'These approaches can help', 'These methods can'),
        (r'What\'s worth noting is', ''),
        (r'Put yourself in this position', ''),
        (r'Think of it like this', ''),
        (r'What makes this interesting is', ''),
        (r'as far as I\'m concerned', ''),
        (r'it\'s not all doom and gloom', 'there\'s hope'),
    ]
    
    for pattern, replacement in ai_starters:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # ============================================================
    # STEP 6: CONVERT BULLET POINTS TO PARAGRAPHS
    # ============================================================
    
    def convert_bullets(match):
        bullet_text = match.group(0)
        bullet_text = re.sub(r'[•\-\*]\s*\*\*(.*?)\*\*:\s*', r'\1: ', bullet_text)
        bullet_text = re.sub(r'[•\-\*]\s*', '', bullet_text)
        items = [item.strip() for item in bullet_text.split('\n') if item.strip()]
        if len(items) > 1:
            if len(items) == 2:
                return f"{items[0]} and {items[1]}"
            else:
                return ", ".join(items[:-1]) + f", and {items[-1]}"
        return items[0] if items else ''
    
    text = re.sub(r'(?:^|\n)([•\-\*]\s*[^\n]+(?:\n[•\-\*]\s*[^\n]+)*)', 
                  lambda m: f'\n{convert_bullets(m)}', text, flags=re.DOTALL)

    # ============================================================
    # STEP 7: ADD PERSONAL VOICE (50+ patterns)
    # ============================================================
    
    personal_pronouns = [
        (r'\bone should\b', 'you should'),
        (r'\bone can\b', 'you can'),
        (r'\bpeople may\b', 'you might'),
        (r'\bit is essential to\b', 'you need to'),
        (r'\bthe reader\b', 'you'),
        (r'\bthe user\b', 'you'),
        (r'\bindividuals\b', 'people like you'),
        (r'\ba person\b', 'you'),
        (r'\bthey may\b', 'you might'),
        (r'\bstudents\b', 'students like you'),
        (r'\bprofessionals\b', 'professionals like you'),
        (r'\btravelers\b', 'travelers like you'),
        (r'\bone must\b', 'you must'),
        (r'\bone could\b', 'you could'),
        (r'\bone would\b', 'you would'),
        (r'\ba student\b', 'you as a student'),
        (r'\ba professional\b', 'you as a professional'),
        (r'\ba beginner\b', 'you as a beginner'),
        (r'\bthe average person\b', 'you'),
        (r'\bmost people\b', 'most of us'),
        (r'\bmany people\b', 'many of us'),
        (r'\bsome people\b', 'some of us'),
        (r'\bfew people\b', 'few of us'),
        (r'\bthe public\b', 'we'),
        (r'\bsociety\b', 'we'),
        (r'\bthe community\b', 'we'),
        (r'\bthe population\b', 'we'),
        (r'\bthe masses\b', 'we'),
        (r'\bthe majority\b', 'most of us'),
        (r'\bthe minority\b', 'some of us'),
        (r'\beveryone\b', 'all of us'),
        (r'\bnobody\b', 'none of us'),
        (r'\bsomeone\b', 'one of us'),
        (r'\banyone\b', 'any of us'),
        (r'\bpeople\b', 'we'),
        (r'\bhumans\b', 'we'),
        (r'\bhuman beings\b', 'we'),
        (r'\bthe human race\b', 'we'),
        (r'\bcivilization\b', 'we'),
        (r'\bthe world\b', 'we'),
        (r'\bthe planet\b', 'we'),
        (r'\bthe earth\b', 'we'),
    ]
    for pattern, replacement in personal_pronouns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # ============================================================
    # STEP 8: ADD RHETORICAL QUESTIONS (25+ patterns)
    # ============================================================
    
    rhetorical_questions = [
        " Have you ever wondered about that?",
        " Have you considered this before?",
        " Isn't that interesting?",
        " What do you think about this?",
        " Have you noticed this in your own experience?",
        " Does this sound familiar to you?",
        " Have you ever thought about it this way?",
        " Can you see how this applies to your own situation?",
        " Have you ever experienced this yourself?",
        " What would you do in this situation?",
        " Isn't it amazing how that works?",
        " Don't you agree that this makes sense?",
        " Have you ever stopped to think about this?",
        " What's your take on this?",
        " Can you relate to this?",
        " Have you ever been in this position?",
        " Doesn't that make you think?",
        " Have you ever asked yourself why?",
        " What if you looked at it differently?",
        " How would you feel if that happened to you?",
        " Have you ever wanted to try something new?",
        " What's holding you back from starting?",
        " Have you ever felt this way before?",
        " Do you see what I mean?",
        " Can you imagine the possibilities?",
        " What would you do if you were in their shoes?",
    ]
    
    paragraphs = text.split('\n\n')
    for idx, para in enumerate(paragraphs):
        if para.strip() and not para.strip().startswith('#'):
            if random.random() < 0.10:
                if para.endswith('.') or para.endswith('?') or para.endswith('!'):
                    paragraphs[idx] = para + random.choice(rhetorical_questions)
    text = '\n\n'.join(paragraphs)

    # ============================================================
    # STEP 9: ADD CONVERSATIONAL FILLERS (30+ patterns)
    # ============================================================
    
    fillers = [
        ("you know", "you know,"),
        ("I mean", "I mean,"),
        ("actually", "actually,"),
        ("honestly", "honestly,"),
        ("to be honest", "to be honest,"),
        ("in fact", "in fact,"),
        ("of course", "of course,"),
        ("after all", "after all,"),
        ("for instance", "for instance,"),
        ("like", "like,"),
        ("really", "really,"),
        ("basically", "basically,"),
        ("the thing is", "the thing is,"),
        ("believe it or not", "believe it or not,"),
        ("to be fair", "to be fair,"),
        ("at the end of the day", "at the end of the day,"),
        ("to tell you the truth", "to tell you the truth,"),
        ("if you ask me", "if you ask me,"),
        ("as far as I'm concerned", "as far as I'm concerned,"),
        ("in my opinion", "in my opinion,"),
        ("from my perspective", "from my perspective,"),
        ("let's be real", "let's be real,"),
        ("honestly speaking", "honestly speaking,"),
        ("the way I see it", "the way I see it,"),
        ("to be perfectly honest", "to be perfectly honest,"),
        ("frankly", "frankly,"),
        ("quite frankly", "quite frankly,"),
        ("if I'm being honest", "if I'm being honest,"),
        ("between you and me", "between you and me,"),
        ("just between us", "just between us,"),
    ]
    
    paragraphs = text.split('\n\n')
    for idx, para in enumerate(paragraphs):
        if para.strip() and not para.strip().startswith('#'):
            if random.random() < 0.15:
                sentences = para.split('. ')
                if len(sentences) > 2:
                    filler = random.choice(fillers)
                    target_idx = random.choice([1, 2]) if len(sentences) > 2 else 1
                    if target_idx < len(sentences):
                        sentences[target_idx] = f"{filler[1]} {sentences[target_idx]}"
                        paragraphs[idx] = '. '.join(sentences)
    text = '\n\n'.join(paragraphs)

    # ============================================================
    # STEP 10: ADD VARIED SENTENCE OPENERS (30+ patterns)
    # ============================================================
    
    openers = [
        "What's interesting is that",
        "The thing about this is",
        "What really matters is",
        "The key point is",
        "What we're seeing is",
        "It turns out that",
        "The reality is that",
        "The truth is",
        "What's fascinating is",
        "Here's what you need to know",
        "Let's be honest",
        "To put it simply",
        "The bottom line is",
        "What's important to remember is",
        "The main takeaway is",
        "What's worth noting is",
        "The surprising thing is",
        "What makes this interesting is",
        "The good news is",
        "The bad news is",
        "What's really going on is",
        "The secret to this is",
        "What most people don't realize is",
        "The overlooked aspect is",
        "What sets this apart is",
        "The way I look at it is",
        "From where I stand",
        "If you ask me",
        "The way I see it",
        "In my book",
        "As far as I can tell",
    ]
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for i in range(1, len(sentences)):
        if len(sentences[i].split()) > 5 and random.random() < 0.06:
            opener = random.choice(openers)
            sentences[i] = f"{opener}, {sentences[i][0].lower() + sentences[i][1:]}"
    text = '. '.join(sentences)

    # ============================================================
    # STEP 11: ADD NATURAL TRANSITIONS (30+ patterns)
    # ============================================================
    
    transitions = [
        (r'\bHowever,\b', "But"),
        (r'\bNevertheless,\b', "Still"),
        (r'\bTherefore,\b', "That means"),
        (r'\bThus,\b', "So"),
        (r'\bHence,\b', "That's why"),
        (r'\bNonetheless,\b', "Even so"),
        (r'\bSubsequently,\b', "After that"),
        (r'\bIn addition,\b', "Plus"),
        (r'\bIn contrast,\b', "On the flip side"),
        (r'\bConversely,\b', "On the other hand"),
        (r'\bMeanwhile,\b', "At the same time"),
        (r'\bFurthermore,\b', "And"),
        (r'\bMoreover,\b', "Plus"),
        (r'\bAdditionally,\b', "Also"),
        (r'\bConsequently,\b', "So"),
        (r'\bAccordingly,\b', "That's why"),
        (r'\bSubsequently,\b', "Next"),
        (r'\bUltimately,\b', "In the end"),
        (r'\bEventually,\b', "Over time"),
        (r'\bGradually,\b', "Slowly"),
        (r'\bInitially,\b', "At first"),
        (r'\bOriginally,\b', "In the beginning"),
        (r'\bPreviously,\b', "Earlier"),
        (r'\bSubsequently,\b', "Later"),
        (r'\bFinally,\b', "In the end"),
        (r'\bLastly,\b', "Finally"),
        (r'\bThen,\b', "Next"),
        (r'\bAfterward,\b', "After that"),
        (r'\bBeforehand,\b', "Before that"),
        (r'\bMeanwhile,\b', "In the meantime"),
        (r'\bPresently,\b', "Right now"),
    ]
    for pattern, replacement in transitions:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # ============================================================
    # STEP 12: ADD DIRECT ADDRESS TO READER (20+ patterns)
    # ============================================================
    
    direct_address = [
        "Imagine this: ",
        "Think about it this way: ",
        "Picture this: ",
        "Consider this for a moment: ",
        "Here's something to think about: ",
        "Just think about it: ",
        "Put yourself in this position: ",
        "Imagine for a second: ",
        "Let me ask you this: ",
        "Here's a thought: ",
        "Think of it like this: ",
        "Consider the following: ",
        "Take a moment to think: ",
        "Here's what I mean: ",
        "Let me put it this way: ",
        "Now, think about this: ",
        "Just imagine for a moment: ",
        "What if I told you: ",
        "Here's the deal: ",
        "This is the thing: ",
    ]
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for i in range(2, len(sentences)):
        if len(sentences[i].split()) > 10 and random.random() < 0.05:
            sentences[i] = random.choice(direct_address) + sentences[i]
    text = '. '.join(sentences)

    # ============================================================
    # STEP 13: PARAGRAPH-AWARE STRUCTURAL PROCESSING
    # ============================================================
    
    paragraphs = text.split('\n\n')
    processed_paragraphs = []

    conjunction_starters = ["And", "But", "So", "Yet", "Then", "Now"]

    for para in paragraphs:
        if not para.strip() or para.strip().startswith('#'):
            processed_paragraphs.append(para.strip())
            continue

        sentences = re.split(r'(?<=[.!?])\s+', para.strip())
        new_sentences = []

        for i, sentence in enumerate(sentences):
            words = sentence.split()
            if not words:
                continue

            if i > 0 and len(words) > 8 and random.random() < 0.10:
                starter = random.choice(conjunction_starters)
                first_word = words[0]
                if first_word != 'I' and not first_word[0].isupper():
                    words[0] = first_word[0].lower() + first_word[1:]
                sentence = f"{starter} " + " ".join(words)

            new_sentences.append(sentence)

        processed_paragraphs.append(" ".join(new_sentences))

    text = '\n\n'.join(processed_paragraphs)

    # ============================================================
    # STEP 14: FINAL CLEANUP
    # ============================================================
    
    # Fix heading spacing
    text = re.sub(r'(?<!\n)#([A-Za-z])', r'# \1', text)
    
    # Fix double headings
    text = re.sub(r'(# .+?) (#.+?)', r'\1\n\n\2', text)
    
    # Clean spaces
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Fix punctuation
    text = re.sub(r'\s([?.!,";:])', r'\1', text)
    
    # Remove duplicate newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove any remaining AI signatures
    text = re.sub(r'\*Generated using.*?technology\*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'---\s*\*Generated using.*?technology\*', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove empty bullet points
    text = re.sub(r'• \*\*.*?\*\*:.*?\n', '', text)
    
    # Fix any remaining "1. 1." patterns
    text = re.sub(r'(\d+)\.\s+\1\.', r'\1.', text)
        # ============================================================
    # STEP 15: EXTRA CLEANUP FOR COMMON ISSUES
    # ============================================================
    
    # Fix duplicate numbering (1. 1. → 1.)
    text = re.sub(r'(\d+)\.\s+\1\.', r'\1.', text)
    
    # Fix "1. 2." patterns (keep both numbers)
    text = re.sub(r'(\d+)\.\s+(\d+)\.', r'\1. \2.', text)
    
    # Remove any remaining "1. 1." patterns
    text = re.sub(r'(\d+)\.\s+\1\.', r'\1.', text)
    
    # Fix "a important" → "an important"
    text = re.sub(r'\ba important\b', 'an important', text)
    
    # Fix "an important role in understanding" - remove completely if appears
    text = re.sub(r'an important role in understanding .*?\.', '', text, flags=re.IGNORECASE)
    
    # Remove any remaining "plays a" patterns
    text = re.sub(r'plays a (important|crucial|vital) role in understanding .*?\.', '', text, flags=re.IGNORECASE)
    
    # Remove "there are several important factors" patterns
    text = re.sub(r'there are several important factors to consider when exploring this area\.', '', text, flags=re.IGNORECASE)
    
    # Remove "experts agree that" patterns
    text = re.sub(r'experts agree that .*? is fundamental to grasping the broader context of .*?\.', '', text, flags=re.IGNORECASE)
    
    # Clean up extra spaces after removals
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()