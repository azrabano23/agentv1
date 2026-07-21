# Azra Bano AI Agent

An intelligent AI agent that answers questions about Azra Bano by scraping her personal website and LinkedIn profile. Built with Python, Flask, and OpenAI's GPT models.

## Features

- 🤖 **Intelligent Q&A**: Ask questions about Azra's work, experience, education, and more
- 🌐 **Web Scraping**: Automatically extracts information from azra-bano.com and LinkedIn
- 🧠 **Vector Database**: Uses ChromaDB for efficient information retrieval
- 💬 **Real-time Chat**: Modern web interface with instant responses
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 🔄 **Auto-refresh**: Keep information up-to-date with one-click refresh

## Technology Stack

- **Backend**: Python, Flask
- **AI/ML**: OpenAI GPT-4, LangChain, Sentence Transformers
- **Database**: ChromaDB (Vector Database)
- **Web Scraping**: BeautifulSoup4, Selenium
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Modern CSS with gradients and animations

## Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Chrome browser (for Selenium web scraping)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agentv1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### First Time Setup

1. Open the application in your browser
2. Click "Start Chat" to initialize the knowledge base
3. The agent will automatically scrape Azra's website and LinkedIn profile
4. Once initialized, you can start asking questions!

### Asking Questions

You can ask questions like:
- "What does Azra Bano do for work?"
- "What is Azra's educational background?"
- "What are Azra's skills and expertise?"
- "Where can I find Azra's contact information?"
- "What projects has Azra worked on?"

### Refreshing Data

Click the "Refresh Data" button in the footer to update the knowledge base with the latest information from Azra's website and LinkedIn.

## Project Structure

```
agentv1/
├── app.py                 # Main Flask application
├── ai_agent.py           # Core AI agent logic
├── web_scraper.py        # Web scraping functionality
├── knowledge_base.py     # Vector database operations
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── env.example           # Environment variables template
├── README.md            # This file
├── templates/
│   └── index.html       # Main web interface
└── static/
    ├── css/
    │   └── style.css    # Modern styling
    └── js/
        └── app.js       # Frontend functionality
```

## API Endpoints

- `GET /` - Main chat interface
- `GET /api/status` - Get agent status
- `POST /api/initialize` - Initialize knowledge base
- `POST /api/ask` - Ask a question
- `GET /api/sample-questions` - Get sample questions
- `POST /api/refresh` - Refresh knowledge base

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `FLASK_SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `FLASK_DEBUG` | Enable debug mode | `True` |

### Customization

You can customize the agent by modifying `config.py`:

- Change the personal website URL (currently: https://azra-bano.com)
- Change the LinkedIn URL (currently: https://www.linkedin.com/in/meetazrabano/)
- Adjust OpenAI model settings
- Modify scraping parameters
- Update UI styling

## Features in Detail

### Web Scraping
- **Personal Website**: Extracts content, headings, links, and meta information from azra-bano.com
- **LinkedIn Profile**: Scrapes professional information, experience, education from https://www.linkedin.com/in/meetazrabano/
- **Direct URL Configuration**: Uses pre-configured LinkedIn URL for reliable scraping
- **Fallback Detection**: Can also extract LinkedIn URL from the personal website if needed
- **Error Handling**: Graceful handling of scraping failures with multiple selector fallbacks

### Knowledge Base
- **Vector Storage**: Uses ChromaDB for efficient similarity search
- **Content Chunking**: Breaks down content into manageable chunks
- **Metadata Tracking**: Tracks source and content type for each piece of information
- **Automatic Updates**: Refreshes data when requested

### AI Processing
- **Context-Aware Responses**: Uses relevant information from knowledge base
- **Confidence Scoring**: Indicates how confident the AI is in its response
- **Source Attribution**: Shows which sources were used for each answer
- **Conversational Tone**: Friendly and helpful responses

### User Interface
- **Modern Design**: Beautiful gradients and animations
- **Real-time Chat**: Instant message exchange
- **Mobile Responsive**: Works on all device sizes
- **Loading States**: Clear feedback during processing
- **Sample Questions**: Quick-start question suggestions

## Troubleshooting

### Common Issues

1. **OpenAI API Error**
   - Ensure your API key is correct and has sufficient credits
   - Check if the API key is properly set in the `.env` file

2. **Web Scraping Issues**
   - Make sure Chrome browser is installed
   - Check internet connection
   - Verify the website URLs are accessible

3. **Knowledge Base Errors**
   - Delete the `chroma_db` folder and reinitialize
   - Check disk space availability

4. **Port Already in Use**
   - Change the port in `app.py` or kill the existing process
   - Use `lsof -ti:5000 | xargs kill -9` to free the port

### Debug Mode

Enable debug mode by setting `FLASK_DEBUG=True` in your `.env` file for detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue on the repository or contact the maintainer.

---

**Note**: This AI agent is designed to provide information about Azra Bano based on publicly available information from her website and LinkedIn profile. Please respect privacy and use the information responsibly.
