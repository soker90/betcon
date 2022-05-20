# Betcon

[![license](https://img.shields.io/github/license/soker90/betcon.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![GitHub release](https://img.shields.io/github/release/soker90/betcon.svg)](https://github.com/soker90/betcon/releases) [![Github All Releases](https://img.shields.io/github/downloads/soker90/betcon/total.svg)](https://github.com/soker90/betcon/releases/) [![AUR](https://img.shields.io/aur/version/betcon.svg)](https://aur.archlinux.org/packages/betcon) [![Launchpad](https://img.shields.io/badge/PPA%20soker%2Fbetcon-v1.7.7.1--1-yellow.svg)](https://launchpad.net/~soker/+archive/ubuntu/betcon)
[![Inactively Maintained](https://img.shields.io/badge/Maintenance%20Level-Inactively%20Maintained-yellowgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

Betcon es una aplicación para sistemas GNU/Linux, Windows y MAC para la gestión de apuestas deportivas. Betcon tiene licencia GPLv3.

### Descargas

#### ArchLinux
```bash
yaourt -S betcon
```
#### Ubuntu
```
sudo add-apt-repository ppa:soker/betcon
sudo apt-get update
sudo apt-get install betcon
```
#### Debian
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys FA4746D8
sudo bash -c "echo 'deb http://ppa.launchpad.net/soker/betcon/ubuntu xenial main #Betcon' >> /etc/apt/sources.list"
sudo apt-get update
sudo apt-get install betcon
```

#### Instalar desde código fuente
Antes de instalar, asegúrate de tener instaladas las dependencias:
* Python
* PyQt5
* SQLite3
* [Pyexcel-ods]('https://github.com/pyexcel/pyexcel-ods')
* PyYAML
* Pillow

Para instalar:
```
make install
```

#### Código fuente

```
git clone https://github.com/soker90/Betcon.git
```

#### MAC y Windows
[Descarga](https://github.com/soker90/betcon/releases)

### Desarollo
Para instalar las dependencias:
```
make install-dependencies
```
Para ejecutar la aplicación:
```
make start
```
### Tests
Para ejecutar los tests:
```
nosetests tests/
```
### Contacto
Puedes contactarme en [eduparra90@gmail.com](mailto:eduparra90@gmail.com).


Mas información en [https://soker90.github.io/betcon/](https://soker90.github.io/betcon/)
