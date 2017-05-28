
serve: .simsearch-installed .models-created
	env/bin/python setup.py develop
	env/bin/python simsearch.py

env: requirements.txt
	test -d env || virtualenv -p python2.7 env
	env/bin/pip install -r requirements.txt
	touch env

env/bin/cython: env

.simsearch-installed: simsearch/stroke.c
	env/bin/python setup.py develop
	touch $@

.models-created: .simsearch-installed
	env/bin/python -m simsearch.models
	touch $@

simsearch/stroke.c: simsearch/stroke.pyx env/bin/cython
	env/bin/cython $<

clean:
	rm -rf env build .simsearch-installed .models-created simsearch.egg-info
