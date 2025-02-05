import requests
import logging
import json
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class FacebookPostManager:
    """Handles Facebook Page posts."""

    def __init__(self, access_token, page_id):
        self.access_token = access_token
        self.page_id = page_id
        self.api_url = f"https://graph.facebook.com/v21.0/{self.page_id}/feed"

    def upload_photo(self, image_url):
        """
        Uploads an image to the Facebook Page.

        Parameters:
            image_url (str): The external image URL.

        Returns:
            str: Media ID if successful, None otherwise.
        """
        upload_url = f"https://graph.facebook.com/v21.0/{self.page_id}/photos"
        payload = {
            "url": image_url,
            "published": "false",
            "access_token": self.access_token
        }

        response = requests.post(upload_url, data=payload)
        data = response.json()

        if "id" in data:
            logging.info(f"✅ Image Uploaded Successfully! Media ID: {data['id']}")
            return data["id"]
        else:
            logging.error(f"❌ Failed to upload image: {data}")
            return None

    def create_post(self, message=None, link=None, media_url=None):
        """
        Creates a post on the Facebook Page.

        Parameters:
            message (str): The text content of the post.
            link (str, optional): A URL to include in the post.
            media_url (str, optional): A media file URL.

        Returns:
            str: Post ID if successful, None otherwise.
        """

        post_data = {"access_token": self.access_token}

        if message:
            post_data["message"] = message

        if link:
            post_data["link"] = link

        if media_url:
            media_id = self.upload_photo(media_url)
            if media_id:
                post_data["attached_media"] = json.dumps([{"media_fbid": media_id}])
            else:
                logging.error("❌ Image upload failed. Skipping media attachment.")
                return None

        if not ("message" in post_data or "link" in post_data or "attached_media" in post_data):
            logging.error("❌ Error: At least one of message, link, or media must be provided.")
            return None

        response = requests.post(self.api_url, data=post_data)
        data = response.json()

        if "id" in data:
            logging.info(f"✅ Post Created Successfully! Post ID: {data['id']}")
            return data["id"]
        else:
            logging.error(f"❌ Failed to create post: {data}")
            return None


class FacebookAdManager:
    """Handles Facebook Ads including campaigns, ad sets, creatives, and ads."""

    def __init__(self, access_token, ad_account_id):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        FacebookAdsApi.init(access_token=self.access_token)

    def create_campaign(self, name="New Campaign", objective="OUTCOME_TRAFFIC",
                        status="PAUSED", special_ad_categories=None):
        """
        Create a Facebook Ad Campaign.

        Parameters:
            name (str): The name of the campaign.
            objective (str): The campaign objective (e.g., "OUTCOME_TRAFFIC", "CONVERSIONS").
            status (str): Campaign status ("PAUSED" or "ACTIVE"). Default is "PAUSED".
            special_ad_categories (list): List of categories like ["HOUSING"]. Default is empty.

        Returns:
            dict: The API response containing the Campaign ID or an error message.
        """

        if special_ad_categories is None:
            logging.error(f"❌ Failed to create campaign: special_ad_categories parameter is required")

        url = f"https://graph.facebook.com/v19.0/{self.ad_account_id}/campaigns"
        campaign_data = {
            "name": name,
            "objective": objective,
            "status": status,
            "special_ad_categories": special_ad_categories,
            "access_token": self.access_token,
        }

        response = requests.post(url, data=campaign_data)
        data = response.json()

        if "id" in data:
            logging.info(f"✅ Campaign Created Successfully! ID: {data['id']}")
            return data["id"]
        else:
            logging.error(f"❌ Failed to create campaign: {data}")
            return None

    def create_ad_set(self, campaign_id,
                      name="Default Ad Set",
                      daily_budget=500,
                      billing_event="IMPRESSIONS",
                      optimization_goal="LINK_CLICKS",
                      bid_strategy="LOWEST_COST_WITHOUT_CAP",
                      countries=None,
                      age_min=18,
                      age_max=45,
                      genders=None,
                      status="PAUSED"
                      ):
        """
        Creates a Facebook Ad Set dynamically.

        Parameters:
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

        url = f"https://graph.facebook.com/v19.0/{self.ad_account_id}/adsets"
        adset_data = {
            "name": name,
            "campaign_id": campaign_id,
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
            "access_token": self.access_token,
        }

        response = requests.post(url, json=adset_data)
        data = response.json()

        if "id" in data:
            logging.info(f"✅ Ad Set Created Successfully! ID: {data['id']}")
            return data["id"]
        else:
            logging.error(f"❌ Failed to create Ad Set: {data}")
            return None

    def create_ad_creative(self, post_id, name="My Default Ad Creative"):
        """
        Links a Facebook Page Post to an Ad Creative.

        Parameters:
            post_id (str): The ID of the existing Page Post to be used in the ad.
            name (str, optional): Name of the Ad Creative. Default is "My Test Ad Creative".

        Returns:
            str: Ad Creative ID if successful, None otherwise.
        """

        if not post_id:
            logging.error("❌ Error: Invalid POST_ID")
            return None

        try:
            ad_creative = AdAccount(self.ad_account_id).create_ad_creative(
                fields=[],
                params={
                    "name": name,
                    "object_story_id": post_id
                }
            )
            ad_creative_id = ad_creative.get("id")
            logging.info(
                f"✅ Ad Creative Created Successfully! ID: {ad_creative_id}")
            return ad_creative_id
        except Exception as e:
            logging.error(f"❌ Failed to create Ad Creative: {e}")
            return None

    def create_ad(self, ad_set_id, ad_creative_id, name="New Ad", status="PAUSED"):
        """
        Creates a Facebook Ad using an existing Ad Set and Ad Creative.

        Parameters:
            ad_set_id (str): The ID of the Ad Set.
            ad_creative_id (str): The ID of the Ad Creative.
            name (str, optional): Name of the Ad. Default is "My Test Ad".
            status (str, optional): Status of the ad ("ACTIVE" or "PAUSED"). Default is "PAUSED".

        Returns:
            str: Ad ID if successful, None otherwise.
        """

        if not ad_set_id or not ad_creative_id:
            logging.error(
                "❌ Cannot create an ad. AD_SET_ID or AD_CREATIVE_ID is missing.")
            return None

        try:
            ad = AdAccount(self.ad_account_id).create_ad(
                fields=[],
                params={
                    "name": name,
                    "adset_id": ad_set_id,
                    "creative": {
                        "creative_id": ad_creative_id
                    },
                    "status": status
                }
            )
            ad_id = ad.get("id")
            logging.info(f"✅ Ad Created Successfully! ID: {ad_id}")
            return ad_id
        except Exception as e:
            logging.error(f"❌ Failed to create Ad: {e}")
            return None
