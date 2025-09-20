import random

class NGramModel:
    def __init__(self, n=3, mode='word'):
        self.n = n
        self.mode = mode
        self.ngrams = {}
        self.start_tokens = []
        self.vocab = set()
    
    def train(self, corpus):
        """Train the n-gram model on given corpus"""
        if self.mode == 'word':
            tokens = corpus.split() if isinstance(corpus, str) else corpus
        else:  # character level
            tokens = list(corpus) if isinstance(corpus, str) else corpus
        
        self.vocab = set(tokens)
        
        # Build n-grams
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i+self.n-1])
            next_token = tokens[i+self.n-1]
            
            if ngram not in self.ngrams:
                self.ngrams[ngram] = {}
            
            if next_token not in self.ngrams[ngram]:
                self.ngrams[ngram][next_token] = 0
            
            self.ngrams[ngram][next_token] += 1
            
            # Track start tokens
            if i == 0:
                self.start_tokens.append(ngram)
    
    def get_next_token(self, context):
        """Get next token based on context using weighted random selection"""
        if context not in self.ngrams or not self.ngrams[context]:
            # For character mode, try shorter contexts if full context not found
            if self.mode == 'character' and len(context) > 1:
                shorter_context = context[1:]
                if shorter_context in self.ngrams and self.ngrams[shorter_context]:
                    return self.get_next_token(shorter_context)
            
            # Fallback: return random token from vocabulary
            if self.vocab:
                return random.choice(list(self.vocab))
            return " "
        
        # Get frequency distribution for weighted random selection
        tokens = list(self.ngrams[context].keys())
        frequencies = list(self.ngrams[context].values())
        
        # Weighted random selection
        total = sum(frequencies)
        rand_val = random.uniform(0, total)
        
        cumulative = 0
        for i, freq in enumerate(frequencies):
            cumulative += freq
            if rand_val <= cumulative:
                return tokens[i]
        
        return random.choice(tokens)
    
    def generate_text(self, max_length=20, start_context=None):
        """Generate text using the trained model with better character handling"""
        if not self.ngrams:
            return ""
        
        # Choose starting context
        if start_context is None:
            if self.start_tokens:
                context = random.choice(self.start_tokens)
            else:
                context = tuple([""] * (self.n - 1))
        else:
            if self.mode == 'word':
                context_tokens = start_context.split()[-self.n+1:]
            else:
                context_tokens = list(start_context)[-self.n+1:]
            
            # Pad if necessary
            while len(context_tokens) < self.n - 1:
                context_tokens.insert(0, " ")
            
            context = tuple(context_tokens)
        
        generated = list(context)
        
        for _ in range(max_length):
            next_token = self.get_next_token(context)
            
            if next_token is None or next_token == "":
                break
            
            generated.append(next_token)
            
            # Update context
            context = tuple(generated[-(self.n-1):])
            
            # For character mode, stop at reasonable punctuation points
            if self.mode == 'character' and next_token in ['.', '!', '?'] and len(generated) > 10:
                break
        
        if self.mode == 'word':
            result = " ".join(generated).strip()
            # Basic capitalization for word mode
            if result and result[0].islower():
                result = result[0].upper() + result[1:]
            return result
        else:
            result = "".join(generated).strip()
            # Clean up character mode output
            result = self._clean_character_output(result)
            return result
    
    def _clean_character_output(self, text):
        """Clean up character-level output"""
        if not text:
            return text
        
        # Remove excessive spaces
        text = ' '.join(text.split())
        
        # Ensure proper spacing around punctuation
        text = text.replace(' .', '.').replace(' ,', ',').replace(' ?', '?').replace(' !', '!')
        
        # Capitalize first letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        # Ensure it ends with punctuation
        if text and text[-1] not in ['.', '!', '?']:
            text += '.'
        
        return text