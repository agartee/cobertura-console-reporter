import xml.etree.ElementTree as ET
from typing import List
import re

from cobertura_reporter.coverage_item import CoverageItem


def parse(file_path:str, package_name:str = None) -> List[CoverageItem]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    results :List[CoverageItem] = []
    
    for package in root.findall(".//package"):
        if package_name != None and package.get("name") != package_name:
            continue

        for classes in package.findall("classes"):
            for cls in classes.findall("class"):
                coverage_item = _create_coverage_item(cls)

                existing = next(
                    (r for r in results if r.name == coverage_item.name), 
                    None)
                
                if existing:
                    _merge_coverage_items(existing, coverage_item)
                    continue

                results.append(coverage_item)

    return results

def _split_conditional_coverage(input_string) -> tuple[int,int]:
    pattern = r"(\d+)%\s*\((\d+)/(\d+)\)"
    match = re.search(pattern, input_string)

    covered_branches = int(match.group(2))
    branches = int(match.group(3))

    return (covered_branches, branches)

def _create_coverage_item(cls) -> CoverageItem:
    class_name = cls.get("name").split("/")[0]
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
    
    return CoverageItem(class_name, file_name, coverable_lines, covered_lines,
                         branches, covered_branches)

def _merge_coverage_items(existing: CoverageItem, new:CoverageItem):
    existing.coverable_lines += new.coverable_lines
    existing.covered_lines += new.covered_lines
    existing.branches += new.branches
    existing.covered_branches += new.covered_branches
