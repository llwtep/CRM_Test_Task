# exceptions.py
class AIException(Exception):
    
    pass

class ForbiddenQueryException(AIException):
    
    pass

class SQLExecutionException(AIException):
    
    def __init__(self, sql: str, original_error: str):
        self.sql = sql
        self.original_error = original_error
        super().__init__(f"SQL execution failed: {original_error}")

class LLMException(AIException):
    ""
    def __init__(self, step: str, original_error: str):
        self.step = step
        self.original_error = original_error
        super().__init__(f"LLM failed at step '{step}': {original_error}")

class RedisConnectionException(AIException):
    
    pass