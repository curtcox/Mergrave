"""Build HTML reports for unit, property, and coverage test results."""

from __future__ import annotations

import html
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
HTMLCOV_DIR = ROOT / "htmlcov"


def _clean_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def _render_page(
    title: str,
    body: str,
    *,
    links: Sequence[tuple[str, str]] = (),
    preformatted: bool = True,
) -> str:
    nav_links = "".join(
        f'<li><a href="{html.escape(href)}">{html.escape(label)}</a></li>'
        for label, href in links
    )
    nav_html = f"<ul>{nav_links}</ul>" if nav_links else ""
    if preformatted:
        body_html = f"<pre>{html.escape(body)}</pre>"
    else:
        body_html = f"<p>{html.escape(body)}</p>"
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <title>{html.escape(title)}</title>
    <style>
      body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.5; }}
      pre {{ background: #1e1e1e; color: #f5f5f5; padding: 1rem; overflow-x: auto; border-radius: 0.5rem; }}
      a {{ color: #0b6bf2; }}
    </style>
  </head>
  <body>
    <h1>{html.escape(title)}</h1>
    {nav_html}
    {body_html}
  </body>
</html>
"""


def _run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def _write_report(command: Sequence[str], destination: Path, title: str) -> None:
    result = _run_command(command)
    output = result.stdout
    if result.stderr:
        output = f"{output}\n{result.stderr}".strip()
    page = _render_page(title, output or "(no output)")
    destination.mkdir(parents=True, exist_ok=True)
    destination.joinpath("index.html").write_text(page, encoding="utf-8")
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)


def _generate_unit_report() -> None:
    _write_report(
        ("python", "-m", "pytest", "-m", "not property", "-ra"),
        REPORTS_DIR / "unit",
        "Unit test results",
    )


def _generate_property_report() -> None:
    _write_report(
        ("python", "-m", "pytest", "-m", "property", "-ra"),
        REPORTS_DIR / "property",
        "Property test results",
    )


def _generate_coverage_report() -> None:
    destination = REPORTS_DIR / "coverage"
    _clean_directory(HTMLCOV_DIR)
    result = _run_command(("python", "-m", "coverage", "erase"))
    if result.returncode != 0:
        message = (result.stdout or "") + (result.stderr or "")
        if "No data to erase" not in message:
            raise subprocess.CalledProcessError(
                result.returncode,
                result.args,
                output=result.stdout,
                stderr=result.stderr,
            )

    run_result = _run_command(("python", "-m", "coverage", "run", "-m", "pytest"))
    if run_result.returncode != 0:
        raise subprocess.CalledProcessError(run_result.returncode, run_result.args, output=run_result.stdout, stderr=run_result.stderr)

    report_result = _run_command(("python", "-m", "coverage", "report", "-m"))
    if report_result.returncode != 0:
        raise subprocess.CalledProcessError(
            report_result.returncode,
            report_result.args,
            output=report_result.stdout,
            stderr=report_result.stderr,
        )

    html_result = _run_command(("python", "-m", "coverage", "html"))
    if html_result.returncode != 0:
        raise subprocess.CalledProcessError(
            html_result.returncode,
            html_result.args,
            output=html_result.stdout,
            stderr=html_result.stderr,
        )

    summary_page = _render_page(
        "Coverage summary",
        report_result.stdout.strip(),
        links=(("Open HTML coverage report", "htmlcov/index.html"),),
    )

    destination.mkdir(parents=True, exist_ok=True)
    destination.joinpath("index.html").write_text(summary_page, encoding="utf-8")
    if (destination / "htmlcov").exists():
        shutil.rmtree(destination / "htmlcov")
    shutil.copytree(HTMLCOV_DIR, destination / "htmlcov")


def _generate_index() -> None:
    links = [
        ("Unit test results", "unit/index.html"),
        ("Property test results", "property/index.html"),
        ("Coverage summary", "coverage/index.html"),
        ("Coverage HTML", "coverage/htmlcov/index.html"),
    ]
    report_page = _render_page(
        "Mergrave test reports",
        "Select a report from the links below.",
        links=links,
        preformatted=False,
    )
    REPORTS_DIR.joinpath("index.html").write_text(report_page, encoding="utf-8")


def main() -> None:
    _clean_directory(REPORTS_DIR)
    _generate_unit_report()
    _generate_property_report()
    _generate_coverage_report()
    _generate_index()


if __name__ == "__main__":
    main()
