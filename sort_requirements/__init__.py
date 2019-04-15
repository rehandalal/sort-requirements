import re


VERSION = (1, 0, 0)
DEPS_RE = r"(.+?)==([^\\\n]+)((?:\\\n[^\\\n]+)*)"


__version__ = ".".join(str(v) for v in VERSION)


def sort_requirements(requirements):
    matches = re.findall(DEPS_RE, requirements)
    data = re.sub(DEPS_RE, "{}", requirements)
    matches = sorted(matches, key=lambda d: d[0].lower())

    deps = []
    for m in matches:
        dep = "{}=={}".format(*m[0:2])
        if m[2]:
            dep += m[2]
        deps.append(dep)

    data = data.format(*deps)
    return data
