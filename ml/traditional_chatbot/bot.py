# ml/traditional_chatbot/bot.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class TraditionalChatbot:
    """
    A standard chatbot with zero emotional awareness.
    Uses DialoGPT-medium — Microsoft's conversational model.
    
    This is your BASELINE for Objective 4 comparison.
    It responds based purely on text pattern matching,
    with no understanding of how the user is feeling.
    """

    MODEL_NAME = "microsoft/DialoGPT-medium"

    def __init__(self):
        print("🔄 Loading Traditional Chatbot model...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME,
            padding_side="left"
        )
        self.model = AutoModelForCausalLM.from_pretrained(self.MODEL_NAME)

        # Track full conversation history for context
        self.chat_history_ids = None
        self.turn_count = 0

        print("✅ Traditional Chatbot ready!")

    def respond(self, user_input: str) -> dict:
        """
        Generate a response with no emotional awareness.

        Args:
            user_input: raw text from user

        Returns:
            {
                "response": str,
                "turn": int,
                "bot_type": "traditional"
            }
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")

        # Encode the user input + EOS token
        # EOS = End Of Sequence — tells model "user stopped talking"
        new_input_ids = self.tokenizer.encode(
            user_input + self.tokenizer.eos_token,
            return_tensors="pt"
        )

        # Append to conversation history for context
        # If first turn, just use current input
        # If not, concatenate with history so model remembers context
        if self.chat_history_ids is not None:
            input_ids = torch.cat(
                [self.chat_history_ids, new_input_ids], dim=-1
            )
        else:
            input_ids = new_input_ids

        # Limit context window to last 1000 tokens
        # Prevents memory issues in long conversations
        if input_ids.shape[-1] > 1000:
            input_ids = input_ids[:, -1000:]

        # Generate response
        # do_sample=True → not always the same response (more natural)
        # temperature → higher = more random, lower = more focused
        # top_p → nucleus sampling, keeps output coherent
        self.chat_history_ids = self.model.generate(
            input_ids,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Decode only the NEW tokens (not the full history)
        response = self.tokenizer.decode(
            self.chat_history_ids[:, input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )

        self.turn_count += 1

        return {
            "response": response,
            "turn": self.turn_count,
            "bot_type": "traditional"
        }

    def reset(self):
        """Clear conversation history — call this between sessions."""
        self.chat_history_ids = None
        self.turn_count = 0