from .base_agent import BaseAgent
import json
import logging
from omegaconf import DictConfig
from pydantic import BaseModel 

class GrammarOutput(BaseModel):
    grammar_score: float
    unnatural_patterns: list[str]
    bot_generated_likelihood: float
    non_native_likelihood: float
    spam_likelihood: float
    reasoning: str

class GrammarAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.weight = cfg["agents"]["grammar"]["weight"]
        self.threshold = cfg["agents"]["grammar"]["threshold"]
    
    def analyze(self, text):
        self.logger.info("Analyzing text for grammatical anomalies and unnatural language patterns")
        
        system_prompt = self.prompts.GRAMMAR_SYSTEM
        user_prompt = self.prompts.GRAMMAR_USER.format(text=text)
        try:
            result = self.query_llm(system_prompt, user_prompt, schema=GrammarOutput)
            if isinstance(result, GrammarOutput):
                result = result.dict()
            return result  
        except (json.JSONDecodeError, AttributeError) as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return GrammarOutput(
                grammar_score=0.5,
                unnatural_patterns=[],
                bot_generated_likelihood=0,
                non_native_likelihood=0,
                spam_likelihood=0,
                reasoning="Failed to parse LLM response"
            ) 