# Reddit Groq Bot

A Python-based Reddit bot that automatically generates and posts content about technology trends using the Groq AI API. The bot can create new posts and engage with existing content through AI-generated comments.

## Features

- 🤖 Automated post creation using Groq AI
- 💬 Intelligent comment generation on existing posts
- ⏰ Scheduled posting and commenting capabilities
- 📝 Comprehensive logging system
- 🔐 Secure environment variable configuration

## Prerequisites

Before running the bot, make sure you have the following:

- Python 3.7 or higher
- Reddit API credentials (client ID, client secret, username, password)
- Groq API key
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:
```bash
https://github.com/Ashish032002/RedditBot.git
cd reddit-groq-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install required packages:
```bash
pip install praw groq schedule python-dotenv
```

4. Create a `.env` file in the project root and add your credentials:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key
SUBREDDIT_NAME=target_subreddit
```

## Usage

To start the bot, run:
```bash
python main.py
```

The bot will:
- You can Modify Main.py and can add your preferred time to post and comment on posts.
- For now i have added time of my choice
- Create new posts daily at 11:25
- Comment on recent posts daily at 10:26
- Log all activities in `reddit_bot.log`

## Project Structure

```
reddit-groq-bot/
├── .env                # Environment variables configuration
├── main.py            # Main bot implementation
├── reddit_bot.log     # Activity logs
├── .gitignore         # Git ignore file
└── README.md          # Project documentation
```

## Configuration

The bot's behavior can be customized by modifying the following parameters in `main.py`:

- Schedule timing for posts and comments
- Number of posts to comment on (`limit` parameter in `comment_on_posts`)
- AI temperature and max tokens in `generate_content`
- Sleep duration between comments

## Safety and Rate Limiting

The bot implements several safety measures:

- Checks for existing comments before posting new ones
- Includes a 60-second delay between comments
- Uses scheduled tasks to prevent excessive posting
- Implements comprehensive error logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot is for educational purposes. Make sure to comply with Reddit's API terms of service and content policies when using this bot.

## Security Note

⚠️ Never commit your `.env` file or expose your API credentials. The `.env` file should always be listed in your `.gitignore`.
