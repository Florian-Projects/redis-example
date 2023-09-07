build:
	cd ./backend/; make build

deploy:
	kubectl apply -k ./kubernetes/