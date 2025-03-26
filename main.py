import hydra
from omegaconf import DictConfig, OmegaConf
import logging

from agents.sentiment_agent import SentimentAgent
from agents.grammar_agent import GrammarAgent
from agents.url_agent import URLAgent
from agents.domain_agent import DomainAgent
from decision_engine import DecisionEngine

# Setup logger
log = logging.getLogger(__name__)

@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:    
    sample_text = """URGENT: Your account has been compromised! Click here to secure your account now: http://secure-account-verify.com. Don't delay or you may lose access permanently!!!"""
    
    # Run the analysis
    result = analyze_text(sample_text, cfg)
    
    # Print results
    print("\nFinal Result:")
    print(f"Classification: {'SPAM' if result['is_spam'] else 'NOT SPAM'}")
    print(f"Confidence: {result['confidence']:.2f}")
    print("\nReasoning:")
    for reason in result['reasoning']:
        print(f"- {reason}")

def analyze_text(text, cfg):
    agent_results = {}

    if cfg.agents.sentiment.enabled:
        log.info("Running sentiment analysis...")
        sentiment_agent = SentimentAgent(cfg)
        agent_results["sentiment"] = sentiment_agent.analyze(text)
    else:
        agent_results["sentiment"] = {"spam_likelihood": None, "reasoning": "Agent disabled"}
    
    if cfg.agents.grammar.enabled:
        log.info("Running grammar analysis...")
        grammar_agent = GrammarAgent(cfg)
        agent_results["grammar"] = grammar_agent.analyze(text)
    else:
        agent_results["grammar"] = {"spam_likelihood": None, "reasoning": "Agent disabled"}
    
    if cfg.agents.url.enabled:
        log.info("Running URL analysis...")
        url_agent = URLAgent(cfg)
        agent_results["url"] = url_agent.analyze(text)
        urls = agent_results["url"].get("urls", [])
    else:
        agent_results["url"] = {"spam_likelihood": None, "reasoning": "Agent disabled", "urls": []}
        urls = []
    
    if cfg.agents.domain.enabled and urls:
        log.info("Running domain analysis...")
        domain_agent = DomainAgent(cfg)
        agent_results["domain"] = domain_agent.analyze(urls)
    else:
        agent_results["domain"] = {"spam_likelihood": None, "reasoning": "Agent disabled or no URLs found"}
    
    log.info("Making final decision...")
    engine = DecisionEngine(cfg)
    final_result = engine.make_decision(
        agent_results["sentiment"],
        agent_results["grammar"],
        agent_results["url"],
        agent_results["domain"]
    )
    
    return final_result

if __name__ == "__main__":
    main() 