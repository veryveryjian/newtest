# YOUR_API_KEY = "AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog"


# import requests
# from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
#
# # ─── 설정 ─────────────────────────────────────────
# HANDLE_URL = 'https://www.youtube.com/@GoogleSearchCentral'
# API_KEY    = 'AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog'  # 발급받은 YouTube Data API v3 키
# # ─────────────────────────────────────────────────
#
# def get_channel_id_from_handle(url: str) -> str:
#     """
#     1) 핸들 URL에 GET 요청 → <link rel="canonical"> 태그에서 채널 URL 획득
#     2) URL에서 마지막 요소(채널 ID) 반환
#     """
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     canonical = soup.find('link', rel='canonical')
#     if not canonical:
#         raise ValueError("Canonical 태그를 찾을 수 없습니다.")
#     return canonical['href'].rstrip('/').split('/')[-1]
#
# def fetch_all_videos(channel_id: str, api_key: str):
#     """
#     1) 채널의 업로드 플레이리스트 ID 조회
#     2) playlistItems.list로 페이지 단위로 반복 조회
#     3) (비디오ID, 제목) 리스트 반환
#     """
#     youtube = build('youtube', 'v3', developerKey=api_key)
#     # 채널의 uploads 플레이리스트 ID 조회
#     res_ch = youtube.channels().list(
#         part='contentDetails',
#         id=channel_id
#     ).execute()
#     uploads_id = res_ch['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#
#     videos = []
#     page_token = None
#     while True:
#         res_pl = youtube.playlistItems().list(
#             part='snippet',
#             playlistId=uploads_id,
#             maxResults=50,
#             pageToken=page_token
#         ).execute()
#         for item in res_pl['items']:
#             vid = item['snippet']['resourceId']['videoId']
#             title = item['snippet']['title']
#             videos.append((vid, title))
#
#         page_token = res_pl.get('nextPageToken')
#         if not page_token:
#             break
#
#     return videos
#
# def main():
#     # 1) 채널 ID 추출
#     channel_id = get_channel_id_from_handle(HANDLE_URL)
#     print(f"채널 ID: {channel_id}")
#
#     # 2) ALL 동영상 조회
#     videos = fetch_all_videos(channel_id, API_KEY)
#     print(f"총 영상 개수: {len(videos)}\n")
#     for vid, title in videos:
#         print(f"{vid} | {title}")
#
# if __name__ == '__main__':
#     main()
#


#

