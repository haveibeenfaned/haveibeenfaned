# Have I been faned

Inspired by have I been pwned, this is the first public record of people that have Onlyfans or Fansly.

### Provided features:

- Lookup for supported link providers
- Lookup for content providers in link providers
- Lookup for URLs, though this option will not persist the username + the content

### Link providers supported:

- Lnktr.ee
- Beacons.ai
- AllMyLinks
- Lnk.bio
- None (plain account parsing)

### Content providers supported:

- OnlyFans
- Fansly

### Features we want to provide:

- Relations between deleted / removed / old profiles and new ones (via waybackmachine)
- Support for plain usernames (will be searched on all socials then, x (twitter), ig, facebook, threads)
- Support for looking up x(twitter), facebook and threads

## Persistance to the hall of shame

## Blockers

- Figure out a way for selenium to run on servers (akash / gpu based vm maybe?)

## Setup

- Copy your Chrome profiles path as an argument to the rasp
- Use the new folder path as an argument option in WebDriver
- Initialise driver and save login in IG
- Start up the crawler

- API needs an API key which can be set up with a SECRET in fly.io
- Postgresql needs to be active for messages to go through

## To research / improve 

- Sometimes beacons.ai hides the link very well, there is an extra reguex for it but the link will not be returned!

## Testing
![Alt Text](https://tenor.com/th/view/are-you-serious-spiderman-meme-laugh-laughing-gif-7178438.gif)

## Deploying with nuxt
From root
```shell
cd web
npm run generate
cd ..
fly deploy
```

## Dev servers
API - From root
```shell
fastapi dev
```

Front end - From root
```shell
cd web
npm run dev
```

Crawler - From root (with orchestrator)
```shell
PYTHONPATH=./ ./src/main.py
```

Make sure to spin up a database and do the corresponding migrations
```shell
docker run -d -p 5432:5432 --name hbif-postgres -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=postgres --volume hbif-postgres-volume:{project_path}.docker/ postgres:17.5-alpine3.22 
```
