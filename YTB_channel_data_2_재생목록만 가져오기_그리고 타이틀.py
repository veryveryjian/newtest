
# API_KEY    = 'AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog'  # YouTube Data API v3 키
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# ─── 설정 ─────────────────────────────────────────
HANDLE_URL = 'https://www.youtube.com/@GoogleSearchCentral'
API_KEY    = 'AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog'   # YouTube Data API v3 키
# ─────────────────────────────────────────────────

def get_channel_id_from_handle(url: str) -> str:
    """핸들 URL에서 canonical 태그로 채널 ID 추출"""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    canonical = soup.find('link', rel='canonical')
    if not canonical:
        raise RuntimeError("canonical 태그를 찾을 수 없습니다.")
    return canonical['href'].rstrip('/').split('/')[-1]

def fetch_playlists(channel_id: str, api_key: str) -> list[dict]:
    """
    해당 채널의 재생목록 ID와 제목만 가져오기
    https://developers.google.com/youtube/v3/docs/playlists/list
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlists = []
    page_token = None

    while True:
        res = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=page_token
        ).execute()

        for item in res['items']:
            playlists.append({
                'playlistId': item['id'],
                'title':      item['snippet']['title']
            })

        page_token = res.get('nextPageToken')
        if not page_token:
            break

    return playlists

def main():
    # 1) 채널 ID 추출
    channel_id = get_channel_id_from_handle(HANDLE_URL)
    print(f"채널 ID: {channel_id}\n")

    # 2) 재생목록 조회
    playlists = fetch_playlists(channel_id, API_KEY)
    print(f"총 재생목록 개수: {len(playlists)}\n")
    for pl in playlists:
        print(f"{pl['playlistId']} | {pl['title']}")

if __name__ == '__main__':
    main()

#
# ###
# import requests
# from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
#
# # ─── 설정 ─────────────────────────────────────────
# HANDLE_URL = 'https://www.youtube.com/@GoogleSearchCentral'
# API_KEY    = 'AIzaSyCCDcqtKPJE46_IiHC-UHz6HHvwQ5muoog'   # YouTube Data API v3 키
# # ─────────────────────────────────────────────────
#
# def get_channel_id_from_handle(url: str) -> str:
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text, 'html.parser')
#     canonical = soup.find('link', rel='canonical')
#     if not canonical:
#         raise RuntimeError("canonical 태그를 찾을 수 없습니다.")
#     return canonical['href'].rstrip('/').split('/')[-1]
#
# def fetch_playlists(youtube, channel_id: str) -> list[dict]:
#     playlists = []
#     page_token = None
#     while True:
#         res = youtube.playlists().list(
#             part='snippet',
#             channelId=channel_id,
#             maxResults=50,
#             pageToken=page_token
#         ).execute()
#         for item in res['items']:
#             playlists.append({
#                 'playlistId': item['id'],
#                 'title':      item['snippet']['title']
#             })
#         page_token = res.get('nextPageToken')
#         if not page_token:
#             break
#     return playlists
#
# def fetch_playlist_videos(youtube, playlist_id: str) -> list[str]:
#     """
#     주어진 재생목록의 모든 비디오 제목을 반환
#     """
#     titles = []
#     page_token = None
#     while True:
#         res = youtube.playlistItems().list(
#             part='snippet',
#             playlistId=playlist_id,
#             maxResults=50,
#             pageToken=page_token
#         ).execute()
#         for item in res['items']:
#             titles.append(item['snippet']['title'])
#         page_token = res.get('nextPageToken')
#         if not page_token:
#             break
#     return titles
#
# def main():
#     # 1) 채널 ID 추출
#     channel_id = get_channel_id_from_handle(HANDLE_URL)
#     print(f"채널 ID: {channel_id}\n")
#
#     # 2) YouTube 클라이언트 생성
#     youtube = build('youtube', 'v3', developerKey=API_KEY)
#
#     # 3) 재생목록 조회
#     playlists = fetch_playlists(youtube, channel_id)
#     print(f"총 재생목록 개수: {len(playlists)}\n")
#
#     # 4) 각 재생목록 아래 비디오 제목 가져오기
#     for pl in playlists:
#         print(f"[{pl['title']}] ({pl['playlistId']})")
#         videos = fetch_playlist_videos(youtube, pl['playlistId'])
#         for idx, title in enumerate(videos, start=1):
#             print(f"  {idx}. {title}")
#         print('-' * 60)
#
# if __name__ == '__main__':
#     main()
