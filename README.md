--[#]-- LINUX RUN --[#]--

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=flasky.py
export FLASK_DEBUG=1

flask db upgrade

flask run


--[?]-- Windows run command --[?]--
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

set FLASK_APP=flasky.py

set FLASK_DEBUG=1

flask db upgrade

flask run


Docker:
```
docker build -t physicshub -f Dockerfile .
```

```
docker run -d --restart unless-stopped -p 8086:5000 -v /root/DataBase/Physicshub:/app/db physicshub
```



### Nginx
```
sudo nano /etc/nginx/sites-available/fizikaonline.uz
```

```
server {
    listen 80;
    listen [::]:80;
    server_name fizikaonline.uz;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
        allow all;
    }

    location / {
        proxy_pass http://95.216.144.224:8086;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
```
sudo ln -s /etc/nginx/sites-available/fizikaonline.uz /etc/nginx/sites-enabled/
```
```
sudo nginx -t
```

```
sudo systemctl reload nginx
```

### SSL
```
sudo certbot --nginx -d fizikaonline.uz
```
