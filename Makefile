all:
	python setup.py build

.PHONY: dist
dist:
	python ./setup.py sdist upload
	python ./setup.py bdist_wheel upload

.PHONY: clean
clean:
	rm -fr build dist pkgs.egg-info timerfd/__pycache__ timerfd.egg-info
	rm -f timerfd/*.o
	rm -fr .venv/lib/python*/site-packages/timerfd*
	rm -fr *egg-info

.PHONY: register
register:
	python ./setup.py register

.PHONY: install
install:
	python ./setup.py install

.PHONY: test
test:
	cd test; ./test.py

.PHONY: buildwait
buildwait:
	-while inotifywait --even modify --recursive timerfd test; do \
		$(MAKE) clean install test; \
	done;
