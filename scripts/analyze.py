import os
import re

def find_suspicious_patterns(file_path):
    patterns = {
        "Reflection": r"java\.lang\.reflect",
        "Runtime Exec": r"Runtime\.getRuntime\(\)\.exec",
        "ProcessBuilder": r"ProcessBuilder",
        "File I/O": r"java\.io\.File|java\.nio\.file",
        "Network": r"java\.net\.|HttpURLConnection|Socket",
        "Unsafe": r"sun\.misc\.Unsafe",
        "Hardcoded Secret": r"(?i)password\s*=\s*[\"\"].+[\"\"]|secret\s*=\s*[\"\"].+[\"\"]|key\s*=\s*[\"\"].+[\"\"]",
        "Class Loading": r"ClassLoader\.loadClass|URLClassLoader",
        "Thread Creation": r"new Thread\(",
        "System Exit": r"System\.exit"
    }

    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                for name, pattern in patterns.items():
                    if re.search(pattern, line):
                        findings.append((name, i+1, line.strip()))
    except Exception as e:
        pass
    return findings

with open("java_cyberhacks.txt", "r") as f:
    files = f.read().splitlines()

for file in files:
    res = find_suspicious_patterns(file)
    if res:
        print(f"\n--- {file} ---")
        for r in res:
            print(f"[{r[0]}] Line {r[1]}: {r[2]}")
