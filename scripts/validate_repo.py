from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def check_skill_structure() -> None:
    validator = SKILLS / "skill-creator" / "scripts" / "quick_validate.py"
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            fail(f"missing {skill_file.relative_to(ROOT)}")
        if len(skill_file.read_text(encoding="utf-8").splitlines()) > 500:
            fail(f"{skill_file.relative_to(ROOT)} exceeds 500 lines")
        result = subprocess.run(
            [sys.executable, str(validator), str(skill_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            fail(f"invalid {skill_dir.name}: {result.stdout}{result.stderr}".strip())
    print(f"PASS: {len(skill_dirs)} skills are structurally valid")


def check_contracts() -> None:
    duplicate = SKILLS / "project-audit" / "references" / "PROJECT_WIKI_TEMPLATE.md"
    if duplicate.exists():
        fail("project-audit contains a duplicate PROJECT_WIKI_TEMPLATE.md")

    targets = [
        SKILLS / "express-incubate" / "SKILL.md",
        SKILLS / "implementation-kit" / "SKILL.md",
    ]
    forbidden = ("Agent(", "TaskOutput(", "run_in_background", "load_skills")
    for target in targets:
        active_contract = target.read_text(encoding="utf-8").split("## Changelog", 1)[0]
        for token in forbidden:
            if token in active_contract:
                fail(f"legacy orchestration token {token!r} in {target.relative_to(ROOT)}")

    express = targets[0].read_text(encoding="utf-8")
    ordered = (
        "项目启动",
        "方向探索",
        "项目定界",
        "需求澄清",
        "研究验证",
        "架构与契约",
        "基线一致性",
        "派生设计",
        "设计一致性",
        "交付与量化验收",
        "交付配套",
        "收尾交接",
    )
    positions = [express.find(label) for label in ordered]
    if -1 in positions or positions != sorted(positions):
        fail("express-incubate phase order is incomplete or inconsistent")

    contaminated = []
    for path in SKILLS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "打卡" in text or "习惯追踪" in text:
            contaminated.append(str(path.relative_to(ROOT)))
    if contaminated:
        fail("domain-specific examples remain: " + ", ".join(contaminated))

    print("PASS: cross-skill contracts are consistent")


def check_public_entrypoints() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in ("## 为什么需要它", "## 30 秒开始", "## 参与贡献", "## License"):
        if heading not in readme:
            fail(f"README missing {heading}")
    for path in (
        ROOT / "CONTRIBUTING.md",
        ROOT / ".github" / "pull_request_template.md",
        ROOT / ".github" / "workflows" / "validate.yml",
    ):
        if not path.exists():
            fail(f"missing public repository entrypoint {path.relative_to(ROOT)}")
    print("PASS: public repository entrypoints are present")


if __name__ == "__main__":
    check_skill_structure()
    check_contracts()
    check_public_entrypoints()
    print("PASS: repository validation complete")
