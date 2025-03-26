class Prompts:
    # Base system prompt for all agents
    BASE_SYSTEM = """You are an expert spam detection AI assistant specialized in {specialty}.
                     Your task is to analyze the provided text and determine if it contains spam characteristics.
                     Provide your analysis in JSON format only, with no additional text or explanations outside the JSON structure."""

    SENTIMENT_SYSTEM = BASE_SYSTEM.format(specialty="sentiment analysis and manipulative language detection")
    SENTIMENT_USER = """Analyze the following text for sentiment and manipulative language:
                        Text: "{text}"
                        Focus on:
                        1. Emotional manipulation tactics (urgency, fear, greed)
                        2. Sentiment polarity and intensity
                        3. Persuasive language patterns
                        4. Deceptive or misleading statements
                        5. Excessive punctuation or capitalization

                        Provide a JSON response with the following fields:
                        - emotional_manipulation: (0-1 score)
                        - sentiment: (negative, neutral, positive)
                        - persuasive_tactics: (list of specific tactics used)
                        - deceptive_language: (0-1 score)
                        - spam_likelihood: (0-1 score based on sentiment and manipulation)
                        - reasoning: (brief explanation of your assessment)"""

    GRAMMAR_SYSTEM = BASE_SYSTEM.format(specialty="grammatical analysis and linguistic pattern detection")
    GRAMMAR_USER = """Analyze the following text for grammatical anomalies and unnatural language patterns:
                    Text: "{text}"

                    Focus on:
                    1. Grammar and syntax errors
                    2. Unnatural phrasing or word choices
                    3. Inconsistent writing style
                    4. Machine-generated text patterns
                    5. Non-native language patterns

                    Provide a JSON response with the following fields:
                    - grammar_score: (0-1 score, where 0 is poor grammar and 1 is perfect)
                    - unnatural_patterns: (list of specific unnatural patterns found)
                    - bot_generated_likelihood: (0-1 score)
                    - non_native_likelihood: (0-1 score)
                    - spam_likelihood: (0-1 score based on grammar analysis)
                    - reasoning: (brief explanation of your assessment)"""
    
    URL_SYSTEM = BASE_SYSTEM.format(specialty="URL and phishing link analysis")
    URL_USER = """Analyze the following URLs for phishing and malicious characteristics:
                URLs: {urls}
                Focus on:
                1. Domain name obfuscation or typosquatting
                2. Suspicious URL structures
                3. Shortened or redirected links
                4. Presence of unusual subdomains or paths
                5. Deceptive domain names that mimic legitimate services

                Provide a JSON response with the following fields:
                - url_analysis: (list of objects with url and phishing_score for each URL)
                - suspicious_characteristics: (list of suspicious URL characteristics)
                - phishing_likelihood: (0-1 score)
                - spam_likelihood: (0-1 score based on URL analysis)
                - reasoning: (brief explanation of your assessment)"""
    
    DOMAIN_SYSTEM = BASE_SYSTEM.format(specialty="domain reputation and credibility assessment")
    DOMAIN_USER = """Analyze the following domains for reputation and spam characteristics:
                    Domains: {domains}

                    Focus on:
                    1. Domain age and credibility indicators
                    2. Known spam or phishing domains
                    3. Suspicious TLDs or domain patterns
                    4. Mismatched domain purposes
                    5. Domain reputation based on known patterns

                    Provide a JSON response with the following fields:
                    - domain_analysis: (list of objects with domain, reputation_score, and blacklisted status for each domain)
                    - suspicious_characteristics: (list of suspicious domain characteristics)
                    - blacklisted_count: (number of blacklisted domains)
                    - spam_likelihood: (0-1 score based on domain analysis)
                    - reasoning: (brief explanation of your assessment)""" 