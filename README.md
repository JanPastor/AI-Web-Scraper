# AI Web Scraper 🤖

An intelligent web scraping tool that combines Selenium-based web scraping with AI-powered content analysis using Ollama LLM. (You are free to use other LLMs, but Ollama is used here for simplicity). In order for this to work, there is a fair amount of setup required. Please read the instructions below carefully.

## Features
- 🌐 Advanced web scraping with BrightData's Scraping Browser
- 🧠 AI-powered content analysis using Ollama LLM
- 🚀 User-friendly Streamlit interface with two-panel layout
- 🛡️ Built-in CAPTCHA handling
- 📝 Clean text extraction and processing
- 📊 Batch processing for large content
- 💾 Multiple download formats (TXT, JSON)
- 📚 Interactive tips & tricks guide

## Prerequisites

1. **Python 3.8+**
2. **Ollama**
   - Install from [Ollama's official website](https://ollama.ai)
   - Pull the LLaMA 3.1 model:
     ```bash
     ollama pull llama3.1
     ```
Feel free to use other LLMs, but this example uses Ollama for simplicity. Just make sure to update the `model` variable in the `parse.py` file with the correct model name.

3. **BrightData Account**
   - Sign up at [BrightData](https://brightdata.com)
   - Get your Scraping Browser WebDriver URL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```env
   SBR_WEBDRIVER=your_brightdata_webdriver_url_here
   ```

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```

2. Access the web interface at `http://localhost:8501`

3. Enter a website URL and click "Scrape Website"

4. Once scraping is complete, you can:
   - View the raw scraped content
   - Ask questions about the content using natural language
   - Get AI-powered analysis of the content

## How It Works

1. **Web Scraping**: 
   - Uses BrightData's Scraping Browser for reliable web access
   - Handles CAPTCHAs automatically
   - Extracts clean text content

2. **Content Processing**:
   - Removes unnecessary HTML and scripts
   - Splits content into manageable chunks
   - Preserves meaningful text structure
   - Displays content in real-time viewer

3. **AI Analysis**:
   - Processes content using Ollama LLM
   - Handles large content through batch processing
   - Provides natural language understanding
   - Extracts specific information based on user queries
   - Offers downloadable results in multiple formats

## Limitations

- Requires a BrightData subscription (free trial available)
- Local LLM performance depends on your hardware 
- Some websites may block automated access (that is what BrightData Webscraping browser is for)
- Content analysis quality depends on the LLM model used

## Credits

This project is based on the original work by [Tech With Tim](https://github.com/techwithtim). 
- Original Tutorial: [Tech With Tim YouTube Channel](https://www.youtube.com/@TechWithTim)
- Tim's Programming Courses: [Learn Programming with Tim](https://techwithtim.net/dev)

## Acknowledgments

- Original concept and implementation by Tech With Tim
- Built with Streamlit
- Powered by Ollama
- Web scraping enabled by BrightData

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

No contributions are needed. This is a simple project for personal use. Think of it as a starting point.
