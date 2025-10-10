import math
import random
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set

class CharacterNGram:
    """
    Advanced Character-Level N-Gram Model for Xhosa
    Focuses on generating morphologically valid Xhosa words
    """
    
    def __init__(self, n: int = 4, smoothing: str = 'kneser_ney'):
        self.n = n
        self.smoothing = smoothing
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = defaultdict(int)
        self.vocab: Set[str] = set()
        self.continuation_counts = defaultdict(set)
        self.total_chars = 0
        
    def train(self, text_corpus: str):
        """Train the character-level N-gram model"""
        # Preprocess for character-level training
        text = text_corpus.lower()
        
        # Remove excessive whitespace but preserve word boundaries
        text = ' '.join(text.split())
        
        # Add start and end of word markers
        words = text.split()
        for word in words:
            if len(word) < 2:  # Skip very short words
                continue
                
            # Pad word with start/end markers
            padded_word = '^' + word + '$'
            
            for i in range(len(padded_word) - self.n + 1):
                ngram = padded_word[i:i + self.n]
                context = ngram[:-1]
                char = ngram[-1]
                
                self.ngram_counts[context][char] += 1
                self.context_counts[context] += 1
                self.vocab.add(char)
                self.continuation_counts[context].add(char)
                self.total_chars += 1
    
    def probability(self, context: str, char: str) -> float:
        """Calculate character probability with smoothing"""
        if self.smoothing == 'kneser_ney':
            return self._kneser_ney_probability(context, char)
        elif self.smoothing == 'laplace':
            return self._laplace_probability(context, char)
        else:
            return self._mle_probability(context, char)
    
    def _kneser_ney_probability(self, context: str, char: str) -> float:
        """Kneser-Ney smoothing for character-level"""
        if not context:
            return self.ngram_counts[''].get(char, 0) / max(1, sum(self.ngram_counts[''].values()))
        
        discount = 0.75
        higher_order = max(self.ngram_counts[context].get(char, 0) - discount, 0)
        higher_order_denom = self.context_counts.get(context, 0)
        
        continuation_count = len(self.continuation_counts[context])
        lower_order_context = context[1:] if len(context) > 1 else ''
        lower_order_prob = self._kneser_ney_probability(lower_order_context, char)
        
        if higher_order_denom == 0:
            return lower_order_prob
            
        lambda_factor = (discount * continuation_count) / higher_order_denom
        
        return (higher_order / higher_order_denom) + (lambda_factor * lower_order_prob)
    
    def _laplace_probability(self, context: str, char: str) -> float:
        """Laplace smoothing for characters"""
        numerator = self.ngram_counts[context].get(char, 0) + 1
        denominator = self.context_counts.get(context, 0) + len(self.vocab)
        return numerator / denominator
    
    def _mle_probability(self, context: str, char: str) -> float:
        """Maximum Likelihood for characters"""
        if self.context_counts.get(context, 0) == 0:
            return 0
        return self.ngram_counts[context].get(char, 0) / self.context_counts[context]
    
    def generate_word(self, max_length: int = 12, start_pattern: str = None, max_attempts: int = 10) -> str:
        """Generate a Xhosa-like word with recursion protection"""
        for attempt in range(max_attempts):
            if start_pattern:
                context = '^' + start_pattern
                context = context[-(self.n - 1):]  # Ensure correct context length
                generated = list(start_pattern)
            else:
                context = '^' * (self.n - 1)
                generated = []
            
            for _ in range(max_length):
                candidates = []
                total_prob = 0
                
                for char in self.vocab:
                    prob = self.probability(context, char)
                    if prob > 0:
                        candidates.append((char, prob))
                        total_prob += prob
                
                if not candidates:
                    break
                    
                # Weighted random selection
                rand_val = random.uniform(0, total_prob)
                cumulative = 0
                selected_char = None
                
                for char, prob in candidates:
                    cumulative += prob
                    if rand_val <= cumulative:
                        selected_char = char
                        break
                
                if selected_char is None:
                    break
                    
                if selected_char == '$':  # End of word
                    break
                    
                generated.append(selected_char)
                context = context[1:] + selected_char
                
                if selected_char == '$':
                    break
            
            word = ''.join(generated)
            validated_word = self._validate_xhosa_word(word)
            
            # Only return if we have a reasonable word
            if validated_word and len(validated_word) >= 2:
                return validated_word
        
        # If all attempts fail, return a fallback word
        fallback_words = ['mholo', 'unjani', 'ndiyaphila', 'enkosi', 'kakuhle']
        return random.choice(fallback_words)
    
    def _validate_xhosa_word(self, word: str) -> str:
        """Apply Xhosa phonological constraints WITHOUT recursion"""
        if not word or len(word) < 2:
            return ""  # Return empty instead of recursing
            
        # Ensure word doesn't start with invalid sequences
        invalid_starts = ['bb', 'dd', 'ff', 'gg', 'hh', 'jj', 'kk', 'll', 
                         'mm', 'nn', 'pp', 'qq', 'rr', 'ss', 'tt', 'vv', 'ww', 'xx', 'yy', 'zz']
        for invalid in invalid_starts:
            if word.startswith(invalid):
                word = word[1:]  # Remove first character
                if not word:  # If word becomes empty
                    return ""
        
        # Ensure reasonable vowel-consonant alternation
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        
        # Count consecutive vowels/consonants
        consecutive_vowels = 0
        consecutive_consonants = 0
        new_word = []
        
        for char in word:
            if char in vowels:
                consecutive_vowels += 1
                consecutive_consonants = 0
            elif char in consonants:
                consecutive_consonants += 1
                consecutive_vowels = 0
            
            # Limit consecutive characters
            if consecutive_vowels <= 3 and consecutive_consonants <= 2:
                new_word.append(char)
            # If limits exceeded, skip this character
        
        result = ''.join(new_word)
        return result if len(result) >= 2 else ""
    
    def generate_multiple_words(self, count: int = 5) -> List[str]:
        """Generate multiple Xhosa-like words"""
        words = []
        attempts = 0
        max_total_attempts = count * 20  # Prevent infinite loops
        
        while len(words) < count and attempts < max_total_attempts:
            word = self.generate_word()
            if word and len(word) >= 3:  # Only keep reasonably long words
                words.append(word)
            attempts += 1
        
        # Fill with fallbacks if needed
        while len(words) < count:
            fallback_words = ['mholo', 'unjani', 'ndiyaphila', 'enkosi', 'kakuhle', 
                            'sawubona', 'ngiyaphila', 'ngiyabonga', 'hamba', 'yah']
            words.append(random.choice(fallback_words))
        
        return words[:count]
    
    def perplexity(self, test_words: List[str]) -> float:
        """Calculate perplexity on test words"""
        total_log_prob = 0
        total_chars = 0
        
        for word in test_words:
            padded_word = '^' + word + '$'
            
            for i in range(self.n - 1, len(padded_word)):
                context = padded_word[i - self.n + 1:i]
                char = padded_word[i]
                
                prob = self.probability(context, char)
                if prob > 0:
                    total_log_prob += math.log2(prob)
                    total_chars += 1
        
        if total_chars == 0:
            return float('inf')
            
        avg_log_prob = total_log_prob / total_chars
        return 2 ** (-avg_log_prob)
    
    def get_model_stats(self) -> Dict:
        """Get character-level model statistics"""
        return {
            'character_vocab_size': len(self.vocab),
            'total_character_ngrams': sum(len(counts) for counts in self.ngram_counts.values()),
            'unique_character_contexts': len(self.ngram_counts),
            'total_characters': self.total_chars,
            'most_common_character_sequences': self._get_most_common_sequences(10)
        }
    
    def _get_most_common_sequences(self, k: int) -> List[Tuple]:
        """Get k most common character sequences"""
        all_sequences = []
        for context, counts in self.ngram_counts.items():
            for char, count in counts.most_common():
                all_sequences.append((context + char, count))
        
        return sorted(all_sequences, key=lambda x: x[1], reverse=True)[:k]