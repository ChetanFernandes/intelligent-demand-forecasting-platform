
class ValidationError(Exception):

    def __init__(self,message):
        super().__init__(message)

    '''
    def __init__(self, report):

        super().__init__(str(report))  # Message shown when printing the exception

        self.report = report   # Full report available for later use
    '''


class SchemaValidationError(ValidationError):
    pass


class MissingValuesValidationError(ValidationError):
    pass


class OutlierValidationError(ValidationError):
    pass


class GXValidationError(ValidationError):
    pass

'''
Raise exceptions at the layer where the problem is detected.
Log exceptions at the layer where you decide how the application should respond (often the pipeline or main.py).
Log in lower layers only if you are adding important context that would otherwise be missing.


raise ValidationError(report)
            │
            ▼
ValidationError.__init__(report)
            │
            ▼
str(report)
            │
            ▼
ValidationReport.__str__()
            │
            ▼
"ERRORS
Missing required column...
WARNINGS..."
            │
            ▼
super().__init__(formatted_string)
            │
            ▼
Exception stores the message
            │
            ▼
self.report = report
'''

