A_VERSION=$(shell grep 'Version' ./src/DEBIAN/control | cut -d ":"  -f 2) 

all:
	@echo Building ${A_VERSION}
	dpkg-deb -b ./src/ $(shell echo "./build/caja-video-columns-${A_VERSION}" | tr -d '[:space:]').deb

clean:
	rm ./build/*.deb

