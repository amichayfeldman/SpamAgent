import re
import json
import logging
from omegaconf import DictConfig
from transformers import BertTokenizerFast, BertForSequenceClassification, pipeline
import torch


class URLAgent:
    def __init__(self, cfg: DictConfig):
        model_name = "CrabInHoney/urlbert-tiny-v3-phishing-classifier"
        tokenizer = BertTokenizerFast.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline(
                            "text-classification",
                            model=model,
                            tokenizer=tokenizer,
                            device=0 if torch.cuda.is_available() else -1,
                            top_k=1
                        )
        self.label_mapping = {"LABEL_0": 0, "LABEL_1": 1}

        self.url_pattern = cfg["agents"]["url"]["url_pattern"]
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def analyze(self, text):
        self.logger.info("Analyzing text for URLs and phishing indicators")
        
        url_pattern = self.url_pattern
        urls = re.findall(url_pattern, text)

        if not urls:
            self.logger.info("No URLs found in the text")
            return {
                "spam_likelihood": 0,
                "reasoning": "No URLs found in the text"
            }
        spam_liklihood_flag = False
        spam_liklihood = 0
        for url in urls:
            pred = self.classifier(url)[0][0]
            current_liklihood = pred["score"] if pred["label"] == "LABEL_1" else 1 - pred["score"]
            spam_liklihood += current_liklihood
            if pred["label"] == "LABEL_1":
                spam_liklihood_flag = True
                break
        if spam_liklihood_flag:
            spam_res = current_liklihood
        else:
            spam_res = spam_liklihood / len(urls)
        return {"spam_likelihood": spam_res,
                "reasoning": "One of the URLs is predicted as phishing" if spam_liklihood_flag else "averaged predicted over URLs"}
        