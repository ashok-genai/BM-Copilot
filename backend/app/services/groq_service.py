
import json

from groq import Groq
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.customer_tools import (
    list_customers,
    count_customers,
    find_customer_by_code
)


client = Groq(
    api_key=settings.groq_api_key
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "list_customers",
            "description": "Retrieve all customers from the database.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_customers",
            "description": "Count the total number of customers.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_customer_by_code",
            "description": "Find a customer using their customer code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_code": {
                        "type": "string",
                        "description": "The unique customer code, for example CUST001."
                    }
                },
                "required": ["customer_code"]
            }
        }
    }
]



def get_ai_response(message: str, db: Session):

    messages = [
        {
            "role": "system",
            "content": (
                "You are BM Copilot, an ERP assistant. "
                "Use the available customer tools when answering "
                "questions about customer records. "
                "Never invent customer data."
            )
        },
        {
            "role": "user",
            "content": message
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.3
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:

        messages.append(response_message)

        for tool_call in response_message.tool_calls:

            function_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                if function_name == "list_customers":
                    result = list_customers(db)

                elif function_name == "count_customers":
                    result = count_customers(db)

                elif function_name == "find_customer_by_code":

                    customer_code = arguments.get("customer_code")

                    if (
                        not isinstance(customer_code, str)
                        or not customer_code.strip()
                    ):
                        raise ValueError("Invalid customer code")

                    result = find_customer_by_code(
                        db,
                        customer_code.strip()
                    )

                else:
                    raise ValueError("Unknown tool requested")

            except (KeyError, TypeError, ValueError):
                raise ValueError("Invalid tool request")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        final_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.3
        )

        return final_response.choices[0].message.content

    return response_message.content
