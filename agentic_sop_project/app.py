
import sys
sys.path.append('/content/drive/MyDrive/agentic_sop_project')

import streamlit as st
from utils.llm_handler import get_llama_model
from utils.data_ingestor import load_and_split_documents, create_and_populate_vector_store
from agents.planner import PlannerAgent
from agents.generator import GeneratorAgent
import json
from datetime import datetime

def clean_section_output(text):
    VALID_SECTIONS = ["Title", "Objective", "Scope", "Procedures", "Compliance", "References"]
    for section in VALID_SECTIONS:
        text = text.replace(section, "")
    return text.strip()

def clean_context(context):
    unwanted_phrases = [
    "Section Content:",
    "'' Section Content:",
    "Expected Output",
    "[Provide the correct section content",
    "[Explain your thought process",
    "[Include the generated output here]",
    "Hint:",
    "In this case, you should use the '' section title.",
    "Version:",
    "Author:",
    "johndoe@example.com",
    "Additional Notes:"
]

    filtered_lines = [
        line for line in context.splitlines()
        if not any(phrase in line for phrase in unwanted_phrases)
    ]
    return "\n".join(filtered_lines)

MODEL_PATH = '/content/drive/MyDrive/agentic_sop_project/models/meta-llama-3-8b.Q4_K_M.gguf'
DATA_DIR = '/content/drive/MyDrive/agentic_sop_project/data/'
CHROMA_DIR = '/content/drive/MyDrive/agentic_sop_project/chromadb/'

@st.cache_resource(show_spinner="Loading Llama model...")
def load_llm():
    return get_llama_model(MODEL_PATH)

@st.cache_resource(show_spinner="Building vector database...")
def load_db():
    docs = load_and_split_documents(DATA_DIR)
    return create_and_populate_vector_store(docs, CHROMA_DIR)

llm = load_llm()
db = load_db()

planner = PlannerAgent(llm)
generator = GeneratorAgent(llm)

st.title("Agentic AI Finance SOP Generator")
user_request = st.text_area("Describe the finance SOP you need:")

if "sop_result" not in st.session_state:
    st.session_state["sop_result"] = ""

if st.button("Generate SOP"):
    try:
        st.info("Generating SOP, please wait...")
        sop_sections_json = planner.plan_sections(user_request)

        try:
            sop_sections_list = json.loads(sop_sections_json)
            if not isinstance(sop_sections_list, list):
                raise ValueError("Invalid sections list format")
        except Exception as e:
            st.warning(f"Fallback to default sections due to error: {e}")
            sop_sections_list = ["Title", "Objective", "Scope", "Procedures", "Compliance", "References"]

        sop_content = ""
        MAX_CONTEXT_CHARS = 4000

        for section in sop_sections_list:
            context_docs = db.as_retriever(search_kwargs={"k": 3}).invoke(f"{user_request} {section}")
            context = "\n".join(set(doc.page_content.strip() for doc in context_docs))
            context = clean_context(context) 
            context = context[:MAX_CONTEXT_CHARS]

            generated = generator.generate_section(section, context)
            section_text = clean_section_output(generated)

            heading_level = "##" if section != "Title" else "###"
            sop_content += f"{heading_level} {section}\n{section_text}\n\n"

        final_output = f"""
# Standard Operating Procedure (SOP)

**Title**: {user_request.title()}
**Effective Date**: {datetime.today().strftime('%Y-%m-%d')}
**Author**: AI Generator

{sop_content}
"""
        st.session_state["sop_result"] = final_output.strip()

    except Exception as e:
        st.error(f"Error generating SOP: {e}")

if st.session_state["sop_result"]:
    st.markdown(st.session_state["sop_result"])
    st.download_button("Download SOP", st.session_state["sop_result"], file_name="sop.md")
