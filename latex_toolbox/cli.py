from __future__ import annotations

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version


def _get_version() -> str:
    try:
        return version("latex-toolbox")
    except PackageNotFoundError:
        return "unknown"

from .project import (
    available_templates,
    create_project,
    rename_current_project,
    rename_project,
)
from .setup import (
    is_first_run,
    mark_initialized,
    run_first_launch_check,
    run_setup,
    warn_if_latex_missing,
)


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
        required=True,
        help="Name of the report and of the generated main .tex file.",
    )
    create_parser.add_argument(
        "--template",
        required=True,
        help="Template name to use.",
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
        first_run = is_first_run()
        if first_run:
            run_first_launch_check()
            mark_initialized()

        try:
            target_dir, main_tex_file = create_project(
                name=args.name,
                template=args.template,
            )
        except (ValueError, FileExistsError) as exc:
            print(str(exc), file=sys.stderr)
            return 1

        print(f"Project created in: {target_dir}")
        print(f"Open next: {main_tex_file}")
        print("The project now embeds its local styles in styles/packages/.")
        print(f"Template used: {args.template}")
        print(f"Current parent folder: {target_dir.parent}")
        print("Remember to customise frontmatter/metadata.tex and the sections.")

        if not first_run:
            warn_if_latex_missing()

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

        print(f"Project renamed in: {target_dir}")
        print(f"New main file: {main_tex_file}")
        print("The project folder and the main .tex file have been renamed.")
        print("Build files tied to the main name were also renamed when they existed.")
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
