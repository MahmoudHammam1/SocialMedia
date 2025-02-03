import requests
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

ACCESS_TOKEN = "access_token"
AD_ACCOUNT_ID = "act_ + busniess_account_id "
PAGE_ID = "page_id"


def create_campaign(ACCESS_TOKEN: str, AD_ACCOUNT_ID: str, name: str = "New Campaign",
                    objective: str = "OUTCOME_TRAFFIC", status: str = "PAUSED",
                    special_ad_categories: list = None):
    """
    Create a Facebook Ad Campaign.

    Parameters:
        access_token (str): Your Facebook API Access Token.
        ad_account_id (str): Your Facebook Ad Account ID (with 'act_' prefix).
        name (str): The name of the campaign.
        objective (str): The campaign objective (e.g., "OUTCOME_TRAFFIC", "CONVERSIONS").
        status (str): Campaign status ("PAUSED" or "ACTIVE"). Default is "PAUSED".
        special_ad_categories (list): List of categories like ["HOUSING"]. Default is empty.

    Returns:
        dict: The API response containing the Campaign ID or an error message.
    """
    if special_ad_categories is None:
        special_ad_categories = []

    URL = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/campaigns"

    campaign_data = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": special_ad_categories,
        "access_token": ACCESS_TOKEN,
    }

    response = requests.post(URL, data=campaign_data)
    data = response.json()

    if "id" in data:
        print(f"✅ Campaign Created Successfully! ID: {data['id']}")
        return data["id"]
    else:
        print("❌ Failed to create campaign:", data)
        return None


def campaign_data(ACCESS_TOKEN: str,
                  AD_ACCOUNT_ID: str,
                  CAMPAIGN_ID: str,
                  name: str = "Default Ad Set",
                  daily_budget: int = 500,
                  billing_event: str = "IMPRESSIONS",
                  optimization_goal: str = "LINK_CLICKS",
                  bid_strategy: str = "LOWEST_COST_WITHOUT_CAP",
                  countries: list = None,
                  age_min: int = 18,
                  age_max: int = 45,
                  genders: list = None,
                  status: str = "PAUSED"
                  ):
    """
    Creates a Facebook Ad Set dynamically.

    Parameters:
        access_token (str): Your Facebook API Access Token.
        ad_account_id (str): Your Facebook Ad Account ID (with 'act_' prefix).
        campaign_id (str): The Campaign ID where this Ad Set belongs.
        name (str): The Ad Set name.
        daily_budget (int): The daily budget in cents (e.g., 500 = $5).
        billing_event (str): How you are charged (e.g., "IMPRESSIONS", "LINK_CLICKS").
        optimization_goal (str): The optimization goal (e.g., "LINK_CLICKS", "CONVERSIONS").
        bid_strategy (str): The bidding strategy (e.g., "LOWEST_COST_WITHOUT_CAP").
        countries (list): List of country codes (e.g., ["US", "CA"]).
        age_min (int): Minimum age for targeting.
        age_max (int): Maximum age for targeting.
        genders (list): List of genders (1 = Male, 2 = Female).
        status (str): Ad Set status ("PAUSED" or "ACTIVE").

    Returns:
        dict: The API response containing the Ad Set ID or an error message.
    """

    if countries is None:
        countries = ["EG"]

    if genders is None:
        genders = [1, 2]

    URL = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/adsets"

    adset_data = {
        "name": name,
        "campaign_id": CAMPAIGN_ID,
        "daily_budget": str(daily_budget),
        "billing_event": billing_event,
        "optimization_goal": optimization_goal,
        "bid_strategy": bid_strategy,
        "targeting": {
            "geo_locations": {"countries": countries},
            "age_min": age_min,
            "age_max": age_max,
            "genders": genders
        },
        "status": status,
        "access_token": ACCESS_TOKEN,
    }

    response = requests.post(URL, json=adset_data)
    data = response.json()

    if "id" in data:
        print(f"✅ Ad Set Created Successfully! ID: {data['id']}")
        return data["id"]
    else:
        print("❌ Failed to create Ad Set:", data)
        return None


