class CoverageItem:
    def __init__(self, name, file_name, coverable_lines, covered_lines, branches, 
                 covered_branches):
        self.name = name
        self.file_name = file_name
        self.coverable_lines = coverable_lines
        self.covered_lines = covered_lines
        self.branches = branches
        self.covered_branches = covered_branches

    def __str__(self):
        return f"CoverageItem: {self.name}"
