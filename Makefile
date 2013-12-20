NOSETESTS ?= nosetests

.PHONY: nosetests nosetests.coverage test flake8

test: nosetests flake8
test.coverage: nosetests.coverage flake8

nosetests:
	@$(NOSETESTS) --with-doctest

nosetests.coverage:
	@$(NOSETESTS) --with-xcoverage --cover-tests --with-doctest

flake8:
	@flake8 *.py twitters utilities web2email

clean:
	@rm -rf .coverage
	@rm -rf coverage.xml
