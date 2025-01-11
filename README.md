# Builder Voting Bot

This is a Telegram bot for managing builder proposals and votes. It allows users to propose builders with input for forms and their telegram handle, entire group vote for or against them, and generate invite links based on voting results.

## Features

- **Propose Builders**: Users can propose builders for voting.
- **Voting System**: Users can vote for or against proposed builders.
- **Invite Links**: Generate invite links for builders with sufficient votes.
- **Daily Reset**: Automatically resets daily stats and removes old proposals.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/builder-voting-bot.git
   cd builder-voting-bot
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed, then run:
   ```bash
   pip install pyTelegramBotAPI
   ```

3. **Configure the Bot**:
   - Set your Telegram bot token in an environment variable or configuration file.
   - Adjust the database name and proposal limits in the configuration.

4. **Run the Bot**:
   ```bash
   python invite.py
   ```

## Usage

- **/propose_builder [name]**: Propose a new builder for voting.
- **/generate_invite**: Generate an invite link for builders with enough votes.
- **/increment_daily_count**: Increment the daily proposal count.

## Improvements

- Securely store the API token.
- Add error handling and logging.
- Organize code into modules.
- Use a configuration file for settings.
- Implement unit tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Environment Setup

This project requires a Telegram bot token to function. You can set this up by creating a `.env.local` file in the root directory of the project.

### Steps to Set Up

1. Create a file named `.env.local` in the root directory.
2. Add the following line to the file:

   ```plaintext
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   ```

   Replace `your_telegram_bot_token_here` with your actual Telegram bot token.

3. Ensure that your environment can read from the `.env.local` file. This is typically handled by your development environment or deployment setup.

### Running the Bot

Once the environment is set up, you can run the bot using:
