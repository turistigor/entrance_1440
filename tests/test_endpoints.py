from starlette import status

from src.config.settings import Settings

class TestEndpoints:
    def get_url(self):
        return f'{Settings.DEVICE_HOST}:{Settings.DEVICE_PORT}'

    async def test_get_data(self, client):
        resp = await client.get(self.get_url() + '/getdata')
        assert resp.status == status.HTTP_200_OK
