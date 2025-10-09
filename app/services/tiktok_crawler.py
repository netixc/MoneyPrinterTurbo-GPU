"""
TikTok/Douyin Video Search and Download Integration
Based on Douyin_TikTok_Download_API project

This implementation includes FREE video search using Douyin's API directly.
No TikHub payment required!
"""
import requests
import random
import time
from loguru import logger
from typing import List, Dict
from urllib.parse import urlencode, quote
from gmssl import sm3, func
from app.config import config


# English to Chinese keyword translation dictionary
# Updated to use more natural Chinese phrases commonly searched on Douyin
KEYWORD_TRANSLATIONS = {
    # Technology & Cyber (using natural phrases)
    "cyber future": "未来科技",
    "cyber future ai": "人工智能",
    "cyber future security": "网络安全",
    "cyber future wearables": "智能穿戴",
    "cyber future healthcare": "智慧医疗",
    "cyber future privacy": "隐私保护",

    # Individual words
    "cyber": "科技",
    "future": "未来",
    "technology": "科技",
    "ai": "人工智能",
    "artificial intelligence": "人工智能",
    "security": "安全",
    "cybersecurity": "网络安全",
    "privacy": "隐私",
    "data": "数据",
    "digital": "数字化",
    "internet": "互联网",
    "computer": "电脑",
    "software": "软件",
    "hardware": "硬件",
    "cloud": "云计算",
    "blockchain": "区块链",
    "cryptocurrency": "数字货币",
    "robot": "机器人",
    "automation": "自动化",
    "smart": "智能",
    "innovation": "创新",
    "tech": "科技",

    # Healthcare
    "healthcare": "医疗",
    "health": "健康",
    "medical": "医学",
    "hospital": "医院",
    "doctor": "医生",
    "medicine": "药物",
    "wearable": "可穿戴设备",
    "wearables": "可穿戴设备",
    "fitness": "健身",
    "wellness": "养生",

    # General
    "device": "设备",
    "phone": "手机",
    "mobile": "移动",
    "app": "应用",
    "network": "网络",
    "system": "系统",
    "platform": "平台",
    "service": "服务",
    "user": "用户",
    "information": "信息",
    "communication": "通讯",
    "gaming": "游戏",
    "entertainment": "娱乐",
    "education": "教育",
    "business": "商业",
    "finance": "金融",
    "social": "社交",
    "media": "媒体",
    "video": "视频",
    "music": "音乐",
    "food": "美食",
    "travel": "旅游",
    "lifestyle": "生活方式",
    "fashion": "时尚",
    "beauty": "美容",
    "sports": "体育",
    "nature": "自然",
    "science": "科学",
    "space": "太空",
    "car": "汽车",
    "city": "城市",
    "world": "世界",
}


