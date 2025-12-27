from src.dependency_management import (
    VirtualEnvironmentManager,
    DependencyManager,
)


def test_available_versions():
    manager = VirtualEnvironmentManager()
    assert manager.available_versions()
    assert manager.default_python_version() in manager.available_versions()


def test_dependency_resolution():
    dep = DependencyManager()
    result = dep.resolve(["core", "dev"])
    assert "requests" in result
    assert "pytest" in result
