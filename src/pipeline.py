import pyrootutils
root  = pyrootutils.setup_root(__file__, 
                               pythonpath=True,
                               cwd=True)

from src.agents.sentiment_agent import SentimentAgent
from src.agents.grammar_agent import GrammarAgent
from src.agents.url_agent import URLAgent
from src.agents.domain_agent import DomainAgent
from src.agents.cleaning_agent import CleaningAgent
from src.decision_engine import DecisionEngine
import logging

class TextAnalysisPipeline:
    def __init__(self, cfg):
        self.cfg = cfg
        self.agent_results = {}
        self.log = logging.getLogger(__name__)

    def analyze(self, text):
        # Step 1: Clean the text using CleaningAgent
        cleaning_agent = CleaningAgent(self.cfg)
        cleaned_text = cleaning_agent.analyze(text)

        if self.cfg["agents"]["sentiment"]["enabled"]:
            self.log.info("Running sentiment analysis...")
            sentiment_agent = SentimentAgent(self.cfg)
            self.agent_results["sentiment"] = sentiment_agent.analyze(cleaned_text)
        else:
            self.agent_results["sentiment"] = {"spam_likelihood": None, "reasoning": "Agent disabled"}
        
        if self.cfg["agents"]["grammar"]["enabled"]:
            self.log.info("Running grammar analysis...")
            grammar_agent = GrammarAgent(self.cfg)
            self.agent_results["grammar"] = grammar_agent.analyze(cleaned_text)
        else:
            self.agent_results["grammar"] = {"spam_likelihood": None, "reasoning": "Agent disabled"}
        
        if self.cfg["agents"]["url"]["enabled"]:
            self.log.info("Running URL analysis...")
            url_agent = URLAgent(self.cfg)
            self.agent_results["url"] = url_agent.analyze(cleaned_text)
            urls = self.agent_results["url"].get("urls", [])
        else:
            self.agent_results["url"] = {"spam_likelihood": None, "reasoning": "Agent disabled", "urls": []}
            urls = []
        
        if self.cfg["agents"]["domain"]["enabled"] and urls:
            self.log.info("Running domain analysis...")
            domain_agent = DomainAgent(self.cfg)
            self.agent_results["domain"] = domain_agent.analyze(urls)
        else:
            self.agent_results["domain"] = {"spam_likelihood": None, "reasoning": "Agent disabled or no URLs found"}
        
        self.log.info("Making final decision...")
        engine = DecisionEngine(self.cfg)
        final_result = engine.make_decision(
            self.agent_results["sentiment"],
            self.agent_results["grammar"],
            self.agent_results["url"],
            self.agent_results["domain"]
        )
        
        return final_result 