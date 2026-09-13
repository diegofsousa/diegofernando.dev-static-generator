PY?=python3
PELICAN?=pelican
PELICANOPTS=
# Pins the pagefind CLI version so local builds and CI index with the same
# engine. Search UI in the theme talks to whatever /pagefind/pagefind.js
# this writes, so bumping this may require checking their JS API changelog.
PAGEFIND?=npx --yes pagefind@1.5.2

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py


DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make ssh_upload                     upload the web site via SSH        '
	@echo '   make rsync_upload                   upload the web site via rsync+ssh  '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

html:
	$(PELICAN) "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
	$(PAGEFIND) --site "$(OUTPUTDIR)"

clean:
	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

# Note: -r keeps regenerating on file changes but only runs pagefind once,
# up front. The search index will go stale as you edit; run `make html`
# again (or restart) when you need it to catch up.
regenerate:
	$(PELICAN) -r "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

# Builds once, indexes, then serves with a plain static server (pelican's
# own `-l` serves the same process that generates, so there's no point to
# hook pagefind into between the two).
serve: html
ifdef PORT
	cd "$(OUTPUTDIR)" && $(PY) -m http.server $(PORT)
else
	cd "$(OUTPUTDIR)" && $(PY) -m http.server 8000
endif

serve-global: html
ifdef SERVER
	cd "$(OUTPUTDIR)" && $(PY) -m http.server $(PORT) --bind $(SERVER)
else
	cd "$(OUTPUTDIR)" && $(PY) -m http.server $(PORT) --bind 0.0.0.0
endif

# See the note on `regenerate` above: search index reflects the last
# `make html`, not every autoreload cycle.
devserver:
ifdef PORT
	$(PELICAN) -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -p $(PORT)
else
	$(PELICAN) -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)
endif

publish:
	$(PELICAN) "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)
	$(PAGEFIND) --site "$(OUTPUTDIR)"


.PHONY: html help clean regenerate serve serve-global devserver publish 