class ABogus:
    """A-Bogus parameter generator for Douyin API (from Douyin_TikTok_Download_API)"""

    __arguments = [0, 1, 14]
    __end_string = "cus"
    __version = [1, 0, 1, 5]
    __browser = "1536|742|1536|864|0|0|0|0|1536|864|1536|864|1536|742|24|24|MacIntel"
    __reg = [1937774191, 1226093241, 388252375, 3666478592, 2842636476, 372324522, 3817729613, 2969243214]
    __str = {
        "s0": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        "s1": "Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
        "s2": "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=",
        "s3": "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe",
        "s4": "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe",
    }

    def __init__(self):
        self.chunk = []
        self.size = 0
        self.reg = self.__reg[:]
        self.ua_code = [76, 98, 15, 131, 97, 245, 224, 133, 122, 199, 241, 166, 79, 34, 90, 191, 128, 126, 122, 98, 66, 11, 14, 40, 49, 110, 110, 173, 67, 96, 138, 252]
        self.browser = self.__browser
        self.browser_len = len(self.browser)
        self.browser_code = [ord(char) for char in self.browser]

    @staticmethod
    def sm3_to_array(data) -> list:
        """Calculate SM3 hash and convert to int array. Supports both str and list input."""
        if isinstance(data, str):
            b = data.encode("utf-8")
        else:
            b = bytes(data)  # Convert List[int] to bytes
        h = sm3.sm3_hash(func.bytes_to_list(b))
        return [int(h[i: i + 2], 16) for i in range(0, len(h), 2)]

    @staticmethod
    def rc4_encrypt(plaintext, key):
        s = list(range(256))
        j = 0
        for i in range(256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            s[i], s[j] = s[j], s[i]
        i = j = 0
        cipher = []
        for k in range(len(plaintext)):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            t = (s[i] + s[j]) % 256
            cipher.append(chr(s[t] ^ ord(plaintext[k])))
        return ''.join(cipher)

    @classmethod
    def generate_string_1(cls):
        return cls.from_char_code(*[170, 85, 170, 0, 0, 0, 0, 0, 170, 85, 170, 0])

    @staticmethod
    def from_char_code(*args):
        return "".join(chr(code) for code in args)

    def generate_string_2(self, url_params: str) -> str:
        start_time = int(time.time() * 1000)
        end_time = start_time + random.randint(4, 8)
        # Double SM3 hash as per Douyin algorithm
        params_array = self.sm3_to_array(self.sm3_to_array(url_params + self.__end_string))
        method_array = self.sm3_to_array(self.sm3_to_array("GET" + self.__end_string))

        a = [
            44, (end_time >> 24) & 255, 0, 0, 0, 0, 24, params_array[21], method_array[21],
            0, self.ua_code[23], (end_time >> 16) & 255, 0, 0, 0, 1, 0, 239, params_array[22],
            method_array[22], self.ua_code[24], (end_time >> 8) & 255, 0, 0, 0, 0,
            (end_time >> 0) & 255, 0, 0, 14, (start_time >> 24) & 255, (start_time >> 16) & 255,
            0, (start_time >> 8) & 255, (start_time >> 0) & 255, 3,
            int(end_time / 256 / 256 / 256 / 256) >> 0, 1,
            int(start_time / 256 / 256 / 256 / 256) >> 0, 1, self.browser_len, 0, 0, 0
        ]

        e = 0
        for i in a:
            e ^= i
        a.extend(self.browser_code)
        a.append(e)

        return self.rc4_encrypt(self.from_char_code(*a), "y")

    @classmethod
    def generate_result(cls, string, e="s4"):
        r = []
        for i in range(0, len(string), 3):
            if i + 2 < len(string):
                n = (ord(string[i]) << 16) | (ord(string[i + 1]) << 8) | ord(string[i + 2])
            elif i + 1 < len(string):
                n = (ord(string[i]) << 16) | (ord(string[i + 1]) << 8)
            else:
                n = ord(string[i]) << 16

            for j, k in zip(range(18, -1, -6), (0xFC0000, 0x03F000, 0x0FC0, 0x3F)):
                if j == 6 and i + 1 >= len(string):
                    break
                if j == 0 and i + 2 >= len(string):
                    break
                r.append(cls.__str[e][(n & k) >> j])

        r.append("=" * ((4 - len(r) % 4) % 4))
        return "".join(r)

    def get_value(self, url_params) -> str:
        if isinstance(url_params, dict):
            url_params = urlencode(url_params)
        string_1 = self.generate_string_1()
        string_2 = self.generate_string_2(url_params)
        string = string_1 + string_2
        return self.generate_result(string, "s4")


class TokenManager:
    """Generate necessary tokens for Douyin API"""

    @staticmethod
    def gen_mstoken() -> str:
        """Generate a fake msToken (real one requires API call, but fake works for search)"""
        base_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        return ''.join(random.choice(base_str) for _ in range(126)) + "=="

    @staticmethod
    def gen_verify_fp() -> str:
        """Generate verifyFp parameter"""
        base_str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        t = len(base_str)
        milliseconds = int(round(time.time() * 1000))
        base36 = ""
        while milliseconds > 0:
            remainder = milliseconds % 36
            if remainder < 10:
                base36 = str(remainder) + base36
            else:
                base36 = chr(ord("a") + remainder - 10) + base36
            milliseconds = int(milliseconds / 36)

        r = base36
        o = [""] * 36
        o[8] = o[13] = o[18] = o[23] = "_"
        o[14] = "4"

        for i in range(36):
            if not o[i]:
                n = int(random.random() * t)
                if i == 19:
                    n = 3 & n | 8
                o[i] = base_str[n]

        return "verify_" + r + "_" + "".join(o)


class TikTokCrawler:
    """
    TikTok/Douyin video crawler with FREE keyword search support
    """

    # Douyin API endpoints
    DOUYIN_DOMAIN = "https://www.douyin.com"
    VIDEO_SEARCH_ENDPOINT = f"{DOUYIN_DOMAIN}/aweme/v1/web/search/item/"

    def __init__(self):
        self.douyin_api_base = config.app.get("douyin_api_base", "https://api.douyin.wtf")
        self.tikhub_api_base = config.app.get("tikhub_api_base", "https://api.tikhub.io")
        self.use_tikhub = config.app.get("use_tikhub_api", False)
        self.tikhub_api_key = config.app.get("tikhub_api_key", "")
        self.douyin_cookie = config.app.get("douyin_cookie", "")

        # User-Agent for Douyin Web API
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

    @staticmethod
    def translate_to_chinese(keyword: str) -> str:
        """
        Translate English keywords to Chinese for Douyin search

        Args:
            keyword: English keyword or phrase

        Returns:
            Chinese translation or original if already Chinese
        """
        # If already contains Chinese characters, return as-is
        if any('\u4e00' <= c <= '\u9fff' for c in keyword):
            return keyword

        # Convert to lowercase for matching
        keyword_lower = keyword.lower().strip()

        # Try exact match first
        if keyword_lower in KEYWORD_TRANSLATIONS:
            chinese = KEYWORD_TRANSLATIONS[keyword_lower]
            logger.info(f"📝 Translated: '{keyword}' → '{chinese}'")
            return chinese

        # Try word-by-word translation for phrases
        words = keyword_lower.split()
        translated_words = []

        for word in words:
            # Remove common stop words
            if word in ["the", "a", "an", "and", "or", "of", "in", "on", "at", "to", "for"]:
                continue

            if word in KEYWORD_TRANSLATIONS:
                translated_words.append(KEYWORD_TRANSLATIONS[word])
            else:
                # Keep untranslated words as fallback
                translated_words.append(word)

        if translated_words:
            chinese = " ".join(translated_words)
            logger.info(f"📝 Translated: '{keyword}' → '{chinese}'")
            return chinese

        # Fallback: return original with warning
        logger.warning(f"⚠️  No translation found for '{keyword}', using as-is")
        return keyword

    def search_videos_by_keyword(
        self,
        keyword: str,
        count: int = 20,
        platform: str = "douyin"
    ) -> List[Dict]:
        """
        Search for videos by keyword

        Args:
            keyword: Search term
            count: Number of results to return
            platform: "douyin" or "tiktok"

        Returns:
            List of video metadata dictionaries
        """
        logger.info(f"Searching {platform} for keyword: {keyword}")

        if self.use_tikhub and self.tikhub_api_key:
            return self._search_tikhub(keyword, count, platform)
        else:
            # Use FREE direct Douyin API search
            if platform == "douyin":
                return self._search_douyin_direct(keyword, count)
            else:
                logger.warning("Free search only supports Douyin platform. Set tiktok_platform='douyin' in config")
                return []

    def _search_douyin_direct(self, keyword: str, count: int) -> List[Dict]:
        """
        FREE search using Douyin's API directly (no TikHub payment required!)
        """
        try:
            # Add random delay to avoid triggering anti-bot protection
            # This mimics human search behavior
            delay = random.uniform(1.5, 3.5)
            logger.info(f"⏱️  Waiting {delay:.1f}s before search (anti-bot protection)...")
            time.sleep(delay)

            logger.info(f"Using FREE Douyin API for keyword search: {keyword}")

            # Auto-translate English keywords to Chinese
            if keyword.isascii() and any(c.isalpha() for c in keyword):
                logger.info("🌐 Detected English keyword, translating to Chinese for Douyin...")
                keyword = self.translate_to_chinese(keyword)

            # Build request parameters
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "search_channel": "aweme_video_web",
                "sort_type": "0",
                "publish_time": "0",
                "keyword": keyword,
                "search_source": "tab_search",
                "query_correct_type": "1",
                "is_filter_search": "0",
                "from_group_id": "",
                "offset": "0",
                "count": str(count),
                "pc_client_type": "1",
                "version_code": "290100",
                "version_name": "29.1.0",
                "cookie_enabled": "true",
                "screen_width": "1920",
                "screen_height": "1080",
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Chrome",
                "browser_version": "130.0.0.0",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "130.0.0.0",
                "os_name": "Windows",
                "os_version": "10",
                "cpu_core_num": "12",
                "device_memory": "8",
                "platform": "PC",
                "downlink": "10",
                "effective_type": "4g",
                "round_trip_time": "0",
                "webid": TokenManager.gen_verify_fp(),
                "msToken": TokenManager.gen_mstoken(),
                "verifyFp": TokenManager.gen_verify_fp(),
                "fp": TokenManager.gen_verify_fp(),
            }

            # Generate A-Bogus parameter
            ab = ABogus()
            a_bogus = ab.get_value(params)

            # Build final URL with A-Bogus
            params["a_bogus"] = a_bogus
            url = f"{self.VIDEO_SEARCH_ENDPOINT}?{urlencode(params)}"

            # Request headers - mimic real browser
            headers = {
                "User-Agent": self.user_agent,
                "Referer": f"{self.DOUYIN_DOMAIN}/search/{quote(keyword)}",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Connection": "keep-alive",
            }

            # Add cookie if configured (required to bypass anti-bot verification)
            if self.douyin_cookie:
                headers["Cookie"] = self.douyin_cookie
                logger.info("🍪 Using configured Douyin cookie for authentication")
            else:
                logger.warning("⚠️  No Douyin cookie configured - may encounter verify_check errors")

            # Make request
            response = requests.get(
                url,
                headers=headers,
                proxies=config.proxy,
                verify=False,
                timeout=(30, 60)
            )

            if response.status_code == 200:
                data = response.json()
                logger.success(f"✓ FREE Douyin search successful!")

                # Log response for debugging (first 500 chars)
                import json
                response_preview = json.dumps(data, ensure_ascii=False)[:500]
                logger.debug(f"Response preview: {response_preview}...")

                return self._parse_douyin_search_results(data)
            else:
                logger.error(f"Douyin API error: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"Free Douyin search failed: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
            return []

    def _parse_douyin_search_results(self, data: Dict) -> List[Dict]:
        """Parse Douyin search results"""
        videos = []

        try:
            # Log the response structure for debugging
            logger.debug(f"Response keys: {list(data.keys())}")

            # Extract video list from response - handle multiple possible structures
            items = None

            # Try different response structures
            if "data" in data:
                data_content = data.get("data")
                if isinstance(data_content, list):
                    items = data_content
                elif isinstance(data_content, dict):
                    # Check for nested data
                    items = data_content.get("data", data_content.get("aweme_list", []))

            if not items:
                items = data.get("aweme_list", [])

            if not items:
                logger.warning(f"No video items found in response. Response structure: {data.keys()}")
                return []

            logger.debug(f"Found {len(items)} items to process")

            for item in items:
                # Handle different response structures
                aweme_info = item.get("aweme_info", item)

                # Extract video duration (in milliseconds)
                duration_ms = aweme_info.get("duration", 0)
                if not duration_ms:
                    duration_ms = aweme_info.get("video", {}).get("duration", 0)

                duration_sec = duration_ms / 1000 if duration_ms else 0

                # Extract video URL
                video_url = self._get_video_url(aweme_info)

                video_info = {
                    "video_id": aweme_info.get("aweme_id", ""),
                    "desc": aweme_info.get("desc", ""),
                    "duration": duration_sec,
                    "download_url": video_url,
                    "author": aweme_info.get("author", {}).get("nickname", ""),
                    "statistics": aweme_info.get("statistics", {})
                }

                if video_info["download_url"]:
                    videos.append(video_info)

            logger.info(f"Parsed {len(videos)} videos from Douyin search results")

        except Exception as e:
            logger.error(f"Failed to parse Douyin search results: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())

        return videos

    def _search_tikhub(self, keyword: str, count: int, platform: str) -> List[Dict]:
        """
        Search using TikHub API (paid service)
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.tikhub_api_key}",
                "Content-Type": "application/json"
            }

            if platform == "douyin":
                endpoint = f"{self.tikhub_api_base}/api/v1/douyin/web/fetch_video_search_result"
            else:
                endpoint = f"{self.tikhub_api_base}/api/v1/tiktok/web/fetch_video_search_result"

            params = {
                "keyword": keyword,
                "count": count,
                "offset": 0
            }

            response = requests.get(
                endpoint,
                headers=headers,
                params=params,
                proxies=config.proxy,
                verify=False,
                timeout=(30, 60)
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_douyin_search_results(data.get("data", {}))
            else:
                logger.error(f"TikHub API error: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            logger.error(f"TikHub search failed: {str(e)}")
            return []

    def _get_video_url(self, item: Dict) -> str:
        """Extract video download URL from item"""
        try:
            video = item.get("video", {})

            # Try different URL fields
            play_addr = video.get("play_addr", {})
            url_list = play_addr.get("url_list", [])

            if url_list:
                return url_list[0]

            # Fallback to bit_rate
            bit_rate = video.get("bit_rate", [])
            if bit_rate and len(bit_rate) > 0:
                play_addr = bit_rate[0].get("play_addr", {})
                url_list = play_addr.get("url_list", [])
                if url_list:
                    return url_list[0]

            return ""
        except Exception as e:
            logger.debug(f"Error extracting video URL: {e}")
            return ""

    def download_video(self, video_url: str, save_path: str) -> bool:
        """
        Download a TikTok/Douyin video

        Args:
            video_url: URL of the video
            save_path: Path to save the downloaded video

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Downloading video from: {video_url}")

            headers = {
                "User-Agent": self.user_agent,
                "Referer": f"{self.DOUYIN_DOMAIN}/"
            }

            response = requests.get(
                video_url,
                headers=headers,
                proxies=config.proxy,
                verify=False,
                timeout=(60, 240),
                stream=True
            )

            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                logger.success(f"Video downloaded: {save_path}")
                return True
            else:
                logger.error(f"Failed to download video: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            return False


if __name__ == "__main__":
    # Test the FREE crawler
    crawler = TikTokCrawler()
    results = crawler.search_videos_by_keyword("美食", count=5, platform="douyin")
    print(f"Found {len(results)} videos")
    for video in results:
        print(f"- {video['desc'][:50]}... ({video['duration']}s)")
