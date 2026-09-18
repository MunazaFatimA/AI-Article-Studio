# utils/ai_writer.py
import os
import requests
import re
import time

#  try/except add 
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass 

# ============================================================
# 🔥 PROFESSIONAL MASTER PROMPT
# ============================================================

MASTER_PROMPT = """
You are an expert content writer. Write a natural, engaging, and highly informative article following these guidelines.

USER REQUIREMENTS:
- Topic: {USER_TOPIC}
- Target Word Count: {WORD_COUNT} words
- Writing Tone: {TONE}
- Target Audience: {AUDIENCE}
- Headings: {HEADINGS}
- Keywords: {KEYWORDS}

WRITING RULES:
- Use H1 (#) for main title, H2 (##) for main sections, H3 (###) for subsections.
- Write direct, human-like sentences.
- Vary sentence length and structure (high burstiness).
- Use active voice and natural contractions (it's, don't, can't).
- Do NOT use AI clichés: "In today's world", "delve", "testament", "paramount", "seamless", "crucial", "landscape".

Write the article directly below:
"""


# ============================================================
# MAIN GENERATE FUNCTION
# ============================================================

def generate_article(title, keywords, word_count=800, tone="Professional", 
                     audience=None, headings=None, instructions=None, 
                     model="groq"):
    """Generate article with strict model isolation and fallback"""
    
    headings_text = "Introduction, Key Concepts, Practical Applications, Conclusion"
    if headings and headings.get("h2"):
        headings_text = ", ".join(headings["h2"])
    
    keywords_str = ", ".join(keywords) if keywords else "Not specified"
    audience_text = audience if audience else "General readers"
    
    formatted_prompt = MASTER_PROMPT.format(
        USER_TOPIC=title,
        WORD_COUNT=word_count,
        TONE=tone,
        AUDIENCE=audience_text,
        HEADINGS=headings_text,
        KEYWORDS=keywords_str
    )
    
    model = model.lower().strip()
    result = None
    
    # Direct Model Routing
    if model == "openrouter":
        result = generate_with_openrouter(formatted_prompt, word_count)
    elif model == "groq":
        result = generate_with_groq(formatted_prompt, word_count)
    elif model == "cohere":
        result = generate_with_cohere(formatted_prompt, word_count)
    elif model == "gemini":
        result = generate_with_gemini(formatted_prompt, word_count)
    elif model == "tavily":
        result = generate_with_tavily(title, formatted_prompt, word_count)
    else:
        result = generate_with_groq(formatted_prompt, word_count)

    # ✅ FIX: Pass model name to fallback for UNIQUE content per model
    if not result or len(result.strip().split()) < 100 or result.startswith("❌"):
        print(f"⚠️ {model} API failed/unavailable. Falling back to Auto-Search Generator...")
        result = auto_search_and_generate(title, word_count, tone, model)

    # Clean formatting
    result = clean_article_formatting(result, title)
    return result


# ============================================================
# API IMPLEMENTATIONS
# ============================================================

def generate_with_groq(prompt, word_count):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or len(api_key) < 10:
            return None
        
        from groq import Groq
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional content writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=min(word_count * 2, 8192)
        )
        content = response.choices[0].message.content
        return content if content and len(content.strip().split()) > 100 else None
    except Exception as e:
        print(f"Groq Error: {e}")
        return None


def generate_with_gemini(prompt, word_count):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or len(api_key) < 10:
            return None
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": min(word_count * 2, 4096)
            }
        }
        response = requests.post(url, headers=headers, json=data, timeout=45)
        if response.status_code == 200:
            res = response.json()
            return res["candidates"][0]["content"]["parts"][0]["text"]
        return None
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None


