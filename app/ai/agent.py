import re
from sqlalchemy import text
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_groq import ChatGroq
from app.core.config import settings
from app.ai.exceptions import (
    ForbiddenQueryException,
    SQLExecutionException, 
    LLMException,
    RedisConnectionException
)

DB_SCHEMA_PROMPT = """
You are an expert PostgreSQL SQL query generator.
Your task is to strictly translate user questions into valid SQL SELECT queries.
You have access to a CRM database with the following schema:
1. Table `teachers` (id, full_name, phone, specialization)
2. Table `students` (id, full_name, phone, birth_date, created_at)
3. Table `groups` (id, name, teacher_id, start_date, status: 'ACTIVE', 'PLANNING', 'FROZEN', 'COMPLETED')
4. Table `group_students` (id, group_id, student_id, status: 'ACTIVE', 'LEFT', 'FROZEN', 'COMPLETED')
5. Table `attendance` (id, group_student_id, date, status: 'PRESENT', 'ABSENT')
CRITICAL RULES:
1. Return ONLY a raw SQL SELECT query. Do not use Markdown formatting, code blocks, explanations, comments, or any additional text. Output only the SQL query itself.
2. You are strictly forbidden from modifying data. If the user requests any INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, or other data/schema modification operation, return exactly:
FORBIDDEN
3. Always use the exact table names provided above (plural form).
4. Generate only valid PostgreSQL SQL syntax.
5. When a question requires data from multiple tables, use proper JOIN statements based on the relationships defined in the schema.
6. If the user's request is unclear or cannot be answered using the available schema, return exactly:
FORBIDDEN
7. Never invent tables or columns that are not present in the schema.
8. Always prefer explicit column names over SELECT * unless the user explicitly requests all available fields.
"""




class CRMChainService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=settings.GROQ_API_KEY,
            temperature=0.0
        )

    def _get_redis_history(self, session_id: str):
        try:
            redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
            return RedisChatMessageHistory(session_id=session_id, url=redis_url, ttl=86400)
        except Exception as e:
            raise RedisConnectionException(f"Cannot connect to Redis: {str(e)}")

    async def chat(self, session_id: str, message: str) -> str:
        try:
            sql_prompt = ChatPromptTemplate.from_messages([
                ("system", DB_SCHEMA_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}")
            ])
            sql_chain = sql_prompt | self.llm | StrOutputParser()
            sql_chain_with_history = RunnableWithMessageHistory(
                sql_chain,
                self._get_redis_history,
                input_messages_key="input",
                history_messages_key="chat_history"
            )
            sql_query = await sql_chain_with_history.ainvoke(
                {"input": message},
                config={"configurable": {"session_id": session_id}}
            )
        except RedisConnectionException:
            raise 
        except Exception as e:
            raise LLMException(step="sql_generation", original_error=str(e))

        
        sql_query = sql_query.strip()
        if "FORBIDDEN" in sql_query or not sql_query.lower().startswith("select"):
            raise ForbiddenQueryException(
                f"LLM rejected the query as forbidden. Raw response: {sql_query}"
            )

        
        try:
            result = await self.db_session.execute(text(sql_query))
            db_result = result.fetchall()
        except Exception as e:
            raise SQLExecutionException(sql=sql_query, original_error=str(e))


        try:
            human_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a friendly AI assistant for a training center's CRM system. Formulate a clear, polite response in English based on the raw data from the database: {db_result}"),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}")
            ])
            human_chain = human_prompt | self.llm | StrOutputParser()
            human_chain_with_history = RunnableWithMessageHistory(
                human_chain,
                self._get_redis_history,
                input_messages_key="input",
                history_messages_key="chat_history"
            )
            final_answer = await human_chain_with_history.ainvoke(
                {"input": message, "db_result": str(db_result)},
                config={"configurable": {"session_id": session_id}}
            )
        except RedisConnectionException:
            raise
        except Exception as e:
            raise LLMException(step="answer_generation", original_error=str(e))

        return final_answer