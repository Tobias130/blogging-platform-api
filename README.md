
# Blogging Platform API 

This is a project from Roadmap, see the link. The project is about a REST API.

https://roadmap.sh/projects/blogging-platform-api
## Run Locally

Clone the project

```bash
  git clone https://github.com/Tobias130/blogging-platform-api.git
```

Go to the project directory

```bash
  cd Blogging-Platform-API
```

Install virtualenv (.venv)

```bash
  pip install virtualenv
```

Install dependencies
```bash
  install -r requirements.txt
```

Start the server

```bash
  py .\main.py
```


## API Reference

#### Get all items

```http
  GET /posts/
```

#### Post item

```http
  POST /posts/
```

#### Get one specific item

```http
  GET /posts/<int:id>
```

#### Update item

```http
  PUT /posts/<int:id>
```

#### Delete item

```http
  DELETE /posts/<int:id>
```

#### Filter item

```http
  /posts?term=<title|content|category>
```