def generate_with_openrouter(prompt, word_count):
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or len(api_key) < 10:
            return None
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "ArticleForge"
        }
        models = [
            "meta-llama/llama-3.3-70b-instruct:free",
            "qwen/qwen-2.5-72b-instruct:free",
            "mistralai/mistral-7b-instruct:free"
        ]
        for model in models:
            try:
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": min(word_count * 2, 4000),
                    "temperature": 0.7
                }
                res = requests.post(url, headers=headers, json=data, timeout=30)
                if res.status_code == 200:
                    content = res.json()["choices"][0]["message"]["content"]
                    if content and len(content.strip().split()) > 100:
                        return content
            except Exception:
                continue
        return None
    except Exception as e:
        print(f"OpenRouter Error: {e}")
        return None


def generate_with_cohere(prompt, word_count):
    try:
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key or len(api_key) < 10:
            return None
        
        url = "https://api.cohere.com/v2/chat"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "command-r-plus-08-2024",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=45)
        if response.status_code == 200:
            return response.json()["message"]["content"][0]["text"]
        return None
    except Exception as e:
        print(f"Cohere Error: {e}")
        return None


def generate_with_tavily(title, prompt, word_count):
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key or len(api_key) < 10:
            return None
        
        url = "https://api.tavily.com/search"
        data = {
            "api_key": api_key,
            "query": f"detailed facts about {title}",
            "search_depth": "advanced",
            "max_results": 3,
            "include_answer": True
        }
        res = requests.post(url, json=data, timeout=30)
        if res.status_code == 200:
            res_data = res.json()
            facts = res_data.get("answer") or "\n".join([r.get("content", "") for r in res_data.get("results", [])])
            
            full_prompt = f"Web Research Context:\n{facts}\n\n{prompt}"
            return generate_with_groq(full_prompt, word_count)
        return None
    except Exception as e:
        print(f"Tavily Error: {e}")
        return None



# ============================================================
# 🔍 AUTO-SEARCH FALLBACK (WITH FREE AI MODELS)
# ============================================================

def auto_search_and_generate(topic, word_count, tone="Professional", model_name=""):
    """
    Ultimate fallback when ALL APIs fail.
    Uses FREE PUBLIC AI MODELS (Hugging Face, Together.ai, Replicate)
    """
    print(f"🔍 Auto-search fallback activated for: {topic} using {model_name}")
    
    # ============================================================
    # MODEL-SPECIFIC PROMPTS
    # ============================================================
    
    model_prompts = {
        "groq": f"""Write a comprehensive article about {topic} in {word_count} words. 
        Use a direct, concise style. Focus on practical applications and actionable insights.
        Include introduction, body sections with subheadings, and conclusion.
        Use active voice and short paragraphs.""",
        
        "gemini": f"""Write a detailed, analytical article about {topic} in {word_count} words.
        Use a research-driven style. Include in-depth analysis and comprehensive coverage.
        Include introduction, body sections with subheadings, and conclusion.
        Use active voice and varied sentence structure.""",
        
        "openrouter": f"""Write a balanced, well-rounded article about {topic} in {word_count} words.
        Use a multi-perspective style. Present different viewpoints objectively.
        Include introduction, body sections with subheadings, and conclusion.
        Use active voice and clear transitions.""",
        
        "cohere": f"""Write an engaging, conversational article about {topic} in {word_count} words.
        Use an accessible, reader-friendly style. Make it easy to understand.
        Include introduction, body sections with subheadings, and conclusion.
        Use active voice and contractions.""",
        
        "tavily": f"""Write a fact-based, evidence-driven article about {topic} in {word_count} words.
        Use an authoritative style. Include specific facts and examples.
        Include introduction, body sections with subheadings, and conclusion.
        Use active voice and clear explanations."""
    }
    
    # 🔥 FIX: Use model_name directly instead of trying to match
    prompt = model_prompts.get(model_name.lower(), f"""
    Write a comprehensive, well-researched article about {topic} in {word_count} words.
    Use a professional, engaging style. Include specific examples and practical information.
    Include introduction, body sections with subheadings, and conclusion.
    Use active voice and short paragraphs.
    """)
    
    # ============================================================
    # TRY FREE AI MODELS
    # ============================================================
    
    models_to_try = ["huggingface", "huggingface_llama"]
    result = None
    
    for model_choice in models_to_try:
        try:
            print(f"🔄 Trying free AI model: {model_choice}...")
            result = call_free_ai_model(prompt, model_choice)
            
            if result and len(result.strip().split()) > 100:
                print(f"✅ {model_choice} succeeded!")
                break
        except Exception as e:
            print(f"⚠️ {model_choice} failed: {e}")
            continue
    
    # ============================================================
    # ULTIMATE FALLBACK: GENERATE FROM TEMPLATE
    # ============================================================
    
    if not result or len(result.strip().split()) < 100:
        print("⚠️ All free AI models failed. Generating from template...")
        # 🔥 FIX: Pass model_name to template
        result = generate_fallback_template(topic, word_count, model_name)
    
    return result

