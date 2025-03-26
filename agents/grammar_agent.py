from .base_agent import BaseAgent
import json
import logging
from omegaconf import DictConfig

class GrammarAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.weight = cfg.agents.grammar.weight
        self.threshold = cfg.agents.grammar.threshold
    
    def analyze(self, text):
        self.logger.info("Analyzing text for grammatical anomalies and unnatural language patterns")
        
        system_prompt = self.prompts.GRAMMAR_SYSTEM
        user_prompt = self.prompts.GRAMMAR_USER.format(text=text)
        try:
            result = self.query_llm(system_prompt, user_prompt)
            spam_likelihood = result.get("spam_likelihood", 0)
            return {
                "grammar_score": result.get("grammar_score", 0.5),
                "unnatural_patterns": result.get("unnatural_patterns", []),
                "bot_generated_likelihood": result.get("bot_generated_likelihood", 0),
                "non_native_likelihood": result.get("non_native_likelihood", 0),
                "spam_likelihood": spam_likelihood,
                "reasoning": result.get("reasoning", "No reasoning provided")
            }
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return {
                "grammar_score": 0.5,
                "unnatural_patterns": [],
                "bot_generated_likelihood": 0,
                "non_native_likelihood": 0,
                "spam_likelihood": 0,
                "reasoning": "Failed to parse LLM response"
            } 