import re
import json
import logging
from omegaconf import DictConfig
from .base_agent import BaseAgent

class URLAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.weight = cfg.agents.url.weight
        self.threshold = cfg.agents.url.threshold
        self.url_pattern = cfg.agents.url.url_pattern
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"URL agent initialized with weight: {self.weight}, threshold: {self.threshold}")
    
    def analyze(self, text):
        self.logger.info("Analyzing text for URLs and phishing indicators")
        
        url_pattern = self.url_pattern
        urls = re.findall(url_pattern, text)
        
        if not urls:
            self.logger.info("No URLs found in the text")
            return {
                "urls": [],
                "phishing_likelihood": 0,
                "malicious_url_count": 0,
                "spam_likelihood": 0,
                "reasoning": "No URLs found in the text"
            }
        
        self.logger.info(f"Found {len(urls)} URLs in the text: {urls}")
        
        system_prompt = self.prompts.URL_SYSTEM
        user_prompt = self.prompts.URL_USER.format(urls=', '.join(urls))
        
        try:
            result = self.query_llm(system_prompt, user_prompt)
            url_analysis = result.get("url_analysis", [])
            malicious_count = sum(1 for url in url_analysis if url.get("phishing_score", 0) > 0.5)
            
            spam_likelihood = result.get("spam_likelihood", 0)            
            return {
                "urls": urls,
                "url_analysis": url_analysis,
                "suspicious_characteristics": result.get("suspicious_characteristics", []),
                "phishing_likelihood": result.get("phishing_likelihood", 0),
                "malicious_url_count": malicious_count,
                "spam_likelihood": spam_likelihood,
                "reasoning": result.get("reasoning", "No reasoning provided")
            }
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return {
                "urls": urls,
                "url_analysis": [],
                "suspicious_characteristics": [],
                "phishing_likelihood": 0,
                "malicious_url_count": 0,
                "spam_likelihood": 0,
                "reasoning": "Failed to parse LLM response"
            } 