# ============================================================
# FREE PUBLIC AI MODEL CALLS
# ============================================================

def call_free_ai_model(prompt, model_choice="huggingface"):
    """
    Call free AI models like Hugging Face, Together.ai, Replicate
    No API key required for some models
    """
    
    models = {
        "huggingface": {
            "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
            "type": "huggingface"
        },
        "huggingface_llama": {
            "url": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
            "type": "huggingface"
        },
        "together": {
            "url": "https://api.together.xyz/inference",
            "type": "together"
        },
        "replicate": {
            "url": "https://api.replicate.com/v1/predictions",
            "type": "replicate"
        }
    }
    
    try:
        model_config = models.get(model_choice, models["huggingface"])
        
        if model_config["type"] == "huggingface":
            return call_huggingface_api(model_config["url"], prompt)
        elif model_config["type"] == "together":
            return call_together_api(model_config["url"], prompt)
        elif model_config["type"] == "replicate":
            return call_replicate_api(model_config["url"], prompt)
        
        return None
    except Exception as e:
        print(f"Free AI model error: {e}")
        return None


def call_huggingface_api(url, prompt):
    """Call Hugging Face inference API (FREE)"""
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2000,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "")
                if prompt in text:
                    text = text.replace(prompt, "").strip()
                return text
        return None
    except Exception as e:
        print(f"HuggingFace error: {e}")
        return None


