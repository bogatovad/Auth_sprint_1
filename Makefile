#make

start:
	docker-compose build && docker-compose build && docker-compose up -d

down:
	docker-compose down
