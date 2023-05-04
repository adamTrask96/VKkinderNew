import vk_api
import pandas as pd
from config.config import vk_access_token, access_token_group, group_id

def get_top_photos(owner_id):
    '''Returns the top three photos for a user or group, sorted by number of likes.'''
    photos_dict = {}
    vk = vk_api.VkApi(token=vk_access_token)
    try:
        response = vk.method('photos.getAll',
                              {'owner_id': owner_id,
                               'extended': 1,
                               'count': 200})
    except vk_api.ApiError as e:
        print(f"Error while requesting photos from API: {e}")
        return None
    
    for item in response['items']:
        try:
            m = 0
            for i in item['sizes']:
                if i['height'] > m:
                    m = i['height']
                    url = i['url']
            photos_dict[item['id']] = {'url': url,
                                       'likes': item['likes']['count']}
        except KeyError as e:
            print(f"Error while processing photo data: {e}")
            continue

    df = pd.DataFrame(photos_dict)
    data = df.transpose()
    data = data.sort_values(by='likes', ascending=False)
    top_photos = data.head(3)
    return top_photos.to_dict('index')


def get_messages_upload_server():
    '''Returns the upload server URL for group messages.'''
    vk = vk_api.VkApi(token=access_token_group)
    try:
        response = vk.method('photos.getMessagesUploadServer',
                              {'group_id': group_id})
    except vk_api.ApiError as e:
        print(f"Error while requesting upload server from API: {e}")
        return None
    
    return response
