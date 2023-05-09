# supermarket-offer-scanner

# What is this?

Simple project to scan the **upcoming** special offers of supermarkets.
You can run this as a command line project or by cron inside a docker container.

# How to use it with docker-compose?

```yml
services:
  supermarket-offer-scanner:
    image: ghcr.io/entepotenz/supermarket-offer-scanner:latest
    restart: unless-stopped
    environment:
      TZ: "Europe/London"
      PUID: "$PUID"
      PGID: "$PGID"
      PUSHOVER_USER_KEY: "$PUSHOVER_USER_KEY"
      PUSHOVER_TOKEN: "$PUSHOVER_TOKEN"
    volumes:
      - ./Docker/docker-cron/crontab-sample.txt:/config/crontab.txt
```

# How to build the docker container yourself?

Please take a look at those two folders:

- `Docker/docker-cron/`
    - run this command: `docker-compose up`
- `Docker/docker-one-shot/`
    - run the script (**warning** it is build in a way which makes sure the image is rebuild each time)
        - `Docker/docker-one-shot/build-and-run-and-remove-docker.sh`