#!/usr/bin/env python3
"""Media Request Bot - Telegram bot for Sonarr and Radarr"""

import logging
import sys

from lib.bot_handler import MediaRequestBot
from lib.config import Config
from lib.radarr_client import RadarrClient
from lib.sonarr_client import SonarrClient
from lib.voice_handler import VoiceHandler


def setup_logging() -> None:
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/media-request-bot.log"),
            logging.StreamHandler()
        ]
    )

    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)


def main() -> None:
    """Main entry point"""
    print("=" * 60)
    print("Media Request Bot")
    print("Telegram bot for Sonarr and Radarr")
    print("=" * 60)
    print()

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = Config()

        # Initialize Sonarr client
        logger.info("Initializing Sonarr client...")
        sonarr_config = config.sonarr_config
        sonarr = SonarrClient(
            base_url=sonarr_config["url"],
            api_key=sonarr_config["api_key"]
        )

        # Test Sonarr connection
        if not sonarr.test_connection():
            logger.error("Failed to connect to Sonarr. Please check your configuration.")
            sys.exit(1)

        # Initialize Radarr client
        logger.info("Initializing Radarr client...")
        radarr_config = config.radarr_config
        radarr = RadarrClient(
            base_url=radarr_config["url"],
            api_key=radarr_config["api_key"]
        )

        # Test Radarr connection
        if not radarr.test_connection():
            logger.error("Failed to connect to Radarr. Please check your configuration.")
            sys.exit(1)

        # Initialize voice handler if configured
        logger.info("Initializing voice handler...")
        voice_config = config.voice_config
        voice_handler = None
        if voice_config.get("enabled", False):
            credentials_path = voice_config.get("google_credentials_path")
            voice_handler = VoiceHandler(credentials_path)
            if voice_handler.is_enabled():
                logger.info("Voice commands enabled")
            else:
                logger.info("Voice commands disabled (credentials not found)")
        else:
            logger.info("Voice commands disabled in config")

        # Initialize and run bot
        logger.info("Initializing Telegram bot...")
        bot = MediaRequestBot(
            telegram_token=config.telegram_token,
            sonarr_client=sonarr,
            radarr_client=radarr,
            sonarr_quality_profile_id=sonarr_config["quality_profile_id"],
            radarr_quality_profile_id=radarr_config["quality_profile_id"],
            sonarr_root_folder=sonarr_config["root_folder"],
            radarr_root_folder=radarr_config["root_folder"],
            voice_handler=voice_handler
        )

        print()
        print("Bot is starting...")
        print("Open Telegram and send /start to your bot")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()

        bot.run()

    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
