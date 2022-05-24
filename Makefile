# Variables -------------------------------------------------------------------

TESTIMONY_OPTIONS=--config testimony.yaml

# Commands --------------------------------------------------------------------

help:
	@echo "  uuid-check                 to check for duplicated or empty :id: in testimony docstring tags"
	@echo "  uuid-fix                   to fix all duplicated or empty :id: in testimony docstring tags"

test-docstrings: uuid-check
	$(info "Checking for errors in docstrings and testimony tags...")
	testimony $(TESTIMONY_OPTIONS) validate tests/

uuid-check:  ## list duplicated or empty uuids
	$(info "Checking for empty or duplicated @id: in docstrings...")
	@scripts/fix_uuids.sh --check

uuid-fix:
	@scripts/fix_uuids.sh

vault-login:
	@scripts/vault_login.py --login

vault-status:
	@scripts/vault_login.py --status

vault-logout:
	@scripts/vault_login.py --logout

.PHONY: help test-docstrings uuid-check