# import requests
# from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
#
# # ─── 설정 ─────────────────────────────────────────
# HANDLE_URL = 'https://www.youtube.com/@GoogleSearchCentral'
# API_KEY    = 'AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog'  # YouTube Data API v3 키
# TOP_N      = 5               # 가져올 영상 개수
# # ─────────────────────────────────────────────────
#
# def get_channel_id_from_handle(url: str) -> str:
#     """핸들 URL에서 <link rel="canonical"> 태그로 채널 ID 추출"""
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     canonical = soup.find('link', rel='canonical')
#     if not canonical:
#         raise RuntimeError("채널 ID를 포함한 canonical 태그를 찾을 수 없습니다.")
#     return canonical['href'].rstrip('/').split('/')[-1]
#
# def fetch_top_videos(channel_id: str, api_key: str, n: int):
#     """상위 n개 영상의 ID·제목·업로드일·조회수를 가져와 리스트로 반환"""
#     youtube = build('youtube', 'v3', developerKey=api_key)
#
#     # 1) 채널의 uploads 플레이리스트 ID 조회
#     res_ch = youtube.channels().list(
#         part='contentDetails',
#         id=channel_id
#     ).execute()
#     uploads_id = res_ch['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#
#     # 2) 플레이리스트 상위 n개 아이템 조회
#     res_pl = youtube.playlistItems().list(
#         part='snippet',
#         playlistId=uploads_id,
#         maxResults=n
#     ).execute()
#
#     videos = []
#     video_ids = []
#     for item in res_pl['items']:
#         vid = item['snippet']['resourceId']['videoId']
#         videos.append({
#             'videoId':    vid,
#             'title':      item['snippet']['title'],
#             'publishedAt':item['snippet']['publishedAt']
#         })
#         video_ids.append(vid)
#
#     # 3) 통계(statistics) 조회 → viewCount 병합
#     stats_res = youtube.videos().list(
#         part='statistics',
#         id=','.join(video_ids)
#     ).execute()
#     stats_map = { v['id']: v['statistics'] for v in stats_res['items'] }
#
#     for video in videos:
#         video['viewCount'] = stats_map.get(video['videoId'], {}).get('viewCount', 'N/A')
#
#     return videos
#
# def main():
#     # 채널 ID 추출
#     channel_id = get_channel_id_from_handle(HANDLE_URL)
#     print(f"채널 ID: {channel_id}\n")
#
#     # 상위 TOP_N개 영상 가져오기
#     top_videos = fetch_top_videos(channel_id, API_KEY, TOP_N)
#     print(f"가져온 영상 개수: {len(top_videos)}\n")
#     for v in top_videos:
#         print(f"{v['videoId']} | {v['title']} | 업로드일: {v['publishedAt']} | 조회수: {v['viewCount']}")
#
# if __name__ == '__main__':
#     main()
#
# import requests
# from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
#
# # ─── 설정 ─────────────────────────────────────────
# HANDLE_URL = 'https://www.youtube.com/@GoogleSearchCentral'
# API_KEY    = 'AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog'      # YouTube Data API v3 키
# TOP_N      = 5                   # 가져올 영상 개수
# # ─────────────────────────────────────────────────
#
# def get_channel_id_from_handle(url: str) -> str:
#     """핸들 URL에서 canonical 태그로 채널 ID 추출"""
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     canonical = soup.find('link', rel='canonical')
#     if not canonical:
#         raise RuntimeError("canonical 태그를 찾을 수 없습니다.")
#     return canonical['href'].rstrip('/').split('/')[-1]
#
# def get_uploads_playlist_id(youtube, channel_id: str) -> str:
#     """채널의 uploads 플레이리스트 ID 반환"""
#     res = youtube.channels().list(
#         part='contentDetails',
#         id=channel_id
#     ).execute()
#     return res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#
# def get_top_video_ids(youtube, uploads_playlist_id: str, n: int) -> list[str]:
#     """uploads 플레이리스트에서 상위 n개 비디오 ID 반환"""
#     res = youtube.playlistItems().list(
#         part='contentDetails',
#         playlistId=uploads_playlist_id,
#         maxResults=n
#     ).execute()
#     return [item['contentDetails']['videoId'] for item in res['items']]
#
# def fetch_video_metadata(youtube, video_ids: list[str]) -> list[dict]:
#     """
#     videos.list로 snippet, statistics, topicDetails 함께 호출
#     https://developers.google.com/youtube/v3/docs/videos/list
#     """
#     res = youtube.videos().list(
#         part='snippet,statistics,topicDetails',
#         id=','.join(video_ids)
#     ).execute()
#
#     videos = []
#     for item in res['items']:
#         snippet = item['snippet']
#         stats   = item.get('statistics', {})
#         topic   = item.get('topicDetails', {})
#
#         videos.append({
#             'videoId':             item['id'],
#             'title':               snippet.get('title'),
#             'description':         snippet.get('description'),
#             'tags':                snippet.get('tags', []),
#             'categoryId':          snippet.get('categoryId'),
#             'defaultLanguage':     snippet.get('defaultLanguage'),
#             'defaultAudioLanguage':snippet.get('defaultAudioLanguage'),
#             'localized':           snippet.get('localized', {}),
#             'viewCount':           stats.get('viewCount'),
#             'likeCount':           stats.get('likeCount'),
#             'favoriteCount':       stats.get('favoriteCount'),
#             'commentCount':        stats.get('commentCount'),
#             'topicIds':            topic.get('topicIds', []),
#             'relevantTopicIds':    topic.get('relevantTopicIds', []),
#         })
#     return videos
#
# def main():
#     # 1) 채널 ID 추출
#     channel_id = get_channel_id_from_handle(HANDLE_URL)
#     print(f"채널 ID: {channel_id}\n")
#
#     # 2) YouTube 클라이언트 생성
#     youtube = build('youtube', 'v3', developerKey=API_KEY)
#
#     # 3) uploads 플레이리스트 ID 획득
#     uploads_id = get_uploads_playlist_id(youtube, channel_id)
#
#     # 4) 상위 TOP_N개 비디오 ID 가져오기
#     video_ids = get_top_video_ids(youtube, uploads_id, TOP_N)
#
#     # 5) 메타데이터 조회
#     videos = fetch_video_metadata(youtube, video_ids)
#
#     # 6) 결과 출력
#     for v in videos:
#         print('─' * 80)
#         print(f"ID:             {v['videoId']}")
#         print(f"제목:           {v['title']}")
#         print(f"설명:           {v['description'][:100]}{'…' if len(v['description'])>100 else ''}")
#         print(f"태그:           {v['tags']}")
#         print(f"카테고리 ID:    {v['categoryId']}")
#         print(f"기본 언어:      {v['defaultLanguage']}")
#         print(f"오디오 언어:    {v['defaultAudioLanguage']}")
#         print(f"지역별 제목·설명: {v['localized']}")
#         print(f"조회수:         {v['viewCount']}")
#         print(f"좋아요 수:      {v['likeCount']}")
#         print(f"즐겨찾기 수:    {v['favoriteCount']}")
#         print(f"댓글 수:        {v['commentCount']}")
#         print(f"topicIds:       {v['topicIds']}")
#         print(f"relevantTopicIds:{v['relevantTopicIds']}")
#     print('─' * 80)
#
# if __name__ == '__main__':
#     main()
#

