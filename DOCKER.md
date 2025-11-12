# Docker Setup Guide

Quick reference for running Media Request Bot with Docker.

## Quick Start

```bash
# 1. Create config file
cp config.example.json config.json
# Edit config.json with your settings

# 2. Start the bot
docker-compose up -d

# 3. Check logs
docker-compose logs -f
```

## Docker Compose Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start bot in background |
| `docker-compose down` | Stop and remove bot |
| `docker-compose restart` | Restart the bot |
| `docker-compose logs -f` | View live logs |
| `docker-compose build` | Rebuild image |
| `docker-compose ps` | Check status |

## Configuration

1. Edit `config.json` with your settings:
   - Telegram bot token
   - Sonarr URL and API key
   - Radarr URL and API key
   - Quality profile IDs
   - Root folder paths

2. The config file is mounted into the container as read-only

## Networking

The default `docker-compose.yml` uses `network_mode: host` which means:
- ✅ Easy access to Sonarr/Radarr on localhost
- ✅ No port mapping needed
- ⚠️ Container shares host network

### Alternative: Custom Docker Network

If Sonarr/Radarr are in Docker containers, modify `docker-compose.yml`:

```yaml
version: '3.8'

services:
  media-request-bot:
    build: .
    container_name: media-request-bot
    restart: unless-stopped
    volumes:
      - ./config.json:/app/config.json:ro
      - ./logs:/app/logs
    networks:
      - media-network
    environment:
      - TZ=America/New_York

networks:
  media-network:
    external: true
```

Then update config.json URLs to use container names:
```json
{
  "sonarr": {
    "url": "http://sonarr:8989",
    ...
  },
  "radarr": {
    "url": "http://radarr:7878",
    ...
  }
}
```

## Logs

Logs are stored in `./logs/media-request-bot.log`

**View logs:**
```bash
# Docker logs
docker-compose logs -f

# Or view log file directly
tail -f logs/media-request-bot.log
```

## Updating

```bash
# Pull latest code (if using git)
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## Troubleshooting

### Bot won't start

**Check logs:**
```bash
docker-compose logs
```

**Common issues:**
- Missing or invalid config.json
- Wrong API keys
- Can't reach Sonarr/Radarr (check URLs)

### Can't connect to Sonarr/Radarr

**If using host network:**
- URLs should be `http://localhost:8989` and `http://localhost:7878`
- Make sure Sonarr/Radarr are running
- Check firewall settings

**If using custom network:**
- URLs should use container names (e.g., `http://sonarr:8989`)
- Make sure all containers are on the same network

### Permission issues

**Logs directory:**
```bash
chmod 755 logs
```

**Config file:**
```bash
chmod 644 config.json
```

## Environment Variables

You can customize the timezone in `docker-compose.yml`:

```yaml
environment:
  - TZ=America/Los_Angeles  # Change to your timezone
```

Common timezones:
- `America/New_York`
- `America/Chicago`
- `America/Denver`
- `America/Los_Angeles`
- `Europe/London`
- `Europe/Paris`
- `Asia/Tokyo`

## Resource Limits

To limit resources, add to `docker-compose.yml`:

```yaml
services:
  media-request-bot:
    # ... other settings ...
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          memory: 128M
```

## Health Check

Add a health check to `docker-compose.yml`:

```yaml
services:
  media-request-bot:
    # ... other settings ...
    healthcheck:
      test: ["CMD", "python3", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Backup

**Backup important files:**
```bash
# Backup config
cp config.json config.json.backup

# Backup logs (optional)
tar -czf logs-backup.tar.gz logs/
```

## Security

- Config file is mounted as read-only (`:ro`)
- Never commit `config.json` to version control
- Keep API keys secure
- Consider using Docker secrets for production

## Manual Docker Commands

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

**Stop:**
```bash
docker stop media-request-bot
```

**Remove:**
```bash
docker rm media-request-bot
```

**View logs:**
```bash
docker logs -f media-request-bot
```

**Execute shell in container:**
```bash
docker exec -it media-request-bot /bin/bash
```

## Production Deployment

For production, consider:

1. **Using a proper logging driver:**
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

2. **Setting resource limits** (see above)

3. **Using Docker secrets** for sensitive data

4. **Setting up monitoring** (Prometheus, Grafana, etc.)

5. **Regular backups** of config.json

6. **Auto-restart policy:** `restart: unless-stopped` (already configured)
