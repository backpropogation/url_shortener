# url_shortener
- `pip install 'fabric<2.0'`
- `docker-compose build`
- `docker-compose up -d db` 
- Wait untill mysql ups
- `docker-compose up -d`
- In other window:
- `fab migrate`
- Navigate to `http://0.0.0.0/api/`
###Run tests
- While server container is up: `fab test`