all:
	cd src && python main.py
	
clean:
	rm -rf src/__pycache__
	rm -rf src/lib/__pycache__
