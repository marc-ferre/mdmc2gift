#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "mdmc2gift"
    sample = repo_root / "examples" / "sample_valid.mdmc"

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        copied_sample = temp_path / sample.name
        shutil.copy2(sample, copied_sample)

        completed = subprocess.run(
            [sys.executable, str(script), str(copied_sample)],
            cwd=temp_path,
            capture_output=True,
            text=True,
            check=True,
        )

        output_file = copied_sample.with_suffix(".gift")
        assert output_file.is_file(), "Le fichier .gift n'a pas été créé"

        content = output_file.read_text(encoding="utf-8")
        assert "::Q1::" in content
        assert "=Paris" in content
        assert "~Lyon" in content
        assert "~Aucune de ces réponses n'est correcte." in content
        assert "::Q2::" in content
        assert "=4" in content

        assert completed.returncode == 0

        sample_five = temp_path / "sample_five.mdmc"
        sample_five.write_text(
            textwrap.dedent(
                """\
                ## [Q3]
                ### Quelle proposition est correcte ?
                + Réponse 1
                - Réponse 2
                - Réponse 3
                - Réponse 4
                - Réponse 5
                """
            ),
            encoding="utf-8",
        )

        subprocess.run(
            [sys.executable, str(script), str(sample_five)],
            cwd=temp_path,
            capture_output=True,
            text=True,
            check=True,
        )

        five_content = sample_five.with_suffix(".gift").read_text(encoding="utf-8")
        assert "~Aucune de ces réponses n'est correcte." not in five_content
        assert five_content.count("\n=") == 1
        assert five_content.count("\n~") == 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())