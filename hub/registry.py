"""Load and validate apps.yaml, the only list of apps in Signal Hub."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "apps.yaml"
FAMILIES = ("Brand", "Market", "Customer", "Research", "Decide")
MODES = ("embedded", "link", "coming_soon")
GITHUB = "https://github.com/UlrikErlingsen"
_SLUG = re.compile(r"^[a-z][a-z0-9]*$")
_TAG = re.compile(r"^v\d+\.\d+\.\d+$")
_WORDS = ("Zero One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen Fourteen Fifteen Sixteen "
          "Seventeen Eighteen Nineteen").split()
_TENS = {2: "Twenty", 3: "Thirty", 4: "Forty", 5: "Fifty", 6: "Sixty", 7: "Seventy", 8: "Eighty", 9: "Ninety"}
_REQUIRED = ("slug", "key", "product", "repo", "dist", "package", "family", "mode", "question", "one_liner")


class RegistryError(ValueError):
    """apps.yaml has an entry the Hub cannot use."""


@dataclass(frozen=True)
class App:
    slug: str
    key: str
    product: str
    repo: str
    dist: str
    package: str
    family: str
    mode: str
    question: str
    one_liner: str
    tag: str | None = None
    public: bool = True
    demo_url: str | None = None
    methods: tuple[str, ...] = field(default_factory=tuple)
    max_upload_mb: int | None = None
    tagline: str | None = None
    topics: tuple[str, ...] = field(default_factory=tuple)

    @property
    def prefix(self) -> str:
        """'Track' for 'Track Signal'."""
        return self.product.removesuffix(" Signal")

    @property
    def slogan(self) -> str:
        """Banner and theme tagline; falls back to the question."""
        return self.tagline or self.question

    @property
    def repo_url(self) -> str | None:
        return f"{GITHUB}/{self.repo}" if self.public else None

    @property
    def requirement(self) -> str | None:
        """pip requirement pinned to the released tag (embedded apps only). A tag archive needs no git client."""
        if self.mode != "embedded":
            return None
        return f"{self.dist}[ui] @ {GITHUB}/{self.repo}/archive/refs/tags/{self.tag}.zip"


def _validate(raw: dict, index: int) -> App:
    where = f"apps.yaml entry {index + 1} ({raw.get('slug', '?')})"
    missing = [name for name in _REQUIRED if not raw.get(name)]
    if missing:
        raise RegistryError(f"{where}: missing {', '.join(missing)}")
    unknown = set(raw) - set(App.__dataclass_fields__)
    if unknown:
        raise RegistryError(f"{where}: unknown field(s) {', '.join(sorted(unknown))}")
    if not _SLUG.match(raw["slug"]):
        raise RegistryError(f"{where}: slug must be lowercase letters and digits")
    if raw["family"] not in FAMILIES:
        raise RegistryError(f"{where}: family must be one of {', '.join(FAMILIES)}")
    if raw["mode"] not in MODES:
        raise RegistryError(f"{where}: mode must be one of {', '.join(MODES)}")
    if raw["mode"] == "embedded" and not _TAG.match(str(raw.get("tag") or "")):
        raise RegistryError(f"{where}: an embedded app needs a release tag like v1.2.0")
    if raw["mode"] == "link" and not str(raw.get("demo_url") or "").startswith("https://"):
        raise RegistryError(f"{where}: a link app needs an https demo_url")
    if not raw["product"].endswith(" Signal"):
        raise RegistryError(f"{where}: product must be '<Prefix> Signal'")
    cap = raw.get("max_upload_mb")
    if cap is not None and (not isinstance(cap, int) or not 1 <= cap <= 1000):
        raise RegistryError(f"{where}: max_upload_mb must be a whole number of MB between 1 and 1000")
    data = dict(raw)
    data["methods"] = tuple(raw.get("methods") or ())
    data["topics"] = tuple(raw.get("topics") or ())
    data["public"] = bool(raw.get("public", True))
    return App(**data)


def load(path: Path = REGISTRY) -> list[App]:
    """All apps, in file order. Raises RegistryError on the first bad entry."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list) or not raw:
        raise RegistryError("apps.yaml must be a non-empty list")
    apps = [_validate(entry, i) for i, entry in enumerate(raw)]
    for attr in ("slug", "repo", "package"):
        seen: set[str] = set()
        for app in apps:
            value = getattr(app, attr)
            if value in seen:
                raise RegistryError(f"apps.yaml: duplicate {attr} {value!r}")
            seen.add(value)
    return apps


def by_family(apps: list[App]) -> dict[str, list[App]]:
    return {family: [a for a in apps if a.family == family] for family in FAMILIES}


def count_word(n: int) -> str:
    """'Twenty' for 20: the suite size in prose (front page, READMEs)."""
    if 0 <= n < 20:
        return _WORDS[n]
    if 20 <= n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + (f"-{_WORDS[ones].lower()}" if ones else "")
    return str(n)
