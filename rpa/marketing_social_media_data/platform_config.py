"""
平台配置文件
管理各社交媒体平台的字段映射关系
"""

# 各平台的标准化字段列表
PLATFORM_FIELDS = {
    "FaceBook": [
        "New Fans", "Posts Published", "Posts Impressions",
        "Posts Engagement", "Posts Reactions", "Posts Comments",
        "Posts Shares", "Posts Video Plays"
    ],
    "Youtube": [
        "Total Subscribers", "Subscribers Gained", "Engagement",
        "Views", "Post"
    ],
    "Instagram": [
        "Total Followers", "Total Interactions", "Total Views",
        "Total Reach", "Post Published"
    ],
    "LinkedIn": [
        "Total Followers-linkedin", "Total Posts", "Follower Growth",
        "Total Impressions", "Total Page Likes", "Total Page Clicks"
    ],
    "X": [
        "Followers", "Following", "Total Tweets"
    ]
}

# Facebook字段映射关系
FACEBOOK_FIELD_MAPPING = {
    "New Fans": "fb-fans",
    "Posts Published": "fb-post-published",
    "Posts Impressions": "fb-post-impressions",
    "Posts Engagement": "fb-post-engagement",
    "Posts Reactions": "fb-posts-reaction",
    "Posts Comments": "fb-post-comments-count",
    "Posts Shares": "fb-post-shares",
    "Posts Video Plays": "fb-post-video-views"
}

# Youtube字段映射关系（预留）
YOUTUBE_FIELD_MAPPING = {
    "Total Subscribers": "yt-subscribers",
    "Subscribers Gained": "yt-subscribers-gained",
    "Engagement": "yt-engagement",
    "Views": "yt-views",
    "Post": "yt-posts"
}

# Instagram字段映射关系（预留）
INSTAGRAM_FIELD_MAPPING = {
    "Total Followers": "ig-followers",
    "Total Interactions": "ig-interactions",
    "Total Views": "ig-views",
    "Total Reach": "ig-reach",
    "Post Published": "ig-posts"
}

# LinkedIn字段映射关系（预留）
LINKEDIN_FIELD_MAPPING = {
    "Total Followers-linkedin": "li-followers",
    "Total Posts": "li-posts",
    "Follower Growth": "li-growth",
    "Total Impressions": "li-impressions",
    "Total Page Likes": "li-likes",
    "Total Page Clicks": "li-clicks"
}

# X字段映射关系（预留）
X_FIELD_MAPPING = {
    "Followers": "x-followers",
    "Following": "x-following",
    "Total Tweets": "x-tweets"
}

# 平台文件映射
PLATFORM_FILES = {
    "facebook": "fb_fetch_inf.json",
    "youtube": "youtube_fetch_inf.json",
    "instagram": "instagram_fetch_inf.json",
    "linkedin": "linkedin_fetch_inf.json",
    "x": "x_fetch_inf.json"
}

# 输出文件映射
OUTPUT_FILES = {
    "facebook": "fb_fetch_inf_update.json",
    "youtube": "youtube_fetch_inf_update.json",
    "instagram": "instagram_fetch_inf_update.json",
    "linkedin": "linkedin_fetch_inf_update.json",
    "x": "x_fetch_inf_update.json"
}

def get_platform_fields(platform: str) -> list:
    """获取指定平台的字段列表"""
    return PLATFORM_FIELDS.get(platform, [])

def get_field_mapping(platform: str) -> dict:
    """获取指定平台的字段映射关系"""
    mapping_map = {
        "facebook": FACEBOOK_FIELD_MAPPING,
        "youtube": YOUTUBE_FIELD_MAPPING,
        "instagram": INSTAGRAM_FIELD_MAPPING,
        "linkedin": LINKEDIN_FIELD_MAPPING,
        "x": X_FIELD_MAPPING
    }
    return mapping_map.get(platform.lower(), {})

def get_platform_file(platform: str) -> str:
    """获取指定平台的输入文件名"""
    return PLATFORM_FILES.get(platform.lower(), "")

def get_output_file(platform: str) -> str:
    """获取指定平台的输出文件名"""
    return OUTPUT_FILES.get(platform.lower(), "") 