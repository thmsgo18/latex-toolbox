"""User profile — read, write and apply personal information to projects."""
from __future__ import annotations

import re
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]


# ── Schema ────────────────────────────────────────────────────────────────

# (key, display_label, section)
PROFILE_SCHEMA: list[tuple[str, str, str]] = [
    ("first_name",  "First name",            "identity"),
    ("last_name",   "Last name",             "identity"),
    ("email",       "Email",                 "identity"),
    ("phone",       "Phone",                 "identity"),
    ("website",     "Website",               "identity"),
    ("github",      "GitHub username",       "online"),
    ("linkedin",    "LinkedIn username",     "online"),
    ("university",  "University",            "academic"),
    ("faculty",     "Faculty / UFR",         "academic"),
    ("program",     "Program / Formation",   "academic"),
    ("supervisor",  "Supervisor",            "academic"),
    ("company",     "Company",               "professional"),
    ("department",  "Department / Service",  "professional"),
    ("job_title",   "Job title",             "professional"),
]

SECTION_HEADERS: dict[str, str] = {
    "identity":     "Identity",
    "online":       "Online profiles",
    "academic":     "Academic",
    "professional": "Professional",
}


# ── File path ─────────────────────────────────────────────────────────────


def profile_path() -> Path:
    return Path.home() / ".latex-forge" / "profile.toml"


# ── Load / Save / Clear ───────────────────────────────────────────────────


def load_profile() -> dict[str, str]:
    """Return the stored profile as a flat dict. Returns {} if no file exists."""
    p = profile_path()
    if not p.exists():
        return {}
    with open(p, "rb") as fh:
        data = tomllib.load(fh)
    return {k: str(v) for k, v in data.items() if isinstance(v, str)}


def save_profile(values: dict[str, str]) -> None:
    """Persist *values* to the profile file with readable section comments."""
    p = profile_path()
    p.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    current_section: str | None = None

    for key, _label, section in PROFILE_SCHEMA:
        if section != current_section:
            if lines:
                lines.append("")
            header = SECTION_HEADERS[section]
            lines.append(f"# ── {header} " + "─" * (55 - len(header)))
            current_section = section
        value = values.get(key, "")
        lines.append(f'{key} = "{value}"')

    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def clear_profile() -> None:
    """Delete the profile file."""
    p = profile_path()
    if p.exists():
        p.unlink()


# ── Apply profile to a newly created project ──────────────────────────────


def apply_profile_to_project(
    target_dir: Path, template: str, profile: dict[str, str]
) -> None:
    """Substitute profile values into a newly created project.

    Targets only built-in templates whose file structure is known.
    Silent no-op for unknown templates or unset profile fields.
    """
    if not profile:
        return

    first = profile.get("first_name", "").strip()
    last  = profile.get("last_name",  "").strip()
    full_name = f"{first} {last}".strip()

    if template in ("cv-en", "cv-fr"):
        _apply_cv(target_dir, template, profile, full_name)
    elif template in ("project-report-en", "project-report-fr", "research", "blank"):
        _apply_metadata(target_dir, template, profile, full_name)
    # External / gallery templates: no-op — don't risk corrupting unknown files


# ── CV templates ──────────────────────────────────────────────────────────


