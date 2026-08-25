from pathlib import Path


class ValidationReport:

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.information = []

    def add_errors(self,message):
        self.errors.append(message)

    def add_warnings(self,message):
        self.warnings.append(message)

    def add_infm(self,message):
        self.information.append(message)
        
    def has_errors(self):
        return len(self.errors) > 0

    def __str__(self):

        output = []

        if self.errors:
            output.append("ERRORS")
            output.extend(self.errors)

        if self.warnings:
            output.append("\nWARNINGS")
            output.extend(self.warnings)

        if self.information:
            output.append("\nINFORMATION")
            output.extend(self.information)

        return "\n".join(output)

    def save_report_first_validation(self,path):
        
        path = Path(path/"validation_report")

        path.mkdir(parents=True,exist_ok=True)

        filename = (
            f"validation_report.txt"
            #f"{datetime.now():%Y%m%d_%H%M%S}.txt"
        )
        filepath = path/filename
        with open(filepath,"w",encoding="utf-8") as f:
            f.write(str(self))

        return filepath

    def save_report_re_validation(self,path):
        
        path = Path(path/"validation_report")

        path.mkdir(parents=True,exist_ok=True)

        filename = (
            f"re_validation_report.txt"
            #f"{datetime.now():%Y%m%d_%H%M%S}.txt"
        )
        filepath = path/filename
        with open(filepath,"w",encoding="utf-8") as f:
            f.write(str(self))

        return filepath

''' 
__str__() exists to define the human-readable representation of your object whenever it is printed, 
logged, or converted to a string. That's why it's so useful for a class like ValidationReport.
'''