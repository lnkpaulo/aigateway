
### STREAM= False

```
curl -v -X 'POST' \
  'http://localhost:8000/generate' \
  -H 'Authorization: Bearer your_secret_token' \
  -H 'Content-Type: application/json' \
  -d "{\"model\":\"llama3.1\",\"prompt\":\"Why is the sky blue?\"}"
```

### STREAM= True

```
curl -v -X 'POST' \
  'http://localhost:8000/generate' \
  -H 'Authorization: Bearer your_secret_token' \
  -H 'Content-Type: application/json' \
  -d "{\"model\":\"llama3.1\",\"prompt\":\"Why is the sky blue?\",\"stream\":true}"
```