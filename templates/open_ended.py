class OpenEndedPrompt():
    def __init__(self, prompt: str):
        self.prompt = prompt

    def openended_prompt_template(self) -> str:
        return self.prompt