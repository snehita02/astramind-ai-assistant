class BaseTool:
    name: str
    description: str

    def run(self, input_data):
        raise NotImplementedError("Tool must implement run method.")
        