from __future__ import annotations

import argparse
import sys

from .project import available_templates, create_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="latex-toolbox",
        description="Utilities for generating standalone LaTeX projects from the toolbox.",
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
        try:
            target_dir, main_tex_file = create_project(
                name=args.name,
                template=args.template,
            )
        except (ValueError, FileExistsError) as exc:
            print(str(exc), file=sys.stderr)
            return 1

        print(f"Projet cree dans: {target_dir}")
        print(f"Ouvre ensuite: {main_tex_file}")
        print("Le projet embarque maintenant son style local dans styles/packages/.")
        print(f"Template utilise: {args.template}")
        print(f"Dossier parent courant: {target_dir.parent}")
        print("Pense a personnaliser frontmatter/metadata.tex puis les sections.")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
