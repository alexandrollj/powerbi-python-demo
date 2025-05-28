import os
from dotenv import load_dotenv
import msal
import requests

# Load env variables
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
REPORT_ID = os.getenv("REPORT_ID")

# Constants
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
RESOURCE = "https://api.powerbi.com"


def get_access_token():
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if isinstance(result, dict):
        if "access_token" in result:
            return result["access_token"]
        else:
            error_msg = result.get("error_description", str(result))
    else:
        error_msg = str(result)

    raise Exception(f"Error getting access token: {error_msg}")


def get_embed_token():
    token = get_access_token()

    headers = {"Authorization": f"Bearer {token}", "Content-type": "application/json"}

    # We get the report information

    report_url = f"{RESOURCE}/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}"
    report_response = requests.get(report_url, headers=headers)
    report_response.raise_for_status()
    report_data = report_response.json()

    embed_url = report_data.get("embedUrl")
    report_id = report_data.get("id")
    report_name = report_data.get("name")

    # Generate embeded token
    token_url = (
        f"{RESOURCE}/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"
    )
    body = {"accessLevel": "View"}

    token_response = requests.post(token_url, headers=headers, json=body)
    print("🔍 Status Code:", token_response.status_code)
    print("🔍 Response Text:", token_response.text)
    token_response.raise_for_status()
    token_data = token_response.json()

    return {
        "embedToken": token_data["token"],
        "embedUrl": embed_url,
        "reportId": report_id,
        "reportTitle": report_name,
    }
