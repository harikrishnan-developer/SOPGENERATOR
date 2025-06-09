
import sys
sys.path.append('/content/drive/MyDrive/agentic_sop_project')

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.prompt_templates import GENERATION_PROMPT

# Optional: simple post-processing
def clean_section_output(text):
    VALID_SECTIONS = ["Title", "Objective", "Scope", "Procedures", "Compliance", "References"]
    for section in VALID_SECTIONS:
        text = text.replace(section, "")
    return text.strip()

class GeneratorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt_template = PromptTemplate.from_template(GENERATION_PROMPT)

    def generate_section(self, section_title, context):
        prompt = self.prompt_template.format(section_title=section_title, context=context)
        raw_output = self.llm.invoke(prompt).strip()
        return clean_section_output(raw_output)
