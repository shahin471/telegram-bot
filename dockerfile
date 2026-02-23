from python:3.14-slim
  workdir /app
  copy . /app
  run pip install --no-cach-dir -r
  requirements.txt
  cmd ['python','bot3.py]
