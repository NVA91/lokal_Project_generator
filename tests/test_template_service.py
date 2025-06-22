from pathlib import Path
import pytest

from src.template_service import TemplateService


def test_structure(tmp_path):
    template_dir = tmp_path / "templates"
    (template_dir / "foo" / "sub").mkdir(parents=True)
    (template_dir / "foo" / "sub" / "file.txt").write_text("data")

    service = TemplateService(template_dir)
    structure = service.get_template_structure("foo")
    assert "foo" in structure
    assert "sub" in structure["foo"]
    assert "file.txt" in structure["foo"]["sub"]


def test_import(tmp_path):
    templates_dir = tmp_path / "templates"
    service = TemplateService(templates_dir)

    src = tmp_path / "src_template"
    (src / "a").mkdir(parents=True)
    (src / "a" / "b.txt").write_text("x")

    dest = service.import_template(src)
    assert dest.exists()
    assert (dest / "a" / "b.txt").read_text() == "x"

    with pytest.raises(FileExistsError):
        service.import_template(src)

    with pytest.raises(ValueError):
        service.import_template(tmp_path / "not_a_dir.txt")


def test_list_templates_sorted(tmp_path):
    templates_dir = tmp_path / "templates"
    (templates_dir / "b").mkdir(parents=True)
    (templates_dir / "a").mkdir(parents=True)
    service = TemplateService(templates_dir)
    assert service.list_templates() == ["a", "b"]
