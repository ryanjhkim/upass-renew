# upass-renew

Designed to renew your upass for the month. 

## Currently only supports UBC students 
1. Edit Configuration
Directly edit the config.yaml file within the project directory.
Put your CWL id and password in place of `"ENTER_USERNAME"` and `"ENTER_PASSWORD"`

2. Build Docker Image
```
# /upass-renew/
docker build -t upass-renew.
```

3. Run Docker Image
```
# /upass-renew/
docker run it upass-renew python -m upass
```
