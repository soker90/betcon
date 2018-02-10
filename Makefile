all: install

install:
	mkdir -p /usr/share/betcon/default/
	mkdir -p /usr/share/betcon/resources/
	cp -r src /usr/share/betcon/
	cp -r ui /usr/share/betcon/
	cp -r resources/bookies /usr/share/betcon/resources/
	cp -r resources/sports /usr/share/betcon/resources/
	cp -r lang/mo/* /usr/share/locale/
	cp default/database.sql /usr/share/betcon/default/
	cp resources/betcon.desktop /usr/share/applications/
	cp resources/icon.png /usr/share/pixmaps/betcon.png
	cp resources/betcon /usr/bin/
	chmod +x /usr/bin/betcon

uninstall:
	rm -rf /usr/share/betcon/
	rm /usr/share/applications/betcon.desktop
	rm /usr/share/pixmaps/betcon.png
	rm /usr/bin/betcon

test:
	nosetests test

clean:
	rm -rf src/__pycache__
	rm -rf src/lib/__pycache__
