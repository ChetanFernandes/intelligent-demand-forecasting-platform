from dataclasses import dataclass, field
from typing import Any

@dataclass
class SageMakerEstimatorConfig:
    """
    Configuration required to create a SageMaker Estimator.
    """
    entry_point: str
    source_dir: str
    framework_version: str
    py_version: str
    instance_type: str
    instance_count: int
    role: str
    sagemaker_session: Any
    metric_definitions: list[dict] 
    hyperparameters: dict[str, Any] = field(default_factory = dict)
 

    # default_factory  =dict - This tells Python: Every time you create a new SageMakerEstimatorConfig, create a brand new empty dictionary.
    # Any - "This value can be of any Python type."
    # field(default_factory = dict) - Each object will have its own dictionary
    # A simple rule to remember - Whenever your dataclass contains a mutable object such as: list, dict, set Always use default_factory.
    ''' 
        dataclass automaticlly creates 

        __init__()
        __repr__()
        __eq__()
'''