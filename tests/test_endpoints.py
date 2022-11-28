from datetime import datetime

from starlette import status

from src.config.settings import Settings

class TestEndpoints:
    def get_url(self):
        return f'https://{Settings.DEVICE_HOST}:{Settings.DEVICE_PORT}'

    async def test_get_data(self, api_client):
        url = self.get_url() + '/getdata'
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
