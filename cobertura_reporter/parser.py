import xml.etree.ElementTree as ET
from cobertura_reporter.coverage_item import CoverageItem
from typing import Iterator
import re


def parse(file_path) -> Iterator[CoverageItem]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    results = []
    for package in root.findall(".//package"):
        for classes in package.findall("classes"):
            for cls in classes.findall("class"):
                class_name = cls.get("name")
                file_name = cls.get("filename")
                
                coverable_lines = 0
                covered_lines = 0
                branches = 0
                covered_branches = 0

                for lines in cls.findall("lines"):
                    for line in lines.findall("line"):
                        coverable_lines += 1

                        if int(line.get("hits")) > 0:
                            covered_lines += 1

                        if line.get("branch") == "True":
                            conditional_coverage = _split_conditional_coverage(
                                line.get("condition-coverage"))
                            
                            covered_branches += conditional_coverage[0]
                            branches += conditional_coverage[1]
                                        
                results.append(CoverageItem(class_name, file_name, coverable_lines, 
                                            covered_lines, branches, covered_branches))

    return results

def _split_conditional_coverage(input_string):
    pattern = r"(\d+)%\s*\((\d+)/(\d+)\)"
    match = re.search(pattern, input_string)

    covered_branches = int(match.group(2))
    branches = int(match.group(3))

    return (covered_branches, branches)
