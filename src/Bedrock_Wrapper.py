import boto3
import json
import os

class LLMQuery:
    def __init__(self):
        self.modelId = "anthropic.claude-3-haiku-20240307-v1:0"
        self.region_name = "ap-southeast-1"
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=self.region_name
        )

    def generate_query_body(self, query: str) -> str:
        return json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": """You are an assistant helping Singapore's Internal Security Department (ISD) in 
                          categorizing texts into 0 to 4 critical areas of concern: Espionage, Terrorism and
                          Violent Extremism, Cybersecurity, and Communalism. """,
                "messages": [
                    {
                        "role": "user",
                        "content":
                            f"""Provide the metadata of the text in the json format: 
                            'metadata': [
                                earliest_date: ,
                                terrorism": True/False,
                                cyber_security": True/False,
                                espionage": True/False,
                                communalism: True/False,
                                countries': []
                            ]
                            Here is the text:
                            {query}"""
                    }
                ]
            }
        )

    def extract_text_from_response(self, response) -> str :
        answer = json.loads(response['body'].read())
        return answer['content'][0]['text']

    def query(self, query: str) -> str:
        body = self.generate_query_body(query)
        response = self.client.invoke_model(
            body=body,
            modelId=self.modelId,
            contentType='application/json',
            accept='application/json'
        )
        # Got metadata about the response here, need to log or what? Idk im not SE
        return self.extract_text_from_response(response)
