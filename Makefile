A_VERSION=$(shell cat ./VERSION) 

all: caja nautilus nemo

caja: prepare-caja
	@echo Building Caja extension ${A_VERSION}
	dpkg-deb -b ./src/caja $(shell echo "./build/caja-video-columns-${A_VERSION}" | tr -d '[:space:]').deb

nautilus: prepare-nautilus
	@echo Building Nautilus extension ${A_VERSION}
	dpkg-deb -b ./src/nautilus $(shell echo "./build/nautilus-video-columns-${A_VERSION}" | tr -d '[:space:]').deb

nemo: prepare-nemo
	@echo Building Nemo extension ${A_VERSION}
	dpkg-deb -b ./src/nemo $(shell echo "./build/nemo-video-columns-${A_VERSION}" | tr -d '[:space:]').deb

prepare-caja:
	sed 's/VERSION_ID/${A_VERSION}/' ./src/base/DEBIAN/control.caja > ./src/caja/DEBIAN/control

prepare-nautilus:
	sed 's/VERSION_ID/${A_VERSION}/' ./src/base/DEBIAN/control.nautilus > ./src/nautilus/DEBIAN/control

prepare-nemo:
	sed 's/VERSION_ID/${A_VERSION}/' ./src/base/DEBIAN/control.nemo > ./src/nemo/DEBIAN/control

clean:
	rm ./build/*.deb

