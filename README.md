--[#]-- LINUX RUN --[#]--

export FLASK_APP=flasky.py
export FLASK_DEBUG=1

flask db upgrade

flask run


--[?]-- Windows run command --[?]--
set FLASK_APP=flasky.py

set FLASK_DEBUG=1

flask db upgrade

flask run


Docker:
```
docker build -t mete-u2s -f Dockerfile .
```

```
docker run -d --restart unless-stopped -p 8082:1717 -v /root/DataBase:/app/instance mete-u2s
```
