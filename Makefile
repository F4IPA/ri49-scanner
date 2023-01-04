path=/opt

deploy:
	rsync -avh $(shell pwd) root@f5zrh.local:$(path) --exclude Makefile --exclude .git >/dev/null
	ssh root@f5zrh.local /opt/ri49-scanner/start.sh