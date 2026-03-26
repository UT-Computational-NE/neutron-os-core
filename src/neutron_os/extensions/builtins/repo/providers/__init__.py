"""Auto-import all repo sensing providers."""

from neutron_os.extensions.builtins.repo.providers import (
    github,  # noqa: F401
    gitlab,  # noqa: F401
)
