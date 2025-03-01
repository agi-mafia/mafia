```
docker build -t app .
docker run --env-file ./.env -p 8000:8000 app
```