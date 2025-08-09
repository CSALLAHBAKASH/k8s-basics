

build:
	docker build -t myapp:latest .

run:
	docker run -d -p 8080:80 myapp:latest

stop:
	docker stop $(docker ps -q --filter ancestor=myapp:latest)