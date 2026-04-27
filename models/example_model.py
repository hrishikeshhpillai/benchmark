from transformers import AudioFlamingo3ForConditionalGeneration, AutoProcessor

class CustomModel():
    def __init__(self, model_id: str = "nvidia/audio-flamingo-3-hf", device: str = "auto"):
        self.model_id = model_id
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AudioFlamingo3ForConditionalGeneration.from_pretrained(model_id, device_map=device)

    def generate(self, prompt: str, audio_path: str):

        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "audio", "path": audio_path},
                ],
            }
        ]

        inputs = self.processor.apply_chat_template(
            conversation,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
        ).to(model.device)

        outputs = self.model.generate(**inputs, max_new_tokens=500)

        decoded_outputs = self.processor.batch_decode(outputs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return decoded_outputs
