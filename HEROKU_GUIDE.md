# Heroku Deployment Guide

This guide will help you deploy your BioLink Protector Bot to Heroku.

## Prerequisites

1. A Heroku account (Create one at [Heroku](https://heroku.com) if you don't have one)
2. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
3. [Git](https://git-scm.com/downloads) installed

## Steps to Deploy

### 1. Login to Heroku CLI

```bash
heroku login
```

### 2. Create a new Heroku app

```bash
heroku create your-app-name
```

### 3. Add Heroku Remote

```bash
git init
heroku git:remote -a your-app-name
```

### 4. Configure Environment Variables

Go to your Heroku app dashboard → Settings → Config Vars, and add the following:

- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API Hash
- `BOT_TOKEN`: Your Telegram Bot Token
- `MONGO_URI`: Your MongoDB Connection URI

### 5. Deploy to Heroku

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

### 6. Scale Worker Dyno

```bash
heroku ps:scale worker=1
```

### 7. Check Logs

```bash
heroku logs --tail
```

## Local Development

For local development, create a `.env` file in the root directory with the following content:

```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MONGO_URI=your_mongo_uri
```

Then run:

```
python bio.py
```

## Need Help?

If you face any issues during deployment, please contact @itsSmartDev on Telegram.
