
import re
import pandas as pd


def analyze_report(text):

    results = []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    number_pattern = r"\d+(?:\.\d+)?"

    range_pattern = re.compile(
        rf"^({number_pattern})\s*[-–—]\s*({number_pattern})$"
    )

    for i in range(1, len(lines) - 2):

        test_name = lines[i - 1]
        value_text = lines[i]
        reference = lines[i + 1]
        unit = lines[i + 2]

        if not re.fullmatch(number_pattern, value_text):
            continue

        range_match = range_pattern.fullmatch(reference)

        if not range_match:
            continue

        if not re.search(r"[A-Za-z]", test_name):
            continue

        value = float(value_text)
        minimum = float(range_match.group(1))
        maximum = float(range_match.group(2))

        if value < minimum:
            status = "Low"
        elif value > maximum:
            status = "High"
        else:
            status = "Normal"

        results.append({
            "Test": test_name,
            "Value": value,
            "Unit": unit,
            "Reference Range": reference,
            "Status": status
        })

    return pd.DataFrame(results)
