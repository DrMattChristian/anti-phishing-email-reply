PREFIX = /usr/local
PERL_SCRIPTS = add-address-to-list.pl addresses2bindzone.pl addresses2sendmailaccess.pl \
feed_barracuda_phish.pl find_phishing_replies_in_sendmail_logs.pl find_phishing_replies.pl
PYTHON_SCRIPTS = addresses2postfixmap.py addresses2postfixmap_trap.py
SHELL_SCRIPTS = sa-phish-gen
.PHONY: all
all: check

# Run one or more Python syntax checkers on scripts
# Comment out any that you don't have installed
check:
	$(foreach script,$(SHELL_SCRIPTS),bash -n $(script))
	$(foreach perlsc,${PERL_SCRIPTS},perl -cW $(perlsc))
	flake8 $(PYTHON_SCRIPTS)
	pep8 $(PYTHON_SCRIPTS)
	pyflakes $(PYTHON_SCRIPTS)
	pylint $(PYTHON_SCRIPTS)
	pylint-3.4 $(PYTHON_SCRIPTS)

# Remove Python compiled file
clean:
	rm -fv $(PYTHON_SCRIPTS)c

# Compile Python scripts
compile:
	python -m py_compile $(PYTHON_SCRIPTS)

# TODO: What to do with pyc Python compiled file
install:
	install $(PYTHON_SCRIPTS) $(PREFIX)/bin
	install $(SHELL_SCRIPTS) $(PREFIX)/bin

