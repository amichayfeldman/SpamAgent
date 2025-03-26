import re
import json
import logging
from omegaconf import DictConfig
from .base_agent import BaseAgent

class DomainAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.weight = cfg.agents.domain.weight
        self.threshold = cfg.agents.domain.threshold
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Domain agent initialized with weight: {self.weight}, threshold: {self.threshold}")
    
    def extract_domains(self, urls):
        domains = []
        for url in urls:
            # Extract domain from URL
            domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            if domain_match:
                domains.append(domain_match.group(1))
        return list(set(domains))
    
    def analyze(self, urls):
        self.logger.info(f"Analyzing domains from {len(urls)} URLs")
        
        domains = self.extract_domains(urls)
        
        if not domains:
            self.logger.info("No domains to analyze")
            return {
                "domains": [],
                "reputation_scores": [],
                "blacklisted_count": 0,
                "spam_likelihood": 0,
                "reasoning": "No domains to analyze"
            }
        
        self.logger.info(f"Extracted {len(domains)} domains: {domains}")
        
        system_prompt = self.prompts.DOMAIN_SYSTEM
        user_prompt = self.prompts.DOMAIN_USER.format(domains=', '.join(domains))
    
        try:
            result = self.query_llm(system_prompt, user_prompt)
            domain_analysis = result.get("domain_analysis", [])
            blacklisted_count = sum(1 for domain in domain_analysis if domain.get("blacklisted", False))
            spam_likelihood = result.get("spam_likelihood", 0)
            
            return {
                "domains": domains,
                "domain_analysis": domain_analysis,
                "suspicious_characteristics": result.get("suspicious_characteristics", []),
                "blacklisted_count": blacklisted_count,
                "spam_likelihood": spam_likelihood,
                "reasoning": result.get("reasoning", "No reasoning provided")
            }
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return {
                "domains": domains,
                "domain_analysis": [],
                "suspicious_characteristics": [],
                "blacklisted_count": 0,
                "spam_likelihood": 0,
                "reasoning": "Failed to parse LLM response"
            } 