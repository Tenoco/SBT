import sys
import cmd
import json
import os

from TEXT_PREPROCESSOR.text_preprocessor import TextPreprocessor
from TEXT_GENERATOR.text_generator import TextGenerator
from TEXT_PREDICTION.text_prediction import TextPredictor
from DATA_MANAGER.data_manager import DataManager
from RATING_MANAGER.rating_manager import RatingManager

class SBTConsole(cmd.Cmd):
    """
    A console-based interface for the Smart Bot Technology (SBT) system.
    
    Provides an interactive command-line interface with various modules
    and functionalities.
    """
    
    intro = """
    ========================================
    Welcome to Smart Bot Technology (SBT)!
    ========================================
    Type 'help' to see available commands.
    Type 'exit' to quit the console.
    ========================================
    """
    
    prompt = '(SBT) > '
    
    def __init__(self):
        """
        Initialize the SBT console with all necessary modules.
        """
        super().__init__()
        self.data_manager = DataManager()
        self.rating_manager = RatingManager(self.data_manager)
        self.text_preprocessor = TextPreprocessor()
        self.text_generator = TextGenerator()
        self.text_predictor = TextPredictor()  # Add text predictor
        
        # Load conversation history
        self.conversation_history = self.data_manager.load_conversation_history()
        
        # Initialize N-gram models
        self.bigram_model = None
        self.trigram_model = None
    def do_preprocess(self, arg):
        """
        Preprocess text input.
        Usage: preprocess <text>
        
        Demonstrates the text preprocessing capabilities:
        - Removes punctuation
        - Converts to lowercase
        - Removes extra whitespaces
        """
        if not arg:
            print("Please provide text to preprocess.")
            return
        
        cleaned_text = self.text_preprocessor.clean_text(arg)
        print(f"Original text: {arg}")
        print(f"Preprocessed text: {cleaned_text}")
    
    def do_generate(self, arg):
        """
        Generate a response based on input.
        Usage: generate <context>
        
        Uses the text generator to create a contextual response.
        """
        if not arg:
            print("Please provide a context for response generation.")
            return
        
        # First preprocess the input
        cleaned_input = self.text_preprocessor.clean_text(arg)
        
        # Generate response
        response = self.text_generator.generate_response(cleaned_input)
        
        # Save to conversation history
        exchange = {
            'input': arg,
            'response': response
        }
        self.conversation_history.append(exchange)
        self.data_manager.save_conversation_history(self.conversation_history)
        
        print(f"Input: {arg}")
        print(f"Generated Response: {response}")
    
    def do_history(self, arg):
        """
        View conversation history.
        Usage: history [limit]
        
        Displays recent conversation exchanges.
        Optional: specify number of recent exchanges to show.
        """
        try:
            limit = int(arg) if arg else len(self.conversation_history)
            recent_history = self.conversation_history[-limit:]
            
            print("Conversation History:")
            print("-" * 50)
            for i, exchange in enumerate(recent_history, 1):
                print(f"Exchange {i}:")
                print(f"  User: {exchange['input']}")
                print(f"  SBT: {exchange['response']}")
                print()
        except ValueError:
            print("Please provide a valid number for history limit.")
    
    def do_feedback(self, arg):
        """
        Process system feedback.
        Usage: feedback <rating>
        
        Adjust system parameters based on user feedback.
        Accepts 'good', 'bad', or a numerical rating (1-10).
        """
        if not arg:
            print("Please provide feedback (good/bad or 1-10).")
            return
        
        try:
            self.rating_manager.process_feedback(arg)
            current_params = self.rating_manager.get_current_params()
            print("Feedback processed successfully.")
            print("Current System Parameters:")
            for param, value in current_params.items():
                print(f"  {param}: {value}")
        except Exception as e:
            print(f"Error processing feedback: {e}")
    
    def do_spell_correct(self, arg):
        """
        Perform basic spell correction.
        Usage: spell_correct <text>
        
        Demonstrates basic spell correction functionality.
        """
        if not arg:
            print("Please provide text for spell correction.")
            return
        
        corrected_text = self.text_preprocessor.basic_spell_correct(arg)
        print(f"Original text: {arg}")
        print(f"Corrected text: {corrected_text}")
    
    def do_export(self, arg):
        """
        Export conversation history.
        Usage: export [filename]
        
        Exports conversation history to a specified file or default location.
        """
        filename = arg if arg else 'conversation_export.json'
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            print(f"Conversation history exported to {filename}")
        except Exception as e:
            print(f"Error exporting history: {e}")
    
    def do_clear_history(self, arg):
        """
        Clear conversation history.
        Usage: clear_history
        
        Removes all stored conversation exchanges.
        """
        self.conversation_history = []
        self.data_manager.save_conversation_history(self.conversation_history)
        print("Conversation history has been cleared.")
    
    def do_build_ngram(self, arg):
        """
        Build N-gram models from a specified file or conversation history.
        Usage: build_ngram <filepath> [n]
        
        Arguments:
        - filepath: Path to the text file for training the N-gram model
        - n: N-gram size (2 for bigram, 3 for trigram, default: 2)
        
        If no filepath is provided, uses conversation history for training.
        
        Example:
        build_ngram training_data.txt 2    # Build bigram model from file
        build_ngram training_data.txt 3    # Build trigram model from file
        build_ngram 2                      # Build bigram model from conversation history
        """
        # Parse arguments
        parts = arg.split()
        
        # Determine training data source and N-gram size
        filepath = None
        n = 2  # Default to bigram
        
        if len(parts) == 1:
            # Check if first argument is a file or n-gram size
            if parts[0] in ['2', '3']:
                n = int(parts[0])
            else:
                filepath = parts[0]
        elif len(parts) == 2:
            filepath = parts[0]
            n = int(parts[1])
        
        # Prepare training text
        if filepath:
            # Validate file exists
            if not os.path.exists(filepath):
                print(f"Error: File '{filepath}' does not exist.")
                return
            
            # Read training text from file
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    all_text = f.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        else:
            # Use conversation history if no file provided
            all_text = ' '.join([
                f"{exchange['input']} {exchange['response']}" 
                for exchange in self.conversation_history
            ])
        
        # Preprocess text
        try:
            cleaned_text = self.text_preprocessor.clean_text(all_text)
            tokens = cleaned_text.split()
            
            # Build N-gram model
            ngram_model = self.text_predictor.build_ngram_model(tokens, n=n)
            
            # Store the model based on n-gram size
            if n == 2:
                self.bigram_model = ngram_model
                print(f"Bigram model built successfully from {'file: ' + filepath if filepath else 'conversation history'}.")
            else:
                self.trigram_model = ngram_model
                print(f"Trigram model built successfully from {'file: ' + filepath if filepath else 'conversation history'}.")
        
        except Exception as e:
            print(f"Error building N-gram model: {e}")
    
    
    def do_predict_next_word(self, arg):
        """
        Predict the next word based on a prefix.
        Usage: predict_next_word <prefix> [model_type]
        
        model_type can be 'bigram' or 'trigram' (default: bigram)
        """
        if not arg:
            print("Please provide a prefix for prediction.")
            return
        
        # Split arguments
        parts = arg.split()
        prefix = ' '.join(parts[:-1]) if len(parts) > 1 and parts[-1] in ['bigram', 'trigram'] else arg
        model_type = parts[-1] if len(parts) > 1 and parts[-1] in ['bigram', 'trigram'] else 'bigram'
        
        # Select appropriate model
        if model_type == 'bigram':
            if not self.bigram_model:
                print("Please build a bigram model first using 'build_ngram'.")
                return
            model = self.bigram_model
            n = 2
        else:
            if not self.trigram_model:
                print("Please build a trigram model first using 'build_ngram 3'.")
                return
            model = self.trigram_model
            n = 3
        
        try:
            next_word = self.text_predictor.predict_next_word(
                model, 
                prefix, 
                n=n, 
                temperature=0.8  # Adjustable temperature
            )
            print(f"Predicted next word for '{prefix}': {next_word}")
        
        except Exception as e:
            print(f"Error predicting next word: {e}")
    
    def do_generate_sequence(self, arg):
        """
        Generate a sequence of words using N-gram model.
        Usage: generate_sequence <seed_text> [length] [model_type] [temperature]
        
        model_type can be 'bigram' or 'trigram' (default: bigram)
        length defaults to 10
        temperature defaults to 0.8
        """
        if not arg:
            print("Please provide a seed text for sequence generation.")
            return
        
        # Parse arguments
        parts = arg.split()
        seed_text = ' '.join(parts[:-3]) if len(parts) > 3 else ' '.join(parts[:-2]) if len(parts) > 2 else arg
        
        # Default values
        length = 10
        model_type = 'bigram'
        temperature = 0.8
        
        # Parse optional arguments
        if len(parts) > 1:
            try:
                length = int(parts[-3]) if parts[-3].isdigit() else length
                model_type = parts[-2] if parts[-2] in ['bigram', 'trigram'] else model_type
                temperature = float(parts[-1]) if parts[-1] != model_type else temperature
            except (ValueError, IndexError):
                pass
        
        # Select appropriate model
        if model_type == 'bigram':
            if not self.bigram_model:
                print("Please build a bigram model first using 'build_ngram'.")
                return
            model = self.bigram_model
            n = 2
        else:
            if not self.trigram_model:
                print("Please build a trigram model first using 'build_ngram 3'.")
                return
            model = self.trigram_model
            n = 3
        
        try:
            sequence = self.text_predictor.generate_sequence(
                model, 
                seed_text, 
                length=length, 
                n=n, 
                temperature=temperature
            )
            print(f"Generated sequence (seed: '{seed_text}', length: {length}):")
            print(sequence)
        
        except Exception as e:
            print(f"Error generating sequence: {e}")
    
    def do_exit(self, arg):
        """
        Exit the SBT console.
        Usage: exit
        """
        print("Exiting Smart Bot Technology console. Goodbye!")
        return True

def main():
    """
    Main entry point for the SBT console.
    """
    SBTConsole().cmdloop()

if __name__ == "__main__":
    main()