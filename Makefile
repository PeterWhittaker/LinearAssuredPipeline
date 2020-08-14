TOP := $(dir $(firstword $(MAKEFILE_LIST)))

# backwards, but given the problem below, I cannot figure different
PACKAGES := strictyaml yamale ruamel.yaml # ruamel has its own dependencies, see targets

######
# check for missing executables
#
# I would rather do this in a loop, but I could not figure out how to make it work
# Hopefully the number of executables required will stay low
WHICH := type -P	# as opposed to which
EXECMISSING := false
PIP	:= $(shell $(WHICH) pip)
PYTHON	:= $(shell $(WHICH) python)

ifndef PIP
$(info Missing pip)
EXECMISSING := true
endif

ifndef PYTHON
$(info Missing python)
EXECMISSING := true
endif
#
# end of check for missing executables - we check this in 'all'
######

#####
#
# start of targets
#
#####

all: yqcheck
ifeq ($(EXECMISSING),true)
	$(error Missing executables )
endif
	@$(TOP)/tests/runTests all

clean:
	@rm -f $(TOP)/tests/*schema.yaml

yqcheck:
	@$(TOP)/tests/yqCheck

check: checkBins checkPkgs

checkBins:
ifeq ($(EXECMISSING),true)
	$(error Missing executables )
endif
	@echo All binaries appear to be installed.

checkPkgs: checkBins
	$(info Checking for required and recommended packages)
	$(foreach package,$(PACKAGES), \
		$(info $(if $(shell $(PIP) show $(package) 2> /dev/null), \
			Package '$(package)' appears to be installed, \
			You will need to run 'pip install $(package)' or 'make $(package)')) \
	)
	@echo Package checks complete

ruamel.yaml: setuptools
	@$(PIP) install $(@)
	@$(PIP) install $(@).cmd

setuptools:
	@$(PIP) install -U setuptools wheel

strictyaml yamale:
	@$(PIP) install $@
