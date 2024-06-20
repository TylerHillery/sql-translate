from pydantic import BaseModel
from typing import Optional, Any, Dict


class SqlErrorDetails(BaseModel):
    description: Optional[str] = None
    line: Optional[int] = None
    col: Optional[int] = None
    start_context: Optional[str] = None
    highlight: Optional[str] = None
    end_context: Optional[str] = None
    into_expression: Optional[str] = None


class SqlTranslationResponse(BaseModel):
    is_valid_sql: bool
    sql: str | SqlErrorDetails


class SqlTranslationRequest(BaseModel):
    sql: str
    from_dialect: str
    to_dialect: str
    options: Optional[Dict[str, Any]] = None


class CaseMapping(BaseModel):
    transpiled_token: str
    correct_case: str
