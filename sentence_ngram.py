import math
import random
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set
import re

class SentenceNGram:
    """
    Advanced Sentence-Level N-Gram Model for Xhosa
    Focuses on generating complete, syntactically coherent sentences
    """
    
    def __init__(self, n: int = 3, smoothing: str = 'kneser_ney'):
        self.n = n
        self.smoothing = smoothing
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = defaultdict(int)
        self.vocab: Set[str] = set()
        self.continuation_counts = defaultdict(set)
        self.total_tokens = 0
        self.start_tokens = []
        
    def preprocess_xhosa_sentence(self, text: str) -> List[str]:
        """Advanced Xhosa-specific sentence preprocessing"""
        # Convert to lowercase but preserve proper nouns and sentence structure
        text = text.lower()
        
        # Preserve Xhosa-specific characters and diacritics
        text = re.sub(r'[^\w\s\u00C0-\u00FF\u0100-\u017F]', '', text)  # Keep letters, numbers, whitespace, and extended Latin
        
        # Tokenize while preserving Xhosa morphological boundaries
        tokens = text.split()
        
        # Enhanced tokenization for agglutinative language
        processed_tokens = []
        for token in tokens:
            if len(token) > 8:  # Likely agglutinated word
                # Simple morphological segmentation for common Xhosa patterns
                segments = self.morphological_segment(token)
                processed_tokens.extend(segments)
            else:
                processed_tokens.append(token)
                
        return processed_tokens
    
    def morphological_segment(self, word: str) -> List[str]:
        """Basic morphological segmentation for Xhosa words"""
        segments = []
        
        # Common Xhosa prefixes
        prefixes = ['umu', 'aba', 'imi', 'ama', 'isi', 'izi', 'ubu', 'uku', 'ili']
        for prefix in prefixes:
            if word.startswith(prefix) and len(word) > len(prefix) + 2:
                segments.append(prefix)
                word = word[len(prefix):]
                break
        
        # Common Xhosa suffixes
        suffixes = ['eni', 'ini', 'oni', 'weni', 'yeni', 'kazi', 'ana']
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                segments.append(word[:-len(suffix)])
                segments.append(suffix)
                return segments
                
        segments.append(word)
        return segments
    
    def train(self, sentences: List[str]):
        """Train the sentence-level N-gram model"""
        for sentence in sentences:
            # Split conversation pairs and process each part
            if '|' in sentence:
                parts = sentence.split('|')
                for part in parts:
                    self._train_sentence(part.strip())
            else:
                self._train_sentence(sentence)
    
    def _train_sentence(self, sentence: str):
        """Train on a single sentence"""
        tokens = self.preprocess_xhosa_sentence(sentence)
        if len(tokens) < self.n:
            return
            
        # Add sentence markers
        padded_tokens = ['<s>'] * (self.n - 1) + tokens + ['</s>']
        
        for i in range(len(padded_tokens) - self.n + 1):
            ngram = tuple(padded_tokens[i:i + self.n])
            context = ngram[:-1]
            word = ngram[-1]
            
            self.ngram_counts[context][word] += 1
            self.context_counts[context] += 1
            self.vocab.add(word)
            self.continuation_counts[context].add(word)
            self.total_tokens += 1
            
            # Track sentence starters
            if context == tuple(['<s>'] * (self.n - 1)):
                self.start_tokens.append(word)
    
    def probability(self, context: Tuple[str, ...], word: str) -> float:
        """Calculate probability with advanced smoothing"""
        if self.smoothing == 'kneser_ney':
            return self._kneser_ney_probability(context, word)
        elif self.smoothing == 'laplace':
            return self._laplace_probability(context, word)
        else:  # Maximum Likelihood
            return self._mle_probability(context, word)
    
    def _kneser_ney_probability(self, context: Tuple[str, ...], word: str) -> float:
        """Kneser-Ney smoothing for better handling of unseen n-grams"""
        if not context:
            # Unigram probability
            return self.ngram_counts[()].get(word, 0) / max(1, sum(self.ngram_counts[()].values()))
        
        discount = 0.75  # Typical discount value
        
        # Higher order probability
        higher_order = max(self.ngram_counts[context].get(word, 0) - discount, 0)
        higher_order_denom = self.context_counts.get(context, 0)
        
        # Lower order continuation probability
        continuation_count = len(self.continuation_counts[context])
        lower_order_context = context[1:] if len(context) > 1 else ()
        lower_order_prob = self._kneser_ney_probability(lower_order_context, word)
        
        if higher_order_denom == 0:
            return lower_order_prob
            
        lambda_factor = (discount * continuation_count) / higher_order_denom
        
        return (higher_order / higher_order_denom) + (lambda_factor * lower_order_prob)
    
    def _laplace_probability(self, context: Tuple[str, ...], word: str) -> float:
        """Laplace (Add-One) smoothing"""
        numerator = self.ngram_counts[context].get(word, 0) + 1
        denominator = self.context_counts.get(context, 0) + len(self.vocab)
        return numerator / denominator
    
    def _mle_probability(self, context: Tuple[str, ...], word: str) -> float:
        """Maximum Likelihood Estimation"""
        if self.context_counts.get(context, 0) == 0:
            return 0
        return self.ngram_counts[context].get(word, 0) / self.context_counts[context]
    
    def generate_sentence(self, max_length: int = 20, start_context: List[str] = None) -> str:
        """Generate a complete Xhosa sentence"""
        if start_context:
            context = tuple(['<s>'] * (self.n - 1 - len(start_context)) + start_context)
        else:
            context = tuple(['<s>'] * (self.n - 1))
        
        generated = []
        
        for _ in range(max_length):
            # Get possible next words with probabilities
            candidates = []
            total_prob = 0
            
            for word in self.vocab:
                prob = self.probability(context, word)
                if prob > 0:
                    candidates.append((word, prob))
                    total_prob += prob
            
            if not candidates:
                break
                
            # Normalize probabilities and select
            rand_val = random.uniform(0, total_prob)
            cumulative = 0
            
            for word, prob in candidates:
                cumulative += prob
                if rand_val <= cumulative:
                    if word == '</s>':  # End of sentence
                        break
                    generated.append(word)
                    context = context[1:] + (word,)
                    break
            else:
                break
                
            if word == '</s>':
                break
        
        # Post-process generated sentence
        sentence = ' '.join(generated)
        return self._post_process_sentence(sentence)
    
    def _post_process_sentence(self, sentence: str) -> str:
        """Apply Xhosa-specific post-processing"""
        # Capitalize first letter
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]
        
        # Ensure proper spacing around punctuation
        sentence = re.sub(r'\s+([.,!?])', r'\1', sentence)
        
        # Add final punctuation if missing
        if sentence and not sentence[-1] in '.!?':
            sentence += '.'
            
        return sentence
    
    def perplexity(self, test_sentences: List[str]) -> float:
        """Calculate perplexity on test data"""
        total_log_prob = 0
        total_words = 0
        
        for sentence in test_sentences:
            tokens = self.preprocess_xhosa_sentence(sentence)
            if len(tokens) < self.n:
                continue
                
            padded_tokens = ['<s>'] * (self.n - 1) + tokens + ['</s>']
            
            for i in range(self.n - 1, len(padded_tokens)):
                context = tuple(padded_tokens[i - self.n + 1:i])
                word = padded_tokens[i]
                
                prob = self.probability(context, word)
                if prob > 0:
                    total_log_prob += math.log2(prob)
                    total_words += 1
        
        if total_words == 0:
            return float('inf')
            
        avg_log_prob = total_log_prob / total_words
        return 2 ** (-avg_log_prob)
    
    def get_model_stats(self) -> Dict:
        """Get comprehensive model statistics"""
        return {
            'vocab_size': len(self.vocab),
            'total_ngrams': sum(len(counts) for counts in self.ngram_counts.values()),
            'unique_contexts': len(self.ngram_counts),
            'total_tokens': self.total_tokens,
            'most_common_ngrams': self._get_most_common_ngrams(10)
        }
    
    def _get_most_common_ngrams(self, k: int) -> List[Tuple]:
        """Get k most common n-grams"""
        all_ngrams = []
        for context, counts in self.ngram_counts.items():
            for word, count in counts.most_common():
                all_ngrams.append((context + (word,), count))
        
        return sorted(all_ngrams, key=lambda x: x[1], reverse=True)[:k]