def _apply_cv(
    target_dir: Path, template: str, profile: dict[str, str], full_name: str
) -> None:
    if template == "cv-en":
        heading_file  = target_dir / "sections" / "heading.tex"
        default_name  = "First LAST"
        default_phone = "+1 000.000.0000"
        default_li    = "first-last"
    else:
        heading_file  = target_dir / "sections" / "en-tete.tex"
        default_name  = "Prénom NOM"
        default_phone = "+33 6.00.00.00.00"
        default_li    = "prenom-nom"

    metadata_file = target_dir / "frontmatter" / "metadata.tex"

    # Built-in template format: personal info lives in the heading section file
    if heading_file.exists():
        content = heading_file.read_text(encoding="utf-8")

        if full_name:
            content = content.replace(default_name, full_name)
        if profile.get("phone"):
            content = content.replace(default_phone, profile["phone"])
        if profile.get("email"):
            content = content.replace("email@example.com", profile["email"])
        if profile.get("github"):
            g = profile["github"]
            content = content.replace(
                r"\href{https://github.com/username}{\texttt{username}}",
                r"\href{https://github.com/" + g + r"}{\texttt{" + g + "}}",
            )
        if profile.get("linkedin"):
            li = profile["linkedin"]
            content = content.replace(
                r"\href{https://www.linkedin.com/in/" + default_li + r"/}{\texttt{" + default_li + "}}",
                r"\href{https://www.linkedin.com/in/" + li + r"/}{\texttt{" + li + "}}",
            )

        heading_file.write_text(content, encoding="utf-8")

    # Gallery / installed template format: personal info in frontmatter/metadata.tex
    # via \newcommand{\cvname}{...}, \newcommand{\cvemail}{...} etc.
    if metadata_file.exists():
        content = metadata_file.read_text(encoding="utf-8")

        if full_name:
            content = _replace_newcmd(content, "cvname", full_name)
        if profile.get("phone"):
            content = _replace_newcmd(content, "cvphone", profile["phone"])
        if profile.get("email"):
            content = _replace_newcmd(content, "cvemail", profile["email"])
        if profile.get("github"):
            content = _replace_newcmd(content, "cvgithub", profile["github"])
        if profile.get("linkedin"):
            content = _replace_newcmd(content, "cvlinkedin", profile["linkedin"])

        metadata_file.write_text(content, encoding="utf-8")


# ── Report / blank templates ──────────────────────────────────────────────


def _apply_metadata(
    target_dir: Path, template: str, profile: dict[str, str], full_name: str
) -> None:
    metadata = target_dir / "frontmatter" / "metadata.tex"
    if not metadata.exists():
        return

    content = metadata.read_text(encoding="utf-8")

    if template == "blank":
        # \author{Author Name}
        if full_name:
            content = _replace_cmd(content, "author", full_name)
    else:
        # project-report-en/fr, research
        if profile.get("university"):
            content = _replace_newcmd(content, "universityname", profile["university"])
        if profile.get("program"):
            content = _replace_newcmd(content, "facultyname", profile["program"])

        first = profile.get("first_name", "").strip()
        last  = profile.get("last_name",  "").strip()
        if first or last:
            # Templates use "LASTNAME Firstname" / "NOM Prenom" convention
            author_arg = f"{last} {first}".strip()
            placeholder = "NOM Prenom" if template == "project-report-fr" else "LASTNAME Firstname"
            content = _replace_addauthor(content, placeholder, author_arg)

    metadata.write_text(content, encoding="utf-8")


# ── Regex helpers ─────────────────────────────────────────────────────────


def _replace_newcmd(content: str, cmd: str, value: str) -> str:
    r"""\\newcommand{\cmd}{OLD} → \\newcommand{\cmd}{value}."""
    pat = re.compile(r"(\\newcommand\{\\" + re.escape(cmd) + r"\}\{)[^}]*(\})")
    return pat.sub(lambda m: m.group(1) + value + m.group(2), content)


def _replace_cmd(content: str, cmd: str, value: str) -> str:
    r"""\\cmd{...} → \\cmd{value}. Applied only to non-commented lines."""
    pat = re.compile(r"(^\s*\\" + re.escape(cmd) + r"\{)[^}]*(\})", re.MULTILINE)
    return pat.sub(lambda m: m.group(1) + value + m.group(2), content)


def _replace_addauthor(content: str, placeholder: str, value: str) -> str:
    r"""Replace first \\addauthor{placeholder}{} → \\addauthor{value}{}."""
    pat = re.compile(r"(\\addauthor\{)" + re.escape(placeholder) + r"(\}\{)")
    return pat.sub(lambda m: m.group(1) + value + m.group(2), content, count=1)
