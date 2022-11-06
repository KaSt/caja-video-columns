A_VERSION=$(shell grep 'Version' ./src/caja/DEBIAN/control | cut -d ":"  -f 2) 

all: caja nautilus nemo

caja:
	@echo Building Caja extension ${A_VERSION}
	dpkg-deb -b ./src/caja $(shell echo "./build/caja-video-columns-${A_VERSION}" | tr -d '[:space:]').deb

nautilus:
	@echo Building Nautilus extension ${A_VERSION}
	dpkg-deb -b ./src/nautilus $(shell echo "./build/nautilus-video-columns-${A_VERSION}" | tr -d '[:space:]').deb

nemo:
	@echo Building Nemo extension ${A_VERSION}
	dpkg-deb -b ./src/nemo $(shell echo "./build/nemo-video-columns-${A_VERSION}" | tr -d '[:space:]').deb

clean:
	rm ./build/*.deb

