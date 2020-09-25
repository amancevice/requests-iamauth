SDIST := dist/$(shell python setup.py --fullname).tar.gz

$(SDIST): test
	python setup.py sdist

.PHONY: all clean test up upload

all: $(SDIST)

clean:
	rm -rf dist

test:
	py.test

upload: $(SDIST)
	twine upload $<
