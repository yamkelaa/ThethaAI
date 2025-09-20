from data_generator import get_word_level_corpus, get_char_level_corpus
from ngram_model import NGramModel
import random

class XhosaChatbot:
    def __init__(self, n=3, mode='word'):
        self.model = NGramModel(n, mode)
        self.mode = mode
        self.n = n
        
        # Train the model
        if mode == 'word':
            corpus = " ".join(get_word_level_corpus())
        else:
            corpus = "".join(get_char_level_corpus())
        
        self.model.train(corpus)
    
    def respond(self, user_input, max_length=15):
        """Generate a response to user input"""
        if not user_input.strip():
            # If empty input, generate random greeting
            return self.model.generate_text(max_length=random.randint(5, 10))
        
        if self.mode == 'word':
            # Use last few words as context
            words = user_input.split()
            context = " ".join(words[-min(len(words), self.n-1):])
        else:
            # Use last few characters as context
            context = user_input[-min(len(user_input), self.n-1):]
        
        response = self.model.generate_text(max_length, context)
        return response
    
    def generate_sample(self, prompt=None, length=10):
        """Generate sample text with optional prompt"""
        return self.model.generate_text(length, prompt)