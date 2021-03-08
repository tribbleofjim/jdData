class Result(object):
    def __init__(self, success=False, message=None, model=None):
        self.success = success
        self.message = message
        self.model = model

    def get_json(self):
        return {
            'success': self.success,
            'message': self.message,
            'model': self.model
        }
