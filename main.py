import praw
import groq
import schedule
import time
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='reddit_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class RedditGroqBot:
    def __init__(self):
        # Reddit API credentials
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD')
        )

        # Groq API setup
        self.groq_client = groq.Client(api_key=os.getenv('GROQ_API_KEY'))

        # Subreddit to post to
        self.subreddit_name = os.getenv('SUBREDDIT_NAME')
        self.subreddit = self.reddit.subreddit(self.subreddit_name)

    def generate_content(self, prompt):
        """Generate content using Groq AI"""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=2000
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating content: {str(e)}")
            return None

    def create_post(self):
        """Create a new Reddit post"""
        try:
            # Generate post title and content
            post_prompt = "Generate an engaging Reddit post title and content about technology trends."
            generated_content = self.generate_content(post_prompt)

            if generated_content:
                # Split content into title and body
                lines = generated_content.split('\n')
                title = lines[0]
                body = '\n'.join(lines[1:])

                # Create Reddit post
                self.subreddit.submit(title=title, selftext=body)
                logging.info(f"Successfully created post: {title}")
        except Exception as e:
            logging.error(f"Error creating post: {str(e)}")

    def generate_comment(self, post_text):
        """Generate a comment based on post content"""
        try:
            prompt = f"Generate a thoughtful and relevant comment for the following post: {post_text}"
            return self.generate_content(prompt)
        except Exception as e:
            logging.error(f"Error generating comment: {str(e)}")
            return None

    def comment_on_posts(self, limit=5):
        """Comment on recent posts in the subreddit"""
        try:
            for post in self.subreddit.new(limit=limit):
                # Check if we haven't already commented
                already_commented = any(comment.author == self.reddit.user.me()
                                        for comment in post.comments.list())

                if not already_commented:
                    comment_text = self.generate_comment(post.selftext)
                    if comment_text:
                        post.reply(comment_text)
                        logging.info(f"Commented on post: {post.title}")
                        time.sleep(60)  # Wait between comments to avoid rate limits
        except Exception as e:
            logging.error(f"Error commenting on posts: {str(e)}")

    def run_scheduled_tasks(self):
        """Run the bot's scheduled tasks"""
        schedule.every().day.at("11:25").do(self.create_post)
        schedule.every().day.at("10:26").do(self.comment_on_posts)

        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key
SUBREDDIT_NAME=your_subreddit_name
""")

    bot = RedditGroqBot()
    bot.run_scheduled_tasks()


if __name__ == "__main__":
    main()
