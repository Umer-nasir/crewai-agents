# CrewAI Cold Email Generator - Streamlit App

A web application that generates personalized cold emails using AI agents powered by CrewAI.

## 🚀 Features

- **Dynamic URL Input**: Users can enter any company website URL
- **Sequential Agent Processing**: Researcher → Strategist → Writer
- **Website Scraping**: Analyzes target company websites
- **Service Matching**: Identifies the best agency service for each prospect
- **Email Generation**: Creates personalized cold emails under 150 words
- **Clean UI**: Simple and intuitive Streamlit interface
- **Secure**: Uses environment variables for API keys

## 📋 Requirements

- Python 3.8+
- Streamlit
- CrewAI
- Google Gemini API key

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Make sure your `.env` file contains:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**:
   Visit `http://localhost:8501`

## ☁️ Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app
4. Connect your GitHub repository
5. Set the main file path to `app.py`
6. Add your secrets in the Streamlit Cloud dashboard:
   - Go to Settings → Secrets
   - Add `GEMINI_API_KEY` with your API key value
7. Deploy!

## 📁 Project Structure

```
.
├── app.py              # Main Streamlit application
├── business.py         # Original terminal version (reference)
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (local)
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🔐 Security Notes

- Never commit your `.env` file to version control
- The `.env` file is included in `.gitignore`
- Use Streamlit Cloud secrets for deployment
- API keys are loaded securely using `python-dotenv`

## 🎯 How It Works

The application uses 3 AI agents working in sequence:

1. **Researcher**: Analyzes the company website to identify business model and weaknesses
2. **Strategist**: Matches identified needs with the best agency service
3. **Writer**: Crafts a personalized, professional cold email

## 📝 Customization

To modify the agency services:
1. Edit the `agency_services` variable in `app.py`
2. Update the strategist agent's backstory accordingly

To change the email format:
1. Modify the writer agent's goal and backstory
2. Adjust the task_write description

## 🐛 Troubleshooting

**API Key Error**: 
- Make sure `GEMINI_API_KEY` is set in your environment
- Verify the API key is valid and has proper permissions

**Website Access Issues**:
- Some websites block scraping
- Try with different target URLs
- Check if the website requires authentication

**Streamlit Not Found**:
```bash
pip install streamlit
```

## 📄 License

MIT License
