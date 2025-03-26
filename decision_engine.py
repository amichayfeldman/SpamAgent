from omegaconf import DictConfig
import logging
import pandas as pd

class DecisionEngine:
    def __init__(self, cfg: DictConfig):
        self.weights = cfg.decision_engine.weights
        self.spam_threshold = cfg.decision_engine.spam_threshold
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def make_decision(self, 
                      sentiment_result, 
                      grammar_result, 
                      url_result, 
                      domain_result):
        components = [
            (sentiment_result["spam_likelihood"], self.weights.sentiment),
            (grammar_result["spam_likelihood"], self.weights.grammar),
            (url_result["spam_likelihood"], self.weights.url),
            (domain_result["spam_likelihood"], self.weights.domain)
        ]
        valid_components = list(filter(lambda x: x[0] is not None, components))
        total_weights = sum(weight for _, weight in valid_components)
        normalized_components = [(score, weight/total_weights) for score, weight in valid_components] if total_weights > 0 else []
        final_score = sum(score * norm_weight for score, norm_weight in normalized_components) if normalized_components else 0
        
        is_spam = final_score >= self.spam_threshold
        reasoning = []
        
        if sentiment_result["spam_likelihood"] is not None and sentiment_result["spam_likelihood"] > 0.5:
            reasoning.append(f"Sentiment analysis: {sentiment_result['reasoning']}")
        
        if grammar_result["spam_likelihood"] is not None and grammar_result["spam_likelihood"] > 0.5:
            reasoning.append(f"Grammar analysis: {grammar_result['reasoning']}")
        
        if url_result["spam_likelihood"] is not None and url_result["spam_likelihood"] > 0.5:
            reasoning.append(f"URL analysis: {url_result['reasoning']}")
        
        if domain_result["spam_likelihood"] is not None and domain_result["spam_likelihood"] > 0.5:
            reasoning.append(f"Domain analysis: {domain_result['reasoning']}")
        
        if is_spam and not reasoning:
            reasoning.append("Combined factors indicate spam despite no single strong indicator")
        
        if not is_spam:
            reasoning.append(f"Message appears legitimate (confidence: {(1-final_score):.2f})")
        
        self.logger.info(f"Classification: {'SPAM' if is_spam else 'NOT SPAM'} with confidence: {final_score if is_spam else (1-final_score):.2f}")
        
        return {
            "is_spam": is_spam,
            "confidence": final_score,
            "reasoning": reasoning,
            "agent_scores": {
                "sentiment": sentiment_result["spam_likelihood"],
                "grammar": grammar_result["spam_likelihood"],
                "url": url_result["spam_likelihood"],
                "domain": domain_result["spam_likelihood"]
            },
            "detailed_results": {
                "sentiment": sentiment_result,
                "grammar": grammar_result,
                "url": url_result,
                "domain": domain_result
            }
        } 