# Holiday dates generator and API

Holiday date generator for initially Finnish holiday dates, later for the whole Europe (or even the world? PR's are welcome!). Gives out JSON or CSV, and has an API functionality available for you to set it up.

## Just need the API? You've got it!

The API is running at https://holidays.hr-bot.eu and is updated regularly. Feel free to use!

# Development

```
git pull git@github.com:hrbotfi/holidaygen.git
docker-compose up
open http://localhost:5000/holidays/
```

When run with Docker-compose, the application will automatically reload every 3 seconds if it detects changes. If you've save a version that will cause a crash, just kill the Docker container with Ctrl+C and start it again with `docker-compose up`. If you've changed dependencies, re-create the container when starting up with `docker-compose up --build`.
