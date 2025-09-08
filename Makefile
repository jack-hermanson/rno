.PHONY: pull-macros update-macros push-macros

# Initialize and pull submodule (used on production or first-time setup)
pull-macros:
	git submodule init
	git submodule update --remote --merge

# Pull updates and commit if there are changes, or error if nothing to commit
update-macros:
	git submodule update --remote --merge
	if git diff --quiet --exit-code application/web/templates/_macros; then \
		echo "No changes to commit in shared macros. Aborting."; \
		exit 1; \
	else \
		git add application/web/templates/_macros; \
		git commit -m "Update macros to latest commit"; \
	fi

# Push the submodule itself (used when you actually edited macros)
push-macros:
	cd application/web/templates/_macros && git push origin main