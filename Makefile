up-d:
	@docker-compose up -d
	@flask run

down:
	@docker-compose down

logs:
	@docker-compose logs