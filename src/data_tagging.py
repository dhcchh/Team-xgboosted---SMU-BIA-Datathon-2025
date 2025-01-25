import pandas as pd
import json
import sys

sys.path.append('./BedrockHelper')
from Bedrock_Wrapper import LLMQuery

def tagging_pipeline():
    NEWS_PATH = "./Dataset/news.csv"
    WIKILEAKS_PATH = "./Dataset/leaks.csv"
    S3_PROCESSED = ""
    
    BedrockWrapper = LLMQuery()

    news_df = pd.read_csv(NEWS_PATH)
    for i in range(news_df.shape[0]):
        text = news_df.iloc[i,0]
        try:
            response = Client.query(text)
        except Exception as e:
            print(f"Error invoking Bedrock Model: {e}")
            raise

        content = response['content'][0]['text']
        start_index = content.find('{')
        end_index = content.rfind('}')
        metadata_json = content[start_index:end_index + 1]
        metadata_dict = json.loads(metadata_json)

        file_content = {
        "text": "This is an example text discussing Singapore and China.",
        "metadata": {
            "countries": ["Singapore", "China"],
            "attributes": ["espionage"],
            "date": "2023-01-01"
            }
        }

        s3 = boto3.client("s3")
        s3.put_object(
            Bucket="your-bucket-name",
            Key="processed_data/text_001.json",
            Body=json.dumps(file_content),
            Tagging="countries=Singapore,China&attributes=espionage&date=2023-01-01"
        )
        



