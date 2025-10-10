import streamlit as st
import matplotlib.pyplot as plt
from character_ngram import CharacterNGram
from sentence_ngram import SentenceNGram
from word_corpus import get_word_corpus

def initialize_models():
    """Initialize and train both models"""
    corpus = get_word_corpus()
    
    # Train Character N-gram
    char_model = CharacterNGram(n=4, smoothing='kneser_ney')
    char_model.train(corpus)
    
    # Train Sentence N-gram
    sentence_model = SentenceNGram(n=3, smoothing='kneser_ney')
    # Use conversations from the corpus as training sentences
    conversations = [
        "Mholo unjani", "Ndiyaphila enkosi", "Ungubani igama lakho",
        "Ndivela eKapa", "Ndihlala eGoli", "Ewe ndiyasebenza",
        "Usapho lwam luyaphila", "Wamkelekile", "Ndithanda ukufunda",
        "Kulungile", "Ewe ndiyasithanda", "Ndiya edolophini"
    ]
    sentence_model.train(conversations)
    
    return char_model, sentence_model

def main():
    st.set_page_config(
        page_title="Xhosa N-gram Model Comparison",
        page_icon="🗣️",
        layout="wide"
    )
    
    st.title("🗣️ Xhosa N-gram Model Comparison")
    st.markdown("""
    Compare Character-level vs Sentence-level N-gram models for Xhosa language generation
    """)
    
    # Initialize models
    if 'char_model' not in st.session_state:
        with st.spinner("Training Xhosa N-gram models..."):
            st.session_state.char_model, st.session_state.sentence_model = initialize_models()
        st.success("Models trained successfully!")
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Model Performance")
        
        # Performance comparison
        if st.button("Run Performance Comparison"):
            # Test data
            test_words = ["mholo", "unjani", "ndiyaphila", "enkosi", "kakhulu"]
            test_sentences = ["Mholo unjani", "Ndiyaphila enkosi", "Ungubani igama lakho"]
            
            # Calculate perplexities
            char_perplexity = st.session_state.char_model.perplexity(test_words)
            sentence_perplexity = st.session_state.sentence_model.perplexity(test_sentences)
            
            # Display metrics
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Character Model Perplexity", f"{char_perplexity:.2f}")
            with metric_col2:
                st.metric("Sentence Model Perplexity", f"{sentence_perplexity:.2f}")
            
            # Plot comparison
            fig, ax = plt.subplots(figsize=(8, 4))
            models = ['Character N-gram', 'Sentence N-gram']
            perplexities = [char_perplexity, sentence_perplexity]
            
            bars = ax.bar(models, perplexities, color=['#FF6B6B', '#4ECDC4'])
            ax.set_ylabel('Perplexity Score')
            ax.set_title('Model Perplexity Comparison (Lower is Better)')
            ax.grid(axis='y', alpha=0.3)
            
            # Add value labels
            for bar, value in zip(bars, perplexities):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       f'{value:.2f}', ha='center', va='bottom')
            
            st.pyplot(fig)
        
        # Model Statistics
        st.subheader("Model Statistics")
        
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.write("**Character N-gram Model**")
            char_stats = st.session_state.char_model.get_model_stats()
            st.write(f"Vocabulary Size: {char_stats['character_vocab_size']}")
            st.write(f"Total N-grams: {char_stats['total_character_ngrams']}")
            st.write(f"Unique Contexts: {char_stats['unique_character_contexts']}")
            st.write(f"Total Characters: {char_stats['total_characters']}")
            
            st.write("**Most Common Sequences:**")
            for seq, count in char_stats['most_common_character_sequences'][:5]:
                st.write(f"`{seq}`: {count}")
        
        with stats_col2:
            st.write("**Sentence N-gram Model**")
            sentence_stats = st.session_state.sentence_model.get_model_stats()
            st.write(f"Vocabulary Size: {sentence_stats['vocab_size']}")
            st.write(f"Total N-grams: {sentence_stats['total_ngrams']}")
            st.write(f"Unique Contexts: {sentence_stats['unique_contexts']}")
            st.write(f"Total Tokens: {sentence_stats['total_tokens']}")
            
            st.write("**Most Common N-grams:**")
            for ngram, count in sentence_stats['most_common_ngrams'][:5]:
                st.write(f"`{' '.join(ngram)}`: {count}")
    
    with col2:
        st.subheader("Text Generation")
        
        # Character model generation
        st.write("**Character N-gram**")
        if st.button("Generate 5 Words"):
            words = st.session_state.char_model.generate_multiple_words(5)
            for i, word in enumerate(words, 1):
                st.write(f"{i}. `{word}`")
        
        char_start = st.text_input("Start pattern:", "ndi")
        if st.button("Generate from Pattern"):
            if char_start:
                word = st.session_state.char_model.generate_word(start_pattern=char_start)
                st.success(f"Generated: `{word}`")
        
        st.markdown("---")
        
        # Sentence model generation
        st.write("**Sentence N-gram**")
        if st.button("Generate 3 Sentences"):
            sentences = []
            for _ in range(3):
                sentence = st.session_state.sentence_model.generate_sentence()
                sentences.append(sentence)
            
            for i, sentence in enumerate(sentences, 1):
                st.write(f"{i}. {sentence}")
        
        sentence_start = st.text_input("Start words:", "mholo")
        if st.button("Generate from Start"):
            if sentence_start:
                sentence = st.session_state.sentence_model.generate_sentence(
                    start_context=sentence_start.split()
                )
                st.success(f"Generated: {sentence}")
    
    # Experiments Section
    st.markdown("---")
    st.subheader("Experiments")
    
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        st.write("**N-gram Order Comparison**")
        
        if st.button("Compare N-gram Orders"):
            n_values = [2, 3, 4]
            perplexities = []
            
            for n in n_values:
                test_model = CharacterNGram(n=n)
                test_model.train(get_word_corpus())
                test_words = ["mholo", "unjani", "ndiyaphila"]
                perplexity = test_model.perplexity(test_words)
                perplexities.append(perplexity)
            
            # Plot results
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(n_values, perplexities, 'o-', linewidth=2, markersize=8)
            ax.set_xlabel('N-gram Order')
            ax.set_ylabel('Perplexity')
            ax.set_title('Perplexity vs N-gram Order')
            ax.grid(True, alpha=0.3)
            
            for i, (n, p) in enumerate(zip(n_values, perplexities)):
                ax.annotate(f'{p:.1f}', (n, p), textcoords="offset points", 
                           xytext=(0,10), ha='center')
            
            st.pyplot(fig)
    
    with exp_col2:
        st.write("**Smoothing Comparison**")
        
        if st.button("Compare Smoothing Methods"):
            methods = ['kneser_ney', 'laplace', 'mle']
            perplexities = []
            
            for method in methods:
                test_model = CharacterNGram(n=3, smoothing=method)
                test_model.train(get_word_corpus())
                test_words = ["mholo", "unjani", "ndiyaphila"]
                perplexity = test_model.perplexity(test_words)
                perplexities.append(perplexity)
            
            # Plot results
            fig, ax = plt.subplots(figsize=(8, 4))
            bars = ax.bar(methods, perplexities, color=['#FF9999', '#99FF99', '#9999FF'])
            ax.set_xlabel('Smoothing Method')
            ax.set_ylabel('Perplexity')
            ax.set_title('Perplexity vs Smoothing Technique')
            ax.grid(axis='y', alpha=0.3)
            
            for bar, value in zip(bars, perplexities):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       f'{value:.2f}', ha='center', va='bottom')
            
            st.pyplot(fig)
    
    # Training Data Info
    st.markdown("---")
    st.subheader("Training Data")
    
    data_col1, data_col2 = st.columns(2)
    
    with data_col1:
        st.write("**Word Corpus Info**")
        corpus = get_word_corpus()
        words = corpus.split()
        unique_words = set(words)
        
        st.write(f"Total words: {len(words)}")
        st.write(f"Unique words: {len(unique_words)}")
        st.write(f"Average word length: {sum(len(word) for word in words) / len(words):.1f} chars")
        
        # Word length distribution
        word_lengths = [len(word) for word in words]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.hist(word_lengths, bins=15, alpha=0.7, color='skyblue')
        ax.set_xlabel('Word Length')
        ax.set_ylabel('Frequency')
        ax.set_title('Word Length Distribution')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with data_col2:
        st.write("**Sample Training Data**")
        corpus = get_word_corpus()
        sample_words = list(set(corpus.split()))[:20]  # First 20 unique words
        st.write("Sample vocabulary:")
        for word in sample_words:
            st.write(f"`{word}`")

if __name__ == "__main__":
    main()