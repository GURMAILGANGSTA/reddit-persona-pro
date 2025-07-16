import aiohttp
import asyncio
import base64
from typing import Tuple, List, Dict, Optional

class RedditFetcher:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.base_url = 'https://oauth.reddit.com'
        self.token = None

    async def _get_token(self, session: aiohttp.ClientSession) -> str:
        """Get OAuth token from Reddit"""
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'User-Agent': self.user_agent
        }
        data = {'grant_type': 'client_credentials'}

        async with session.post(
            'https://www.reddit.com/api/v1/access_token',
            headers=headers,
            data=data
        ) as response:
            if response.status != 200:
                raise Exception(f"Failed to get token: {await response.text()}")
            result = await response.json()
            return result['access_token']

    async def _fetch_data(self, session: aiohttp.ClientSession, endpoint: str) -> List[Dict]:
        """Fetch data from Reddit API with pagination"""
        if not self.token:
            self.token = await self._get_token(session)

        headers = {
            'Authorization': f'Bearer {self.token}',
            'User-Agent': self.user_agent
        }
        items = []
        after = None

        while True:
            params = {'limit': 100}
            if after:
                params['after'] = after

            async with session.get(
                f"{self.base_url}{endpoint}",
                headers=headers,
                params=params
            ) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data: {await response.text()}")

                data = await response.json()
                children = data['data']['children']
                items.extend([child['data'] for child in children])

                after = data['data'].get('after')
                if not after or len(items) >= 1000:  # Limit to 1000 items
                    break

        return items

    async def fetch_user_content(self, username: str) -> Tuple[List[Dict], List[Dict]]:
        """Fetch user's posts and comments"""
        async with aiohttp.ClientSession() as session:
            posts = await self._fetch_data(session, f"/user/{username}/submitted")
            comments = await self._fetch_data(session, f"/user/{username}/comments")
            return posts, comments

    async def fetch_user_avatar(self, username: str) -> Optional[str]:
        """Fetch user's avatar image URL"""
        async with aiohttp.ClientSession() as session:
            if not self.token:
                self.token = await self._get_token(session)

            headers = {
                'Authorization': f'Bearer {self.token}',
                'User-Agent': self.user_agent
            }
            url = f"{self.base_url}/user/{username}/about"

            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"⚠️ Could not fetch avatar for user '{username}'")
                    return None

                data = await response.json()
                return data['data'].get('icon_img', None)
