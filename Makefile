.PHONY: tests
tests :
	@echo "Running tests..."
	export PYTHONPATH=.  ;\
	echo $(PYTHONPATH) ;\
	pytest -v