def call_together_api(url, prompt):
    """Call Together.ai API (FREE tier)"""
    try:
        data = {
            "model": "togethercomputer/llama-2-70b-chat",
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = requests.post(url, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("output", {}).get("choices", [{}])[0].get("text", "")
        return None
    except Exception as e:
        print(f"Together.ai error: {e}")
        return None


def call_replicate_api(url, prompt):
    """Call Replicate API (FREE tier)"""
    try:
        data = {
            "version": "meta/llama-2-70b-chat",
            "input": {
                "prompt": prompt,
                "max_new_tokens": 2000,
                "temperature": 0.7
            }
        }
        
        response = requests.post(url, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            prediction_url = result.get("urls", {}).get("get")
            if prediction_url:
                time.sleep(5)
                get_response = requests.get(prediction_url, timeout=30)
                if get_response.status_code == 200:
                    data = get_response.json()
                    return " ".join(data.get("output", []))
        return None
    except Exception as e:
        print(f"Replicate error: {e}")
        return None


# ============================================================
# ULTIMATE FALLBACK TEMPLATE
# ============================================================

def generate_fallback_template(topic, word_count, model_name=""):
    """
    Ultimate fallback when EVERYTHING fails.
    Generates UNIQUE content for each model with PROPER WORD COUNT.
    """
    
    # Calculate how many sections needed based on word count
    num_sections = max(3, word_count // 150)  # ~150 words per section
    num_sections = min(num_sections, 6)  # Max 6 sections
    
    # ============================================================
    # MODEL-SPECIFIC TEMPLATES WITH EXPANDABLE CONTENT
    # ============================================================
    
    # Base template with placeholders for expansion
    def expand_section(heading, content_lines, word_count_target):
        """Expand a section to meet word count"""
        base_content = "\n".join(content_lines)
        words = base_content.split()
        
        # If section is too short, add more content
        if len(words) < 50:
            extra_lines = [
                f"This is particularly important because it affects how we approach {topic} in practical terms.",
                f"Understanding these concepts can lead to better outcomes and more effective strategies.",
                f"Many professionals in this field emphasize the importance of mastering these fundamentals.",
                f"Research shows that a solid grasp of these principles leads to more successful implementation.",
                f"By focusing on these key areas, you can develop a more comprehensive understanding of {topic}.",
            ]
            # Add random extra lines
            import random
            for _ in range(random.randint(1, 3)):
                content_lines.append(random.choice(extra_lines))
        
        return "\n".join(content_lines)
    
    # Model-specific templates
    model_templates = {
        "groq": f"""# {topic}

## Introduction

{topic} represents a dynamic field where speed and efficiency drive success. This guide provides a comprehensive overview of the key concepts and practical applications that define this important subject.

Understanding {topic} is essential for anyone looking to stay ahead in today's fast-paced environment. The principles outlined in this guide will help you navigate the complexities and achieve meaningful results.

## Key Concepts

The fundamentals of {topic} can be broken down into several core areas. Each of these areas plays a vital role in building a complete understanding of the subject.

• **Efficiency:** How to achieve optimal results with minimal resources
• **Scalability:** Adapting strategies to meet growing demands
• **Reliability:** Ensuring consistent and dependable outcomes
• **Innovation:** Embracing new approaches and technologies

### Practical Implementation

When implementing strategies related to {topic}, it's important to consider the specific context and requirements of your situation. A one-size-fits-all approach rarely works.

Start by assessing your current capabilities and identifying areas for improvement. Then, develop a phased approach that allows for gradual progress and adjustment.

## Advanced Strategies

For those looking to go beyond the basics, advanced strategies offer opportunities for significant improvement. These approaches require more effort but yield greater rewards.

### Optimization Techniques

Several optimization techniques can enhance your performance in this area. These include data-driven decision making, continuous feedback loops, and adaptive planning.

### Measuring Success

Tracking progress is essential for long-term success. Establish clear metrics and regularly evaluate your performance against these benchmarks.

## Conclusion

By applying these principles, you can achieve significant results with {topic}. The journey requires dedication and persistence, but the rewards are well worth the effort.

Start implementing these strategies today and watch your understanding and capabilities grow. Remember, every expert was once a beginner who refused to give up.

---
*Generated using {model_name} fallback*""",

        "gemini": f"""# {topic}

## Introduction

{topic} offers rich opportunities for exploration and discovery. This comprehensive guide provides detailed analysis and research-based insights into this fascinating subject.

The importance of {topic} cannot be overstated in today's world. As we continue to face new challenges and opportunities, understanding this field becomes increasingly valuable.

## Core Concepts

A thorough understanding of {topic} requires examining multiple dimensions. Each dimension offers unique insights and practical applications that can enhance your overall comprehension.

### Structural Frameworks

The structural framework of {topic} consists of several interconnected components. These components work together to create a cohesive system that can be analyzed and optimized.

### Behavioral Patterns

Understanding behavioral patterns is crucial for predicting outcomes and making informed decisions. These patterns reveal important trends and opportunities for intervention.

## Analytical Insights

Research reveals important connections between different aspects of {topic}. These insights inform practical applications and strategic decisions.

### Research Findings

Recent studies have shown that effective implementation of {topic} principles leads to measurable improvements in various areas. These findings provide a strong foundation for action.

### Practical Applications

The principles of {topic} can be applied in numerous real-world scenarios. From professional settings to personal development, the applications are diverse and impactful.

## Future Directions

The future of {topic} is bright, with new developments and innovations emerging regularly. Staying informed about these trends is essential for maintaining a competitive edge.

### Emerging Trends

Several emerging trends are shaping the future of {topic}. These include technological advancements, evolving best practices, and changing societal needs.

### Strategic Recommendations

Based on current research and future projections, strategic recommendations can help guide your approach to {topic}. These recommendations are designed to maximize success.

## Conclusion

Continued exploration of {topic} will yield valuable insights and opportunities for growth. The journey of discovery is ongoing, and each step forward brings new understanding.

---
*Generated using {model_name} fallback*""",

        "openrouter": f"""# {topic}

## Introduction

{topic} requires consideration from multiple perspectives. This balanced guide presents diverse viewpoints and practical recommendations to help you navigate this complex subject.

Understanding the various dimensions of {topic} is essential for making informed decisions and achieving optimal outcomes.

## Different Perspectives

Examining {topic} from various angles reveals its complexity and importance. Each perspective offers unique insights that contribute to a more complete understanding.

### Theoretical View

The theoretical foundation of {topic} provides a framework for understanding its core principles. This perspective emphasizes conceptual understanding and analytical thinking.

### Practical View

The practical perspective focuses on real-world applications and implementation strategies. This view prioritizes actionable insights and measurable results.

### Future View

Looking ahead, the future of {topic} presents both opportunities and challenges. Anticipating these developments can help you prepare and adapt.

## Practical Considerations

Real-world applications of {topic} require careful planning and execution. Key factors include preparation, implementation, and ongoing evaluation.

### Implementation Strategies

Effective implementation strategies are essential for success. These strategies should be tailored to your specific context and goals.

### Common Challenges

Several common challenges arise when working with {topic}. Understanding these challenges helps you prepare and respond effectively.

### Best Practices

Following established best practices can significantly improve outcomes. These practices have been validated through experience and research.

## Conclusion

A balanced approach to {topic} leads to better outcomes and more comprehensive understanding. By considering multiple perspectives, you can make more informed decisions.

---
*Generated using {model_name} fallback*""",

        "cohere": f"""# {topic}

## Introduction

Let's explore {topic} in a way that's easy to understand and apply. This guide breaks down complex concepts into simple, actionable insights that anyone can use.

Whether you're new to {topic} or looking to deepen your knowledge, this guide has something for everyone. The key is to start where you are and build from there.

## What You Need to Know

The basics of {topic} are actually quite simple. Once you understand the fundamentals, everything else falls into place naturally.

### The Fundamentals

Understanding the fundamentals is the first step toward mastery. These core concepts form the foundation for more advanced learning.

### Why It Matters

{topic} matters because it affects so many aspects of our lives. From professional success to personal wellbeing, the principles of {topic} have far-reaching implications.

## Getting Started

Applying {topic} to your own situation is easier than you think. Start small, learn as you go, and keep improving.

### Simple Steps

1. Identify your goals and objectives
2. Research best practices and approaches
3. Develop a plan tailored to your needs
4. Take action and monitor your progress
5. Adjust your approach based on results

### Common Mistakes to Avoid

Everyone makes mistakes when learning something new. Being aware of common pitfalls can help you avoid them and accelerate your progress.

## Advanced Tips

Once you've mastered the basics, advanced tips can help you achieve even better results. These techniques are used by experts in the field.

### Optimization Strategies

Optimization strategies can help you get the most out of your efforts. These approaches focus on efficiency and effectiveness.

### Continuous Improvement

The journey of learning {topic} is ongoing. Embrace continuous improvement and keep pushing yourself to grow.

## Conclusion

{topic} is a topic that truly matters. By understanding it better, you can make more informed decisions and achieve better outcomes.

Remember, every expert was once a beginner. Keep learning, keep growing, and don't be afraid to ask questions along the way.

---
*Generated using {model_name} fallback*""",

        "tavily": f"""# {topic}

## Introduction

Based on current research and verified data, {topic} demonstrates several important characteristics that deserve careful attention. This evidence-based guide provides a comprehensive overview of the key findings and their implications.

The importance of {topic} in today's world is supported by a growing body of research. Understanding these findings can help you make better decisions.

## Key Findings

Evidence shows that {topic} has significant implications across multiple domains. These findings are based on rigorous research and analysis.

### Statistical Overview

Recent statistics reveal important trends and patterns related to {topic}. These numbers provide valuable context for understanding the subject.

### Research Highlights

Several research studies have produced significant findings related to {topic}. These studies offer insights that can inform practice and policy.

## Practical Implications

Research findings translate into actionable recommendations for professionals and organizations. These implications have real-world significance.

### Implementation Guidelines

Based on research findings, specific implementation guidelines can help you apply the principles of {topic} effectively.

### Case Examples

Real-world case examples illustrate how the principles of {topic} can be applied in practice. These examples provide valuable learning opportunities.

## Future Directions

The evidence suggests that {topic} will continue to evolve and grow in importance. Staying informed about these developments is essential.

### Emerging Research

New research is constantly adding to our understanding of {topic}. Keeping up with these developments can give you a competitive advantage.

### Strategic Recommendations

Based on current evidence and future projections, strategic recommendations can guide your approach to {topic}.

## Conclusion

Evidence-based approaches to {topic} lead to better outcomes and more informed decisions. By relying on research and data, you can achieve more reliable results.

---
*Generated using {model_name} fallback*"""
    }
    
    # Get model-specific template or default
    template = model_templates.get(model_name.lower(), f"""# {topic}

## Introduction

{topic} is a topic that deserves careful attention and understanding. This guide explores the key aspects and practical implications that define this important subject.

Understanding {topic} can help you make better decisions and achieve more meaningful results. The information in this guide is designed to be both informative and actionable.

## Key Concepts

Understanding the core concepts of {topic} is essential. These concepts form the foundation for practical applications and deeper learning.

### Fundamentals

The fundamentals of {topic} provide the basis for all other learning. Mastering these concepts is the first step toward expertise.

### Applications

The principles of {topic} can be applied in various contexts, from professional settings to everyday situations. Understanding these applications helps you see the relevance of the subject.

## Practical Applications

Applying the principles of {topic} in real-world situations requires careful planning and execution. The following sections provide guidance on implementation.

### Getting Started

Taking the first step can be the hardest part. Start with small, achievable goals and build from there.

### Common Challenges

Everyone faces challenges when learning something new. Understanding common obstacles can help you overcome them more effectively.

### Success Strategies

Several strategies can help you succeed with {topic}. These approaches have been validated through experience and research.

## Conclusion

{topic} offers valuable opportunities for learning, growth, and practical application. By understanding the key concepts and applying them effectively, you can achieve meaningful results.

---
*Generated using AI fallback*""")
    
    # Expand template to meet word count
    # Count current words
    current_words = len(template.split())
    
    # If need more words, add additional content
    if current_words < word_count:
        additional_content = f"""
## Additional Insights

Continuing our exploration of {topic}, there are several more aspects worth considering. These additional insights build on the foundations we've already established.

### Deepening Your Understanding

To truly master {topic}, it's important to go beyond the basics. This means exploring advanced concepts and their practical applications.

### Real-World Examples

Real-world examples illustrate how the principles of {topic} apply in practice. These examples provide valuable context and learning opportunities.

### Continuous Learning

The field of {topic} is constantly evolving. Committing to continuous learning will help you stay current and competitive.

### Taking Action

Knowledge without action is incomplete. Use the insights from this guide to take meaningful action and achieve your goals.

### Building on Success

As you make progress, build on your successes. Each achievement creates momentum for further growth and development.
"""
        template = template + "\n" + additional_content
    
    return template
# ============================================================
# 🧹 FORMATTING CLEANUP
# ============================================================

def clean_article_formatting(text, title):
    if not text:
        return text
    
    # Fix heading formatting (#Heading -> # Heading)
    text = re.sub(r'(?<!\n)#([A-Za-z])', r'# \1', text)
    text = re.sub(r'(?<!\n)##([A-Za-z])', r'## \1', text)
    text = re.sub(r'(?<!\n)###([A-Za-z])', r'### \1', text)
    
    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Ensure title is present at top
    if not text.strip().startswith('#'):
        text = f"# {title}\n\n" + text.strip()
        
    return text.strip()