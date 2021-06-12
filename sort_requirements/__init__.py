import re


VERSION = (1, 4, 0)
DEPS_RE = r"((?:#[^\n]+?\n)*)([^\n]+?)([=!~>]=)([^\\\n]+)((?:\\\n[^\\\n]+)*)"


__version__ = ".".join(str(v) for v in VERSION)


def sort_requirements(requirements, remove_duplicates=False):

    matches = re.findall(DEPS_RE, requirements)
    data = re.sub(DEPS_RE, "{}", requirements)
    matches = sorted(matches, key=lambda d: d[1].lower())

    deps = []
    for m in matches:
        deps.append("{}{}{}{}{}".format(*m))

    data = data.format(*deps)
    return data
