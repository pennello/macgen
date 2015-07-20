.PHONY: test install uninstall clean

DESTDIR = /usr/local

name = macgen
bin = $(name)
zip = $(name).zip

# For cleaning up after test runs.
pyc_all = $(patsubst %.py, %.pyc, $(shell find src test -name '*.py'))

# Only these will be built by the bin target.
pyo_src = $(patsubst %.py, %.pyo, $(shell find src -name '*.py'))

# pyo_all is for robust test cleanup.  See the clean target.
pyo_all = $(patsubst %.py, %.pyo, $(shell find src test -name '*.py'))

$(bin): src/header $(zip)
	cat $^ > $@
	chmod +x $@

$(zip): $(pyo_src)
	rm -f $@
	cd src && echo $(patsubst src/%, %, $^) | xargs zip -9 ../$@

%.pyo: %.py
	python -OOm py_compile $^

test:
	PYTHONPATH=src python -m unittest discover -v -s test

clean:
# Remove pyo_all since user could have run PYTHONOPTIMIZE=1 make test.
	rm -f $(bin) $(zip) $(pyc_all) $(pyo_all)

install:
	install $(bin) $(DESTDIR)/bin/$(bin)

uninstall:
	rm $(DESTDIR)/bin/$(bin)
