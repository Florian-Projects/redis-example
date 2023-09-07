build:
	cd ./backend/; make build
	cd ./frontend/; pnpm run docker

deploy:
	kubectl apply -k ./kubernetes/