run:
	docker-compose -f docker/docker-compose.yml up
build:
	docker-compose -f docker/docker-compose.yml build
qr:
	@echo "Wait for the QR..."
	@docker-compose -f src/WebWhatsapp-Wrapper/docker-compose.yml up -d
	@echo "Now copy the folder 'firefox_cache'"
web:
	docker exec -it web bash
mongo:
	docker exec -it mongo mongo admin -u root -p
bot:
	docker exec -it bot bash
create:
	# docker exec -it web python src/create.py data/emails/emails.test.csv
	docker exec -it web python src/create.py data/features/features_CA116_2019.json
	docker exec -it web python src/create.py data/predictions/predictions_CA116_2019_week_9.json
	docker exec -it web python src/create.py data/recommendations/recommendations_CA116_2019_week_9.json
send:
	docker exec -it web python src/send.py
down:
	docker-compose -f docker/docker-compose.yml down -v
reset:
	docker stop $(docker ps -q); docker rm $(docker ps -a -q)
prune:
	docker network prune -f; docker volume prune -f
kill:
	make down; make reset; make prune; make run
devel-bot:
	docker-compose -f docker/docker-compose.yml run bot bash
