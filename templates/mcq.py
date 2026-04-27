from typing import List
class MCQPrompt():
    def __init__(self, prompt: str, choices: List[str]):
        self.prompt = prompt
        self.choices = choices

    def mcq_prompt_template(self) -> str:
        formatted_choices = [f"\n{chr(idx + 65)}. {choice}" for idx, choice in enumerate(self.choices)]
        return "\n".join([self.prompt] + formatted_choices)