#
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# ─── 설정 ─────────────────────────────────────────
HANDLE_URL = 'https://www.youtube.com/@GoogleSearchCentral'
API_KEY    = 'AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog'  # YouTube Data API v3 키
TOP_N      = 5               # 가져올 영상 개수
# ─────────────────────────────────────────────────

def get_channel_id_from_handle(url: str) -> str:
    """핸들 URL에서 canonical 태그로 채널 ID 추출"""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    canonical = soup.find('link', rel='canonical')
    if not canonical:
        raise RuntimeError("canonical 태그를 찾을 수 없습니다.")
    return canonical['href'].rstrip('/').split('/')[-1]

def get_uploads_playlist_id(youtube, channel_id: str) -> str:
    """채널의 uploads 플레이리스트 ID 반환"""
    res = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    return res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_top_video_ids(youtube, uploads_playlist_id: str, n: int) -> list[str]:
    """uploads 플레이리스트에서 상위 n개 비디오 ID 반환"""
    res = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=n
    ).execute()
    return [item['contentDetails']['videoId'] for item in res['items']]

def fetch_video_metadata(youtube, video_ids: list[str]) -> list[dict]:
    """snippet, statistics 파트로 메타데이터 조회"""
    res = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids)
    ).execute()

    videos = []
    for item in res['items']:
        snip = item['snippet']
        stats = item.get('statistics', {})
        videos.append({
            'id':           item['id'],
            'title':        snip.get('title'),
            'description':  snip.get('description', ''),
            'tags':         snip.get('tags', []),
            'categoryId':   snip.get('categoryId'),
            'viewCount':    stats.get('viewCount'),
            'likeCount':    stats.get('likeCount'),
            'commentCount': stats.get('commentCount')
        })
    return videos

def main():
    # 1) 채널 ID 추출
    channel_id = get_channel_id_from_handle(HANDLE_URL)
    print(f"채널 ID: {channel_id}\n")

    # 2) YouTube 클라이언트 생성
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # 3) uploads 플레이리스트 ID 획득
    uploads_id = get_uploads_playlist_id(youtube, channel_id)

    # 4) 상위 TOP_N개 비디오 ID 가져오기
    video_ids = get_top_video_ids(youtube, uploads_id, TOP_N)

    # 5) 메타데이터 조회 및 출력
    videos = fetch_video_metadata(youtube, video_ids)
    for v in videos:
        print('-' * 60)
        print(f"ID:             {v['id']}")
        print(f"제목:           {v['title']}")
        print(f"설명:           {v['description'][:200]}{'…' if len(v['description'])>200 else ''}")
        print(f"태그:           {v['tags']}")
        print(f"카테고리 ID:    {v['categoryId']}")
        print(f"조회수:         {v['viewCount']}")
        print(f"좋아요 수:      {v['likeCount']}")
        print(f"댓글 수:        {v['commentCount']}")
    print('-' * 60)

if __name__ == '__main__':
    main()
