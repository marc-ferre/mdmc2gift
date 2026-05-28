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

        sample_format = temp_path / "sample_format.mdmc"
        sample_format.write_text(
            textwrap.dedent(
                """\
                ## [Q4]
                ### Énoncé **important** en *italique*
                + Réponse **correcte**
                - Réponse *incorrecte*
                - Réponse neutre
                - Réponse finale
                """
            ),
            encoding="utf-8",
        )

        subprocess.run(
            [sys.executable, str(script), str(sample_format)],
            cwd=temp_path,
            capture_output=True,
            text=True,
            check=True,
        )

        format_content = sample_format.with_suffix(".gift").read_text(encoding="utf-8")
        assert "::Q4:: Énoncé <strong>important</strong> en <em>italique</em>. {" in format_content
        assert "=Réponse <strong>correcte</strong>" in format_content
        assert "~Réponse <em>incorrecte</em>" in format_content

        sample_list = temp_path / "sample_list.mdmc"
        sample_list.write_text(
            textwrap.dedent(
                """\
                ## [Q5]
                ### Voici une question
                Première ligne

                - élément 1
                - élément 2

                Conclusion
                + Bonne réponse
                - Mauvaise réponse 1
                - Mauvaise réponse 2
                - Mauvaise réponse 3
                """
            ),
            encoding="utf-8",
        )

        subprocess.run(
            [sys.executable, str(script), str(sample_list)],
            cwd=temp_path,
            capture_output=True,
            text=True,
            check=True,
        )

        list_content = sample_list.with_suffix(".gift").read_text(encoding="utf-8")
        assert "<ul>" in list_content
        assert "<li>élément 1</li>" in list_content
        assert "<li>élément 2</li>" in list_content
        assert "<p>Conclusion.</p>" in list_content
        assert "=Bonne réponse" in list_content
        assert "~Mauvaise réponse 3" in list_content

    return 0


if __name__ == "__main__":
    raise SystemExit(main())