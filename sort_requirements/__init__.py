import re


VERSION = (1, 3, 1)
# Match packages with version specifiers: comments + package + version_spec + version + continuation
DEPS_WITH_VERSION_RE = (
    r"((?:#[^\n]+?\n)*)([^\n]+?)([=!~>]=)([^\\\n]+)((?:\\\n[^\\\n]+)*)"
)


__version__ = ".".join(str(v) for v in VERSION)


def sort_requirements(requirements, deduplicate=True):
    had_trailing_newline = requirements.endswith("\n")

    # Handle packages with version specifiers (existing behavior)
    matches = re.findall(DEPS_WITH_VERSION_RE, requirements)
    data = re.sub(DEPS_WITH_VERSION_RE, "{}", requirements)

    # Now handle packages without version specifiers
    # Process the remaining content to find lines that are packages without versions
    lines = data.split("\n")
    packages_no_version = []

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Skip empty lines, comments, directives, and placeholders
        if (
            not line_stripped
            or line_stripped.startswith("#")
            or line_stripped.startswith("-r")
            or line_stripped == "{}"
        ):
            continue

        # Skip if it contains a version specifier (should have been matched)
        if re.search(r"[=!~>]=", line_stripped):
            continue

        # This is a package without version
        # Extract comments and package name
        comment_match = re.match(r"((?:#[^\n]+\n?)*)", line_stripped)
        comments = comment_match.group(1) if comment_match else ""
        package_name = line_stripped[len(comments) :].strip()

        if package_name:
            packages_no_version.append((comments, package_name))
            # Replace this line with a placeholder
            lines[i] = "|||"

    # Combine and sort by package name (deduplicate exact lines only when enabled)
    all_packages = []
    seen = set() if deduplicate else None

    # Add versioned packages with their package names for sorting
    for m in matches:
        if deduplicate:
            line_content = "{}{}{}{}{}".format(*m)
            if line_content in seen:
                continue
            seen.add(line_content)
        all_packages.append(("with_version", m[1].lower().strip(), m))

    # Add non-versioned packages with their package names for sorting
    for comments, package_name in packages_no_version:
        if deduplicate:
            line_content = "{}{}".format(comments, package_name)
            if line_content in seen:
                continue
            seen.add(line_content)
        package_name_lower = package_name.lower().strip()
        all_packages.append(
            ("no_version", package_name_lower, (comments, package_name))
        )

    # Sort all packages together by package name
    all_packages.sort(key=lambda x: x[1])

    # Format sorted packages
    all_deps = []
    for pkg_type, pkg_name_lower, pkg_data in all_packages:
        if pkg_type == "with_version":
            all_deps.append("{}{}{}{}{}".format(*pkg_data))
        else:
            comments, package_name = pkg_data
            all_deps.append("{}{}".format(comments, package_name))

    # Replace placeholders line-by-line so removed duplicates don't leave blank lines.
    placeholder_idx = 0
    output_lines = []
    for line in lines:
        if line in ("{}", "|||"):
            if placeholder_idx < len(all_deps):
                output_lines.append(all_deps[placeholder_idx])
                placeholder_idx += 1
            continue
        output_lines.append(line)

    result = "\n".join(output_lines)
    if had_trailing_newline and not result.endswith("\n"):
        result += "\n"
    return result
