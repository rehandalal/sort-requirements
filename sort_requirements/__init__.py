import re


VERSION = (1, 3, 2)
DEPENDENCY_RE = re.compile(r"^([^\s!=~><#]+)\s*([=!~>]=)?\s*(.*)$")


__version__ = ".".join(str(v) for v in VERSION)


def _parse_dependency_line(line):
    match = DEPENDENCY_RE.match(line.strip())
    if not match:
        return None

    name, operator, version = match.groups()
    if operator:
        version = version.rstrip("\\").strip()
    else:
        version = None
    return name, operator, version


def sort_requirements(requirements, deduplicate=True):
    had_trailing_newline = requirements.endswith("\n")
    lines = requirements.split("\n")

    output_tokens = []
    dependencies = []
    pending_comments = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("#"):
            pending_comments.append(line)
            i += 1
            continue

        if not stripped:
            output_tokens.extend(("line", comment) for comment in pending_comments)
            pending_comments = []
            output_tokens.append(("line", line))
            i += 1
            continue

        if stripped.startswith("-r"):
            output_tokens.extend(("line", comment) for comment in pending_comments)
            pending_comments = []
            output_tokens.append(("line", line))
            i += 1
            continue

        parsed = _parse_dependency_line(line)
        if parsed is None:
            output_tokens.extend(("line", comment) for comment in pending_comments)
            pending_comments = []
            output_tokens.append(("line", line))
            i += 1
            continue

        name, operator, version = parsed
        block_lines = pending_comments + [line]
        pending_comments = []

        while block_lines[-1].rstrip().endswith("\\") and i + 1 < len(lines):
            i += 1
            block_lines.append(lines[i])

        dependencies.append(
            {
                "name": name,
                "operator": operator,
                "version": version,
                "block": "\n".join(block_lines),
            }
        )
        output_tokens.append(("dependency",))
        i += 1

    output_tokens.extend(("line", comment) for comment in pending_comments)

    sorted_dependencies = sorted(
        dependencies,
        key=lambda dep: dep["name"].casefold(),
    )

    if deduplicate:
        deduped = []
        seen = set()
        for dep in sorted_dependencies:
            if dep["block"] in seen:
                continue
            seen.add(dep["block"])
            deduped.append(dep)
        sorted_dependencies = deduped

    result_lines = []
    dep_index = 0
    for token in output_tokens:
        if token[0] == "line":
            result_lines.append(token[1])
            continue
        if dep_index < len(sorted_dependencies):
            result_lines.append(sorted_dependencies[dep_index]["block"])
            dep_index += 1

    result = "\n".join(result_lines)
    if had_trailing_newline and not result.endswith("\n"):
        result += "\n"
    return result
