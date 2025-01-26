from provider.preprocessor.simple_preprocessr import SimplePreprocessor


class PreprocessorFactory:
    """Preprocessor Factory
    """
    def __init__(self):
        pass

    def create(self, preprocessor_model:str = "simple"):
        """Creates a preprocessor for processing text
        """
        if preprocessor_model == "simple":
            preprocessor = SimplePreprocessor()
            return preprocessor
        else:
            raise NotImplementedError("This preprocessor is not implemented")
