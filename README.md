# Smart Bot Technology (SBT)

## Project Overview

Smart Bot Technology (SBT) is a modular, extensible AI chatbot system designed to demonstrate a flexible approach to natural language processing and interaction. The project showcases a clean, organized architecture with separate modules handling different aspects of conversational AI.

## Project Structure

```
SBT1/
│
├── sbt_main.py         # Central controller and console interface
├── TEXT_PREPROCESSOR/text_preprocessor.py # Text cleaning and normalization module
├── TEXT_GENERATOR/text_generator.py   # Response generation module
├── DATA_MANAGER/data_manager.py     # Data persistence and management module
├── RATING_MANAGER/rating_manager.py   # Feedback and parameter adjustment module
└── data/               # Directory for storing persistent data
    ├── conversation_history.json
    └── system_params.json
```

## Modules

### 1. Text Preprocessor
- Cleans and normalizes input text
- Removes punctuation
- Converts text to lowercase
- Removes extra whitespaces
- Performs basic spell correction

### 2. Text Generator
- Generates responses based on input context
- Uses template-based response generation
- Supports different types of interactions

### 3. Data Manager
- Handles persistent storage of conversation data
- Saves and loads conversation history
- Manages system configuration parameters

### 4. Rating Manager
- Processes user feedback
- Dynamically adjusts system parameters
- Allows for adaptive system behavior

### 5. Main Controller
- Integrates all modules
- Provides a command-line interface
- Manages overall system workflow

## Installation

### Prerequisites
- Python 3.7+
- No external dependencies required

### Setup
1. Clone the repository
2. Navigate to the project directory
3. Run the main script

```bash
git clone https://github.com/your-username/smart-bot-technology.git
cd smart-bot-technology
python sbt_main.py
```

## Usage

### Starting the Console
```bash
python sbt_main.py
```

### Available Commands
- Simply type a message to chat
- Commands:
  - `exit`: Close the SBT console
  - `history`: View recent conversations
  - `clear`: Clear conversation history

## Example Interaction
```
Welcome to Smart Bot Technology
Type 'help' for command list or start chatting.

SBT > Hello, how are you?
Hello! How can I help you today?

SBT > Tell me a joke
I'm not sure how to respond to that.

SBT > history
Recent Conversations:
1. You: Hello, how are you?
   SBT: Hello! How can I help you today?
2. You: Tell me a joke
   SBT: I'm not sure how to respond to that.
```

## Extensibility
The modular design allows easy extension and modification:
- Add new response templates
- Implement more advanced preprocessing
- Enhance feedback mechanisms

## Future Improvements
- Advanced natural language processing
- Machine learning-based response generation
- More sophisticated spell correction
- Enhanced context understanding

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License

## Contact
TENOCO
https://t.me/TENOCO
```

## Notes
- Customize the README with your specific project details
- Add your name, contact information
- Include any specific setup or usage instructions
- Adapt the license as needed
