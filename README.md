# Media Request Bot

A Telegram bot for requesting movies and TV shows through Sonarr and Radarr. Search and add media to your library directly from Telegram!

## Features

- 🎬 Search and request movies via Radarr
- 📺 Search and request TV shows via Sonarr
- 🔍 Interactive search with inline keyboard selection
- 🎤 Voice message support (optional - speak movie/show names!)
- ✅ Automatic addition to your media library
- 🤖 Simple Telegram interface

## Prerequisites

- Python 3.9 or higher (or Docker)
- Sonarr (running and configured)
- Radarr (running and configured)
- Telegram Bot Token (from @BotFather)
- Google Cloud Speech-to-Text API key (optional - only for voice commands)

## Installation

### Option 1: Docker (Recommended)

See the [Docker Setup](#docker-setup) section below.

### Option 2: Python Installation

1. **Clone or download this directory**

2. **Install dependencies**
   ```bash
   cd /Users/monalvalia/Downloads/media-request-bot
   pip3 install -r requirements.txt
   ```

   For best practice, use a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip3 install -r requirements.txt
   ```

3. **Create a Telegram bot**
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot` command
   - Follow the prompts to name your bot
   - Save the bot token you receive

4. **Get your Sonarr and Radarr API keys**

   **Sonarr:**
   - Open Sonarr web interface
   - Go to Settings → General
   - Copy the API Key
   - Note the URL (e.g., http://localhost:8989)
   - Go to Settings → Profiles → Find your preferred Quality Profile ID
   - Go to Settings → Media Management → Find your Root Folder path

   **Radarr:**
   - Open Radarr web interface
   - Go to Settings → General
   - Copy the API Key
   - Note the URL (e.g., http://localhost:7878)
   - Go to Settings → Profiles → Find your preferred Quality Profile ID
   - Go to Settings → Media Management → Find your Root Folder path

5. **Configure the bot**
   ```bash
   cp config.example.json config.json
   ```

   Edit `config.json` with your settings:
   ```json
   {
       "telegram": {
           "bot_token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
       },
       "sonarr": {
           "url": "http://localhost:8989",
           "api_key": "your_sonarr_api_key_here",
           "quality_profile_id": 1,
           "root_folder": "/media/tv"
       },
       "radarr": {
           "url": "http://localhost:7878",
           "api_key": "your_radarr_api_key_here",
           "quality_profile_id": 1,
           "root_folder": "/media/movies"
       }
   }
   ```

## Voice Commands Setup (Optional)

Voice commands allow you to speak movie and TV show names instead of typing them. This feature uses Google Cloud Speech-to-Text.

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable the **Speech-to-Text API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Speech-to-Text API"
   - Click "Enable"

### 2. Create Service Account

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name it (e.g., "media-bot-speech")
4. Grant role: "Cloud Speech Client"
5. Click "Done"

### 3. Create and Download Credentials

1. Click on your new service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Download the JSON file
6. Save it as `google-credentials.json` in your project directory

### 4. Update Configuration

Edit your `config.json` and add the voice section:

```json
{
    "telegram": { ... },
    "sonarr": { ... },
    "radarr": { ... },
    "voice": {
        "enabled": true,
        "google_credentials_path": "/app/google-credentials.json"
    }
}
```

**To disable voice commands:**
```json
"voice": {
    "enabled": false
}
```

### 5. Restart the Bot

```bash
docker-compose restart
```

### Google Cloud Pricing

- **Free Tier**: 60 minutes of audio per month
- **After free tier**: $0.006 per 15 seconds (~$1.44/hour)
- Most users stay within the free tier

### Using Voice Commands

1. Send `/movie` or `/show` to the bot
2. Instead of typing, **tap the microphone icon** in Telegram
3. **Speak** the movie or show name (e.g., "Inception" or "Breaking Bad")
4. The bot will transcribe and search automatically

**Tips:**
- Speak clearly and at normal pace
- Works best in quiet environments
- Supports English by default (can be configured for other languages)

## Docker Setup

### Quick Start with Docker Compose

1. **Navigate to the project directory**
   ```bash
   cd /Users/monalvalia/Downloads/media-request-bot
   ```

2. **Create configuration file**
   ```bash
   cp config.example.json config.json
   # Edit config.json with your settings (see Configuration section)
   ```

3. **Build and start the container**
   ```bash
   docker-compose up -d
   ```

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

5. **Stop the bot**
   ```bash
   docker-compose down
   ```

### Docker Commands Reference

**Build the image:**
```bash
docker-compose build
```

**Start the bot:**
```bash
docker-compose up -d
```

**Restart the bot:**
```bash
docker-compose restart
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the bot:**
```bash
docker-compose down
```

**Update the bot:**
```bash
git pull  # If using git
docker-compose down
docker-compose build
docker-compose up -d
```

### Manual Docker Commands

If you prefer not to use Docker Compose:

**Build:**
```bash
docker build -t media-request-bot .
```

**Run:**
```bash
docker run -d \
  --name media-request-bot \
  --restart unless-stopped \
  --network host \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/logs:/app/logs \
  -e TZ=America/New_York \
  media-request-bot
```

**View logs:**
```bash
docker logs -f media-request-bot
```

**Stop:**
```bash
docker stop media-request-bot
docker rm media-request-bot
```

### Docker Notes

- The container uses `network_mode: host` to easily access Sonarr/Radarr on localhost
- If Sonarr/Radarr are in other containers, consider using a Docker network instead
- Logs are persisted in the `./logs` directory
- Config file is mounted read-only for security
- Container automatically restarts unless stopped manually

## Usage

### Start the bot

**With Docker:**
```bash
docker-compose up -d
```

**Without Docker:**

```bash
python3 bot.py
```

You should see:
```
Bot is starting...
Open Telegram and send /start to your bot

Press Ctrl+C to stop
```

### Use the bot in Telegram

1. **Open Telegram** and search for your bot (by the username you created)

2. **Start a conversation** with `/start`

3. **Request a movie:**
   - Send `/movie`
   - Enter the movie title
   - Select from search results
   - Confirm to add

4. **Request a TV show:**
   - Send `/show`
   - Enter the show title
   - Select from search results
   - Confirm to add

### Available Commands

- `/start` - Welcome message
- `/help` - Show help information
- `/movie` - Request a movie (supports voice messages!)
- `/show` - Request a TV show (supports voice messages!)
- `/cancel` - Cancel current request

## Running in Background

### Using nohup (Linux/Mac)
```bash
nohup python3 bot.py > bot.log 2>&1 &
```

### Using screen (Linux/Mac)
```bash
screen -S media-bot
python3 bot.py
# Press Ctrl+A, then D to detach
# Use 'screen -r media-bot' to reattach
```

### Using systemd (Linux)
Create a service file at `/etc/systemd/system/media-request-bot.service`:
```ini
[Unit]
Description=Media Request Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/media-request-bot
ExecStart=/usr/bin/python3 bot.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable media-request-bot
sudo systemctl start media-request-bot
```

## How It Works

1. You send a `/movie` or `/show` command to the bot
2. The bot asks for a search query
3. It searches Radarr (for movies) or Sonarr (for shows)
4. You select from up to 10 results
5. The bot adds the media to your library
6. Radarr/Sonarr automatically starts downloading

## Troubleshooting

### Bot doesn't respond

1. Check that bot.py is running
2. Verify your Telegram bot token is correct
3. Make sure you've sent `/start` to the bot first

### Can't connect to Sonarr/Radarr

1. Verify the URLs are correct (include http:// or https://)
2. Check that Sonarr/Radarr are running
3. Verify API keys are correct
4. Check firewall settings if running on different machines

### Quality Profile ID / Root Folder not working

1. The Quality Profile ID is a number (usually 1, 2, 3, etc.)
2. Find it in Sonarr/Radarr Settings → Profiles
3. Root folder must be an exact path that exists in your system
4. Check Settings → Media Management → Root Folders

### Media already exists error

This is normal - Sonarr/Radarr won't add duplicates. The bot will show an error message if the media is already in your library.

## Security Notes

- **Never commit config.json** - It contains sensitive API keys
- Consider restricting bot access to specific Telegram user IDs
- Run the bot on a trusted network
- Keep your Telegram bot token secret

## Logs

Logs are stored in `logs/media-request-bot.log`

## Future Features

Possible enhancements:
- View download queue
- Get notifications when downloads complete
- User access control (whitelist specific Telegram users)
- Support for multiple quality profiles
- Search by IMDb/TMDB/TVDB ID

## License

This project is provided as-is for personal use.

## Disclaimer

This bot is not affiliated with, endorsed by, or in any way officially connected to Sonarr, Radarr, or Telegram. Use responsibly and in accordance with your media library's terms of service.
