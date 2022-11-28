import json
from datetime import datetime

from starlette import status

from src.config.settings import Settings

class TestEndpoints:
    def get_url(self):
        return f'https://{Settings.DEVICE_HOST}:{Settings.DEVICE_PORT}'

    async def test_get_data(self, api_client):
        url = f'{self.get_url()}/getdata'
        resp = await api_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        channels = resp.json()['channels']
        assert len(channels) == 4
        for ch in channels:
            assert 1 <= ch['num'] <= 4
            assert isinstance(ch['current'], float)
            assert isinstance(ch['voltage'], float)
            try:
                datetime.fromisoformat(ch['update_dt'])
            except ValueError:
                assert False

    async def test_channel_on(self, api_client):
        url = f'{self.get_url()}/channelon'
        data = {
            'num': 3,
            'current': 5.1,
            'voltage': 5.2,
        }
        resp = await api_client.post(url=url, data=json.dumps(data))
        assert resp.status_code == status.HTTP_200_OK

    async def test_channel_off(self, api_client):
        url = f'{self.get_url()}/channeloff'
        resp = await api_client.post(url=url, data=json.dumps({'num': 3}))
        assert resp.status_code == status.HTTP_200_OK
