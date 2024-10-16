from dataclasses import dataclass

@dataclass
class ServerErrorCode:
    unsupportedHttpMehod = "STD_1000"
    invalidInputParameters = "STD_1001"
