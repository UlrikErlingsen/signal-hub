from pathlib import Path

import pytest
import yaml

from hub import registry
from hub.registry import RegistryError, load

ROOT = Path(__file__).resolve().parents[1]


def _write(tmp_path: Path, entries: list[dict]) -> Path:
    path = tmp_path / "apps.yaml"
    path.write_text(yaml.safe_dump(entries), encoding="utf-8")
    return path


def _entry(**overrides) -> dict:
    entry = {"slug": "track", "key": "track", "product": "Track Signal", "repo": "brand-tracking",
             "dist": "tracksignal", "package": "tracksignal", "tag": "v1.1.0", "family": "Brand",
             "mode": "embedded", "question": "Is the brand moving?", "one_liner": "Brand tracking."}
    entry.update(overrides)
    return entry


def test_registry_loads_every_app_once() -> None:
    apps = load()
    assert len(apps) >= 20
    assert len({a.slug for a in apps}) == len(apps)
    assert {a.family for a in apps} == set(registry.FAMILIES)


def test_every_app_matches_the_shared_theme() -> None:
    from hub.theme import MARKS, sig

    for app in load():
        theme_app = sig.app(app.key)
        assert theme_app["name"] == app.product
        assert theme_app["repo"] == app.repo
        assert theme_app["fam"]["label"] == app.family
        assert (MARKS / f"{theme_app['slug']}-mark.svg").exists()


def test_embedded_apps_are_public_and_pinned() -> None:
    for app in load():
        if app.mode == "embedded":
            assert app.public, app.slug
            assert app.requirement.endswith(f"/archive/refs/tags/{app.tag}.zip")
        else:
            assert app.requirement is None


def test_freddo_crm_is_not_a_hub_app() -> None:
    assert all(a.repo != "signal-crm" for a in load())


def test_influencer_campaigns_uses_its_current_name() -> None:
    names = {a.repo: a.product for a in load()}
    assert names["influencer-campaigns"] == "Influence Signal"
    assert "Creator Signal" not in (ROOT / "apps.yaml").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"family": "Sales"}, "family must be one of"),
        ({"mode": "iframe"}, "mode must be one of"),
        ({"tag": "main"}, "release tag"),
        ({"mode": "link", "tag": None}, "https demo_url"),
        ({"product": "TrackSignal"}, "<Prefix> Signal"),
        ({"colour": "red"}, "unknown field"),
        ({"question": ""}, "missing question"),
    ],
)
def test_bad_entries_fail_loudly(tmp_path: Path, overrides: dict, message: str) -> None:
    with pytest.raises(RegistryError, match=message):
        load(_write(tmp_path, [_entry(**overrides)]))


def test_duplicate_slugs_are_rejected(tmp_path: Path) -> None:
    with pytest.raises(RegistryError, match="duplicate slug"):
        load(_write(tmp_path, [_entry(), _entry(repo="other", package="other")]))


def test_every_generated_list_matches_the_registry() -> None:
    """README tables, theme APPS block, topics, repo metadata, requirement pins: run scripts/sync_suite.py."""
    from scripts import sync_suite

    stale = [str(path.relative_to(ROOT)) for path, data in sync_suite.plan(hub_only=True).items()
             if not (path.exists() and sync_suite._same(path.read_bytes(), data))]
    assert not stale, f"{stale} out of date; run python scripts/sync_suite.py"


def test_count_word_spells_the_suite_size() -> None:
    from hub.registry import count_word

    assert [count_word(n) for n in (9, 19, 20, 21, 34)] == ["Nine", "Nineteen", "Twenty", "Twenty-one", "Thirty-four"]


def test_every_app_has_a_mark_and_brand_images() -> None:
    from hub.theme import THEME_DIR

    assets = THEME_DIR / "assets"
    for app in load():
        slug = f"{app.key}signal"
        for path in (assets / "marks" / f"{slug}-mark.svg", assets / "marks" / f"{slug}-mark-64.png",
                     assets / "banners" / f"{slug}-banner.png", assets / "social" / f"{slug}-social.png"):
            assert path.exists(), f"{path.name} missing; see docs/ADDING_AN_APP.md"


def test_requirement_files_are_generated_from_the_registry() -> None:
    from scripts import gen_requirements

    for path, text in gen_requirements.render().items():
        assert path.read_text(encoding="utf-8") == text, f"{path.name} is stale; run scripts/gen_requirements.py"
