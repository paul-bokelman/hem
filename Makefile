.PHONY: run-server-dev run-web-dev install-server install-web dev clean

# run server in dev mode
run-server-dev:
	cd server && source venv/bin/activate && venv/bin/python3.12 main.py --dev

run-server:
	cd server && source venv/bin/activate && venv/bin/python3.12 main.py

# run web in dev mode
run-web-dev:
	cd web && npm run dev

# run web in production mode
run-web:
	cd web && npm run build && npm start

# install server dependencies
install-server:
	cd server && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# install web dependencies
install-web:
	cd web && npm install

# start both server and web in dev mode
dev:
	make -j 2 run-server-dev run-web-dev

# start both server and web in production mode
prod:
	make -j 2 run-server run-web

# clean all build artifacts
clean:
	rm -rf server/__pycache__ server/venv web/node_modules
