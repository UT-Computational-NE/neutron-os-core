"""Lifecycle management for RAG connections.

Ensures PostgreSQL (pgvector) is running before RAG operations.
"""

from __future__ import annotations

import logging
import socket

log = logging.getLogger(__name__)


def ensure_postgresql_running() -> bool:
    """Silently ensure PostgreSQL is available via K3D cluster.

    Returns True if PostgreSQL is responding on localhost:5432.
    Attempts to start the K3D cluster if Docker is running but
    the cluster is stopped. Never prompts.
    """
    if _is_pg_serving():
        return True

    # Try to start the K3D cluster
    try:
        from neutron_os.setup.infra import check_docker, check_k3d, start_cluster, InfraStatus

        docker = check_docker()
        if docker.status != InfraStatus.READY:
            log.debug("Docker not running — cannot auto-start PostgreSQL")
            return False

        k3d = check_k3d()
        if k3d.status != InfraStatus.READY:
            log.debug("K3D not installed — cannot auto-start PostgreSQL")
            return False

        log.info("Auto-starting neut-local K3D cluster for PostgreSQL...")
        if start_cluster():
            # Wait for PostgreSQL to come up
            import time
            for _ in range(10):
                time.sleep(1)
                if _is_pg_serving():
                    log.info("PostgreSQL auto-started")
                    return True

        log.debug("K3D cluster started but PostgreSQL not responding")
        return False

    except ImportError:
        log.debug("infra module not available for auto-start")
        return False
    except Exception as e:
        log.debug("PostgreSQL auto-start failed: %s", e)
        return False


def _is_pg_serving(host: str = "localhost", port: int = 5432) -> bool:
    """Check if PostgreSQL is accepting connections."""
    try:
        sock = socket.create_connection((host, port), timeout=1)
        sock.close()
        return True
    except Exception:
        return False
