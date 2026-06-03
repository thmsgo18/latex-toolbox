from __future__ import annotations

from pathlib import Path

import pytest

import latex_forge.config as config_module


def test_no_config_file_returns_none_template(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "_CONFIG_PATH", tmp_path / ".latex-forge.toml")
    assert config_module.get_default_template() is None


def test_default_template_read_from_config(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    config_file.write_text('default_template = "rapport-projet-fr"\n', encoding="utf-8")
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    assert config_module.get_default_template() == "rapport-projet-fr"


def test_no_config_file_returns_none_output_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "_CONFIG_PATH", tmp_path / ".latex-forge.toml")
    assert config_module.get_default_output_dir() is None


def test_default_output_dir_valid(tmp_path, monkeypatch):
    output_dir = tmp_path / "projects"
    output_dir.mkdir()
    config_file = tmp_path / ".latex-forge.toml"
    config_file.write_text(
        f'default_output_dir = "{output_dir.as_posix()}"\n', encoding="utf-8"
    )
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    assert config_module.get_default_output_dir() == output_dir


def test_default_output_dir_nonexistent_dir(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    config_file.write_text(
        'default_output_dir = "/nonexistent/path/that/does/not/exist"\n', encoding="utf-8"
    )
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    assert config_module.get_default_output_dir() is None


def test_malformed_config_returns_none(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    config_file.write_text("not valid toml ][[\n", encoding="utf-8")
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    assert config_module.get_default_template() is None
    assert config_module.get_default_output_dir() is None


def test_empty_template_string_returns_none(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    config_file.write_text('default_template = ""\n', encoding="utf-8")
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    assert config_module.get_default_template() is None


# --- profile ---


def test_get_profile_no_config(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "_CONFIG_PATH", tmp_path / ".latex-forge.toml")
    assert config_module.get_profile() == {}


def test_save_and_get_profile_roundtrip(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    profile = {
        "name": "Thomas Gourmelen",
        "university": "Université de Bordeaux",
        "program": "Master Informatique",
        "github": "thmsgo18",
    }
    config_module.save_profile(profile)
    assert config_module.get_profile() == profile


def test_save_profile_preserves_other_keys(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    config_file.write_text('default_template = "rapport-projet-fr"\n', encoding="utf-8")
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    config_module.save_profile({"name": "Alice"})
    assert config_module.get_default_template() == "rapport-projet-fr"
    assert config_module.get_profile().get("name") == "Alice"


def test_save_profile_replaces_existing_profile(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    config_module.save_profile({"name": "Alice", "github": "alice"})
    config_module.save_profile({"name": "Bob"})
    profile = config_module.get_profile()
    assert profile.get("name") == "Bob"
    assert "github" not in profile  # old field gone


def test_save_profile_skips_empty_values(tmp_path, monkeypatch):
    config_file = tmp_path / ".latex-forge.toml"
    monkeypatch.setattr(config_module, "_CONFIG_PATH", config_file)
    config_module.save_profile({"name": "Alice", "github": ""})
    profile = config_module.get_profile()
    assert "name" in profile
    assert "github" not in profile
