
import sys
sys.path.append('/content/drive/MyDrive/agentic_sop_project')

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.prompt_templates import PLANNING_PROMPT
import re
import json

VALID_SECTIONS = ["Title", "Objective", "Scope", "Procedures", "Compliance", "References"]

class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(PLANNING_PROMPT)
        self.chain = LLMChain(llm=llm, prompt=self.prompt)

    def plan_sections(self, user_request):
        try:
            output = self.chain.run(user_request=user_request).strip()

            # First, try to parse output as JSON
            try:
                sections = json.loads(output)
                if not isinstance(sections, list):
                    raise ValueError("Parsed JSON is not a list")
            except Exception:
                # Fallback to regex extraction
                sections = re.findall(r'"(.*?)"', output)

            # Validate sections - keep only valid ones, enforce order
            sections = [s for s in sections if s in VALID_SECTIONS]
            sections = [s for s in VALID_SECTIONS if s in sections]

            if not sections:
                raise ValueError("No valid sections found")

            return json.dumps(sections)

        except Exception as e:
            print(f"[PlannerAgent] Fallback triggered due to error: {e}")
            return json.dumps(VALID_SECTIONS)
