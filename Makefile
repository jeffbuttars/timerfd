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

.PHONY: register
register:
	python ./setup.py register
