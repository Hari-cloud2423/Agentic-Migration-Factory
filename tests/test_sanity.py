from pathlib import Path


def test_repo_layout_has_deploy_helpers():
    assert Path('scripts/install_deps.sh').exists()
    assert Path('scripts/deploy_gcp.sh').exists()
