import re
import json
import logging
from omegaconf import DictConfig
from .base_agent import BaseAgent
from pydantic import BaseModel  


class DomainOutput(BaseModel):
    domains: list[str]
    domain_analysis: list[dict]
    suspicious_characteristics: list[str]
    blacklisted_count: int
    spam_likelihood: float
    reasoning: str

class DomainAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.weight = cfg["agents"]["domain"]["weight"]
        self.threshold = cfg["agents"]["domain"]["threshold"]
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Domain agent initialized with weight: {self.weight}, threshold: {self.threshold}")
    
    def extract_domains(self, urls):
        domains = []
        for url in urls:

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
            result = self.query_llm(system_prompt, user_prompt, schema=DomainOutput)
            return result  # Return the validated output directly
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return DomainOutput(
                domains=domains,
                domain_analysis=[],
                suspicious_characteristics=[],
                blacklisted_count=0,
                spam_likelihood=0,
                reasoning="Failed to parse LLM response"
            ) 