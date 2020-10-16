from sys import argv
from DataPipelineParser import ModifyConnectionType

if __name__ == "__main__":
    data_pipeline = ModifyConnectionType()
    data_pipeline.convert(argv[1])
