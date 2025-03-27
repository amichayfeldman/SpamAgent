from .base_agent import BaseAgent
import json
import logging
from omegaconf import DictConfig
from pydantic import BaseModel  


class SentimentOutput(BaseModel):
    emotional_manipulation: float
    sentiment: str
    persuasive_tactics: list[str]
    deceptive_language: float
    spam_likelihood: float
    reasoning: str

class SentimentAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.weight = cfg["agents"]["sentiment"]["weight"]
        self.threshold = cfg["agents"]["sentiment"]["threshold"]
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Sentiment agent initialized with weight: {self.weight}, threshold: {self.threshold}")
    
    def analyze(self, text):
        self.logger.info("Analyzing text for sentiment and manipulative language")
        
        system_prompt = self.prompts.SENTIMENT_SYSTEM
        user_prompt = self.prompts.SENTIMENT_USER.format(text=text)
        try:
            result = self.query_llm(system_prompt, user_prompt, schema=SentimentOutput)
            if isinstance(result, SentimentOutput):
                result = result.dict()
            return result 
        except (json.JSONDecodeError, AttributeError) as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return SentimentOutput(
                emotional_manipulation=0,
                sentiment="neutral",
                persuasive_tactics=[],
                deceptive_language=0,
                spam_likelihood=0,
                reasoning="Failed to parse LLM response"
            ) 