def create_page_post(ACCESS_TOKEN: str, PAGE_ID: str,
                     content: str, link: str = None, media_url: str = None):
    """
    Creates a post on a Facebook Page via API.

    Parameters:
        access_token (str): Facebook API Access Token (Page Access Token).
        page_id (str): Facebook Page ID.
        message (str): The text content of the post.
        link (str, optional): A URL to include in the post (default: None).
        media_url (str, optional): Image or Video URL to attach to the post (default: None).

    Returns:
        dict: API response containing the post ID or error message.
    """

    URL = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"

    post_data = {
        "message": content,
        "access_token": ACCESS_TOKEN,
    }

    if link:
        post_data["link"] = link

    if media_url:
        post_data["attached_media"] = [{"media_fbid": media_url}]

    response = requests.post(URL, data=post_data)
    data = response.json()

    if "id" in data:
        print(f"✅ Post Created Successfully! Post ID: {data['id']}")
        return data["id"]
    else:
        print("❌ Failed to create post:", data)
        return None


def ad_creative(ACCESS_TOKEN: str, AD_ACCOUNT_ID: str, POST_ID: str,
                name: str = "My Default Ad Creative"):
    """
    Links a Facebook Page Post to an Ad Creative.

    Parameters:
        access_token (str): Facebook API Access Token.
        ad_account_id (str): Facebook Ad Account ID (with 'act_' prefix).
        post_id (str): The ID of the existing Page Post to be used in the ad.
        name (str, optional): Name of the Ad Creative. Default is "My Test Ad Creative".

    Returns:
        str: Ad Creative ID if successful, None otherwise.
    """

    if not POST_ID:
        print("❌ Error: Invalid POST_ID")
        return None

    FacebookAdsApi.init(access_token=ACCESS_TOKEN)

    try:
        ad_creative = AdAccount(AD_ACCOUNT_ID).create_ad_creative(
            fields=[],
            params={
                "name": name,
                "object_story_id": POST_ID
            },
        )

        ad_creative_id = ad_creative.get("id")
        print(f"✅ Ad Creative Created Successfully! ID: {ad_creative_id}")
        return ad_creative_id

    except Exception as e:
        print(f"❌ Failed to create Ad Creative: {e}")
        return None


def create_ad(ACCESS_TOKEN: str, AD_ACCOUNT_ID: str,
              AD_SET_ID: str, AD_CREATIVE_ID: str,
              name: str = "New Ad", status: str = "PAUSED"):
    """
    Creates a Facebook Ad using an existing Ad Set and Ad Creative.

    Parameters:
        access_token (str): Facebook API Access Token.
        ad_account_id (str): Facebook Ad Account ID (with 'act_' prefix).
        ad_set_id (str): The ID of the Ad Set.
        ad_creative_id (str): The ID of the Ad Creative.
        name (str, optional): Name of the Ad. Default is "My Test Ad".
        status (str, optional): Status of the ad ("ACTIVE" or "PAUSED"). Default is "PAUSED".

    Returns:
        str: Ad ID if successful, None otherwise.
    """

    if not AD_SET_ID or not AD_CREATIVE_ID:
        print("❌ Error: Missing AD_SET_ID or AD_CREATIVE_ID")
        return None

    FacebookAdsApi.init(access_token=ACCESS_TOKEN)

    try:
        ad = AdAccount(AD_ACCOUNT_ID).create_ad(
            fields=[],
            params={
                "name": name,
                "adset_id": AD_SET_ID,
                "creative": {"creative_id": AD_CREATIVE_ID},
                "status": status,
            },
        )

        ad_id = ad.get("id")
        print(f"✅ Ad Created Successfully! ID: {ad_id}")
        return ad_id

    except Exception as e:
        print(f"❌ Failed to create Ad: {e}")
        return None
