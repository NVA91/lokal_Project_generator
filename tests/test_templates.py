from src.template_base import SmartHomeTemplate, AutomationTemplate, GameDevTemplate


def test_smart_home_template():
    t = SmartHomeTemplate()
    assert t.get_name() == "Smart Home Controller"
    structure = t.get_structure()
    assert "docs" in structure and "hardware" in structure["docs"]
    meta = t.get_metadata()
    assert "wled" in meta.get("dependencies", [])


def test_automation_template():
    t = AutomationTemplate()
    assert t.get_name() == "CI/CD Automation"
    structure = t.get_structure()
    assert ".github" in structure
    meta = t.get_metadata()
    assert "docker" in meta.get("dependencies", [])


def test_game_dev_template():
    t = GameDevTemplate()
    assert t.get_name() == "Flutter Card Game"
    assert "lib" in t.get_structure()
    meta = t.get_metadata()
    assert "flutter" in meta.get("dependencies", [])
