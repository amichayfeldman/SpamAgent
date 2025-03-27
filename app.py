import streamlit as st
from omegaconf import OmegaConf
from hydra import compose, initialize
from pipeline import TextAnalysisPipeline

@st.cache_data
def load_config():    
    with initialize(version_base=None, config_path="configs"):
        cfg = compose(config_name="config")
        cfg = OmegaConf.to_container(cfg, resolve=True)
    return cfg

@st.cache_resource
def init_pipeline(cfg):
    return TextAnalysisPipeline(cfg)

cfg = load_config()
pipeline = init_pipeline(cfg)

st.title("Spam Detection App")
st.sidebar.header("Input Text")
input_text = st.sidebar.text_input("Enter your text here:")

if st.sidebar.button("Submit"):
    if input_text:
        result = pipeline.analyze(input_text)

        st.subheader("Final Result:")
        st.write(f"**Classification:** {'SPAM' if result['is_spam'] else 'NOT SPAM'}")
        st.write(f"**Confidence:** {result['confidence']:.2f}")
        st.divider()
        st.subheader("Reasoning:")
        for reason in result['reasoning']:
            st.write(f"- {reason}")
    else:
        st.warning("Please enter some text to analyze.")