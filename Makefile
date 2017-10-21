#==================
# Macros
#==================

pardir = $(patsubst %/,%,$(dir $(abspath $(1))))


#==================
# Helper Constants
#==================

THIS := $(abspath $(lastword $(MAKEFILE_LIST)))
HERE := $(call pardir,$(THIS))
DRAW := $(HERE)/draw_party


#==================
# Targets
#==================

.PHONY: clean
clean:
	cd $(DRAW)/client && npm run clean
	git clean -dffx -- $(DRAW)/client/node_modules

.PHONY: deps
deps:
	pip install -q -r requirements_dev.txt
	cd $(DRAW)/client && npm install

.PHONY: js-build
js-build: deps
	cd $(DRAW)/client && npm run build

.PHONY: js-watch
js-watch: deps
	cd $(DRAW)/client && npm run watch

.PHONY: serve
serve: deps js-build
	gunicorn --log-file=- --access-logfile=- app:app

.PHONY: test
test: test-python

.PHONY: test-python
test-python: deps
	cd $(DRAW) && flake8 .
	cd $(DRAW) && coverage erase && nosetests --with-coverage .
	@cd $(DRAW) && coverage xml -o $(HERE)/test-reports/coverage_draw.xml
	@cd $(DRAW) && coverage report -m --fail-under=100
