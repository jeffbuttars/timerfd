all:
	python setup.py build

.PHONY: clean
clean:
	rm -fr build
	rm -f timerfd/*.o
