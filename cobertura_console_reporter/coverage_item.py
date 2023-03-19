class CoverageItem(object):
    def __init__(self, name: str, file_name: str, coverable_lines: int, 
                 covered_lines: int, branches: int, covered_branches: int):
        self.name = name
        self.file_name = file_name
        self.coverable_lines = coverable_lines
        self.covered_lines = covered_lines
        self.branches = branches
        self.covered_branches = covered_branches

    @property
    def class_name(self) -> str:
        if "." not in self.name:
            return self.name

        _, class_name = self.name.rsplit(".", 1)
        return class_name
    
    @property
    def class_namespace(self) -> str:
        if "." not in self.name:
            return ""
        
        namespace, _ = self.name.rsplit(".", 1)
        return namespace
