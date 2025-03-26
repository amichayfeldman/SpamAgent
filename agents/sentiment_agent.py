from .base_agent import BaseAgent
import json
import logging
from omegaconf import DictConfig

class SentimentAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.weight = cfg.agents.sentiment.weight
        self.threshold = cfg.agents.sentiment.threshold
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Sentiment agent initialized with weight: {self.weight}, threshold: {self.threshold}")
    
    def analyze(self, text):
        self.logger.info("Analyzing text for sentiment and manipulative language")
        
        system_prompt = self.prompts.SENTIMENT_SYSTEM
        user_prompt = self.prompts.SENTIMENT_USER.format(text=text)
        try:
            result = self.query_llm(system_prompt, user_prompt)
            spam_likelihood = result.get("spam_likelihood", 0)
            return {
                "emotional_manipulation": result.get("emotional_manipulation", 0),
                "sentiment": result.get("sentiment", "neutral"),
                "persuasive_tactics": result.get("persuasive_tactics", []),
                "deceptive_language": result.get("deceptive_language", 0),
                "spam_likelihood": spam_likelihood,
                "reasoning": result.get("reasoning", "No reasoning provided")
            }
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return {
                "emotional_manipulation": 0,
                "sentiment": "neutral",
                "persuasive_tactics": [],
                "deceptive_language": 0,
                "spam_likelihood": 0,
                "reasoning": "Failed to parse LLM response"
            } 