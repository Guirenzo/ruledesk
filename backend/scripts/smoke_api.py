from __future__ import annotations

import json
from urllib.request import Request, urlopen

from app.schemas.incidents import sample_incidents


def main() -> None:
    payload = json.dumps(sample_incidents()[0]).encode("utf-8")
    request = Request(
        "http://127.0.0.1:8000/api/incidents",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))

    evaluation = data["evaluation"]
    print("API respondeu com sucesso.")
    print(f"Prioridade: {evaluation['priority']['level']} - {evaluation['priority']['label']}")
    print(f"Score: {evaluation['score']}")


if __name__ == "__main__":
    main()
