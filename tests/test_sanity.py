from pathlib import Path


def test_repo_layout_has_deploy_helpers():
    assert Path('scripts/install_deps.sh').exists()
    assert Path('scripts/deploy_gcp.sh').exists()


def test_install_script_has_windows_fallback_launcher():
    script = Path("scripts/install_deps.sh").read_text()
    assert "command -v python" in script
    assert "command -v py" in script
