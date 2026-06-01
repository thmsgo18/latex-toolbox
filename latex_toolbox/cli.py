from __future__ import annotations

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .project import (
    available_templates,
    create_project,
    rename_current_project,
    rename_project,
    validate_name,
)
from .setup import (
    is_first_run,
    mark_initialized,
    offer_open_vscode,
    run_first_launch_check,
    run_setup,
    warn_if_latex_missing,
)


def _get_version() -> str:
    try:
        return version("latex-toolbox")
    except PackageNotFoundError:
        return "unknown"


def _is_interactive() -> bool:
    try:
        return sys.stdin.isatty()
    except Exception:
        return False


def _ask_project_name() -> str:
    while True:
        try:
            name = input("Project name: ").strip()
        except (EOFError, OSError, KeyboardInterrupt):
            print("")
            sys.exit(1)
        try:
            validate_name(name)
            return name
        except ValueError as exc:
            print(str(exc))


def _select_template_interactively() -> str:
    templates = available_templates()
    print("Available templates:")
    for i, name in enumerate(templates, 1):
        print(f"  {i}. {name}")
    while True:
        try:
            answer = input(f"Choose a template [1-{len(templates)}]: ").strip()
            idx = int(answer) - 1
            if 0 <= idx < len(templates):
                return templates[idx]
        except (EOFError, OSError, KeyboardInterrupt):
            print("")
            sys.exit(1)
        except ValueError:
            pass
        print(f"Please enter a number between 1 and {len(templates)}.")


def _ask_output_dir() -> Path:
    default = Path.cwd()
    try:
        answer = input(f"Create project in [{default}]: ").strip()
    except (EOFError, OSError, KeyboardInterrupt):
        print("")
        sys.exit(1)
    if not answer:
        return default
    path = Path(answer).expanduser().resolve()
    if not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            print(f"Cannot create directory: {exc}", file=sys.stderr)
            sys.exit(1)
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="latex-toolbox",
        description="Utilities for generating standalone LaTeX projects from the toolbox.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {_get_version()}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser(
        "create",
        help="Create a new LaTeX project from a template.",
    )
    create_parser.add_argument(
        "--name",
        default=None,
        help="Name of the project (prompted interactively if omitted).",
    )
    create_parser.add_argument(
        "--template",
        default=None,
        help="Template name to use (prompted interactively if omitted).",
    )
    create_parser.add_argument(
        "--output",
        default=None,
        help="Directory where the project will be created (default: current directory).",
    )

    rename_parser = subparsers.add_parser(
        "rename",
        help="Rename a generated LaTeX project folder and its main .tex file.",
    )
    rename_parser.add_argument(
        "names",
        nargs="+",
        help="Use `old_name new_name` from the parent folder, or only `new_name` from inside the project folder.",
    )

    setup_parser = subparsers.add_parser(
        "setup",
        help="Install VS Code extensions when possible and check LaTeX prerequisites.",
    )
    setup_parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check the current environment without installing VS Code extensions.",
    )
    setup_parser.add_argument(
        "--skip-extensions",
        action="store_true",
        help="Skip VS Code extension installation.",
    )
    setup_parser.add_argument(
        "--install-tex",
        action="store_true",
        help="Try to install a LaTeX distribution with a common package manager for the current OS.",
    )

    subparsers.add_parser(
        "list-templates",
        help="List the available templates.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list-templates":
        for template_name in available_templates():
            print(template_name)
        return 0

    if args.command == "create":
        name = args.name
        template = args.template
        guided = False

        if name is None:
            if not _is_interactive():
                print("--name is required in non-interactive mode.", file=sys.stderr)
                return 1
            name = _ask_project_name()
            guided = True

        if template is None:
            if not _is_interactive():
                print("--template is required in non-interactive mode.", file=sys.stderr)
                return 1
            template = _select_template_interactively()
            guided = True

        if args.output is not None:
            output_dir = Path(args.output).resolve()
        elif guided:
            output_dir = _ask_output_dir()
        else:
            output_dir = Path.cwd()

        first_run = is_first_run()
        if first_run:
            run_first_launch_check()
            mark_initialized()

        try:
            target_dir, main_tex_file = create_project(
                name=name,
                template=template,
                output_dir=output_dir,
            )
        except (ValueError, FileExistsError) as exc:
            print(str(exc), file=sys.stderr)
            return 1

        print(f"Project created: {target_dir}")
        print(f"Edit: {main_tex_file.relative_to(target_dir.parent)}")
        print("Next: fill in frontmatter/metadata.tex then save to compile.")

        if not first_run:
            warn_if_latex_missing()

        offer_open_vscode(target_dir)

        return 0

    if args.command == "rename":
        try:
            if len(args.names) == 1:
                target_dir, main_tex_file = rename_current_project(
                    new_name=args.names[0],
                )
            elif len(args.names) == 2:
                target_dir, main_tex_file = rename_project(
                    old_name=args.names[0],
                    new_name=args.names[1],
                )
            else:
                print(
                    "Usage: latex-toolbox rename <new-name> "
                    "or latex-toolbox rename <old-name> <new-name>",
                    file=sys.stderr,
                )
                return 1
        except (FileNotFoundError, FileExistsError) as exc:
            print(str(exc), file=sys.stderr)
            return 1

        print(f"Project renamed: {target_dir}")
        print(f"Main file: {main_tex_file.name}")
        return 0

    if args.command == "setup":
        return run_setup(
            check_only=args.check_only,
            skip_extensions=args.skip_extensions,
            install_tex=args.install_tex,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
