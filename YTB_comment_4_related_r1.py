from googleapiclient.discovery import build
from collections import Counter
import re

# API 키를 여기에 입력하세요.
API_KEY = "AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog"

# 검색어
SEARCH_KEYWORD = "한미 무역 협상"
MAX_RESULTS = 50  # 더 많은 결과 수집

def extract_keywords(text):
    """텍스트에서 한글, 영어, 숫자만 추출하여 반환합니다."""
    if text:
        return re.findall(r'[가-힣a-zA-Z0-9]+', text.lower())
    return []

try:
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=MAX_RESULTS,
        q=SEARCH_KEYWORD,
        type="video"
    )
    response = request.execute()

    keyword_counts = Counter()
    items = response.get("items", [])

    if not items:
        print("검색 결과가 없습니다.")
    else:
        print(f"'{SEARCH_KEYWORD}' 검색 결과:")
        for item in items:
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                channel_title = item["snippet"]["channelTitle"]
                publish_time = item["snippet"]["publishTime"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                title_keywords = extract_keywords(title)
                description_keywords = extract_keywords(item["snippet"].get("description", ""))
                tags = item["snippet"].get("tags", [])
                tag_keywords = [tag.lower() for tag in tags]

                all_keywords = title_keywords + description_keywords + tag_keywords
                keyword_counts.update(all_keywords)

                print("-" * 50)
                print(f"제목: {title}")
                print(f"채널: {channel_title}")
                print(f"게시일: {publish_time}")
                print(f"URL: {video_url}")
                print(f"추출된 키워드: {', '.join(all_keywords)}")

        print("\n" + "=" * 50)
        most_common_keywords = keyword_counts.most_common(50)
        print(f"'{SEARCH_KEYWORD}' 관련 상위 연관 검색어 (상위 50개, 전체 데이터 기반):")
        for keyword, count in most_common_keywords:
            print(f"- {keyword}: {count}")

except Exception as e:
    print(f"오류 발생: {e}")