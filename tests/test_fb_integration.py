from social_media.core import FacebookAdManager, FacebookPostManager


ACCESS_TOKEN = "facebook_page_access_token"
AD_ACCOUNT_ID = "act_ + ad_account_id"
PAGE_ID = "page_id"


#  Create A New Post
# A link is required in the post for the ad to be created
post_manager = FacebookPostManager(ACCESS_TOKEN, PAGE_ID)
new_post_id = post_manager.create_post(
    message="Post with link and Ad",
    link="https://lenaai.net"
)

# Create Campagin
# special_ad_categories is required
ad_manager = FacebookAdManager(ACCESS_TOKEN, AD_ACCOUNT_ID)
campaign_id = ad_manager.create_campaign(special_ad_categories=["HOUSING"])

# Create Ad Set
if campaign_id:
    ad_set_id = ad_manager.create_ad_set(campaign_id)

# Create Ad Creative
if new_post_id:
    ad_creative_id = ad_manager.create_ad_creative(new_post_id)

# Create The Ad
if ad_set_id and ad_creative_id:
    ad_id = ad_manager.create_ad(ad_set_id, ad_creative_id)