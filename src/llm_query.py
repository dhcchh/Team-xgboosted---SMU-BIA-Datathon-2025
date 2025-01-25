import boto3
import json
import os

from dotenv import load_dotenv


class LLMQuery:
    def __init__(self):
        load_dotenv()
        self.modelId = "anthropic.claude-3-haiku-20240307-v1:0"
        self.region_name = "ap-southeast-1"
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=self.region_name,
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )

    def generate_query_body(self, query: str) -> str:
        return json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": "You are an assistant helping Singapore's Internal Security Department (ISD) in addressing"
                          "four critical areas of concern: Espionage, Terrorism and Violent Extremism, Cybersecurity,"
                          "and Communalism. Using datasets from WikiLeaks articles and news excerpts, the goal is to"
                          "extract structured data to identify key entities, relationships, and incidents relevant to"
                          "Singapore’s internal security. The data may include unrelated global events (e.g., the"
                          "Taliban takeover in Afghanistan), but these are still valuable for identifying patterns,"
                          "trends, and lessons that could impact Singapore indirectly. By scoring relevance and"
                          "extracting actionable insights, ISD can prioritize risks, allocate resources effectively,"
                          "and maintain a proactive stance against both domestic and international security threats.",
                "messages": [
                    {
                        "role": "user",
                        "content":
                            f"Provide the output of the text in the format: "
                            f"- Entity "
                            f"- Type (Person, Organization, Location, Incident, Keyword) "
                            f"- Date (if mentioned) "
                            f"- Summary (brief overview of relevance to ISD's concerns)"
                            f"- Area of Concern (Espionage, Terrorism, Cybersecurity, Communalism)"
                            f"- Relevance Score (High, Medium, Low)"
                            f"- Relationships (if applicable, e.g., Person A linked to Organization B)."
                            f"Here is the text:"
                            f"{query}"
                    }
                ]
            }
        )

    def extract_text_from_response(self, response: dict) -> str:
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
