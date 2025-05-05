from googleapiclient.discovery import build

# API 키를 여기에 입력하세요.
API_KEY = "AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog"

# 검색어
SEARCH_KEYWORD = "상상영어 동물농장"

try:
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=100,  # 가져올 최대 결과 수
        q=SEARCH_KEYWORD
    )
    response = request.execute()

    items = response.get("items", [])

    if not items:
        print("검색 결과가 없습니다.")
    else:
        for item in items:
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                channel_title = item["snippet"]["channelTitle"]
                publish_time = item["snippet"]["publishTime"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                print(f"제목: {title}")
                print(f"채널: {channel_title}")
                print(f"게시일: {publish_time}")
                print(f"URL: {video_url}")
                print("-" * 30)

except Exception as e:
    print(f"오류 발생: {e}")