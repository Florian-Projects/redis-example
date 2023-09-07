build:
	cd ./backend/; make build
	cd ./frontend/; pnpm run docker

deploy:
	helm upgrade --install --namespace redis-example --set replica.replicaCount=0 --set master.persistence.enabled=false --set auth.enabled=false redis oci://registry-1.docker.io/bitnamicharts/redis

	kubectl apply -k ./kubernetes/