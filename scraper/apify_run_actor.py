"""Run an Apify Actor and save its default dataset as JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from apify_client import ApifyClient


def load_actor_input(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None

    try:
        with path.open(encoding="utf-8") as input_file:
            actor_input = json.load(input_file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"No se pudo leer el JSON de entrada: {error}") from error

    if not isinstance(actor_input, dict):
        raise ValueError("La entrada del Actor debe ser un objeto JSON.")

    return actor_input


def run_actor(actor_id: str, actor_input: dict[str, Any] | None) -> list[dict[str, Any]]:
    token = os.environ.get("APIFY_API_TOKEN")
    if not token:
        raise ValueError("Configura APIFY_API_TOKEN en el entorno antes de ejecutar.")

    client = ApifyClient(token=token)
    run = client.actor(actor_id).call(run_input=actor_input)
    if run is None:
        raise RuntimeError("El Actor no terminó correctamente o no devolvió una ejecución.")

    return list(client.dataset(run.default_dataset_id).iterate_items())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ejecuta un Actor de Apify y guarda los elementos de su dataset."
    )
    parser.add_argument("actor_id", help="ID o nombre del Actor, por ejemplo apify/hello-world")
    parser.add_argument("--input", type=Path, help="Archivo JSON con la entrada del Actor")
    parser.add_argument(
        "--output", type=Path, help="Archivo JSON de salida (por defecto: stdout)"
    )
    args = parser.parse_args()

    try:
        items = run_actor(args.actor_id, load_actor_input(args.input))
        serialized_items = json.dumps(items, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(serialized_items + "\n", encoding="utf-8")
            print(f"Se guardaron {len(items)} elementos en {args.output}.")
        else:
            print(serialized_items)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
