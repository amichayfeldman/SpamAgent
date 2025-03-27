import hydra
from omegaconf import DictConfig, OmegaConf
import logging

from pipeline import TextAnalysisPipeline  # Import the new pipeline class

# Setup logger
log = logging.getLogger(__name__)

@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:    
    sample_text = """Press here if you want to won the PRIZE!!!"""
    
    # Run the analysis using the pipeline
    pipeline = TextAnalysisPipeline(cfg)
    result = pipeline.analyze(sample_text)
    
    # Print results
    print("\nFinal Result:")
    print(f"Classification: {'SPAM' if result['is_spam'] else 'NOT SPAM'}")
    print(f"Confidence: {result['confidence']:.2f}")
    print("\nReasoning:")
    for reason in result['reasoning']:
        print(f"- {reason}")

if __name__ == "__main__":
    main() 