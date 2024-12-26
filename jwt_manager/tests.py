from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import AsyncMock, patch


class DocumentViewsTests(APITestCase):
    @patch('httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_upload_document(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json.return_value = {'success': True}
        mock_response.status_code = 200
        mock_post.return_value.__aenter__.return_value = mock_response

        url = reverse('upload')
        with open('test_file.txt', 'w') as f:
            f.write('test content')

        with open('test_file.txt', 'rb') as f:
            response = await self.client.post(url, {'file': f}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'success': True})

    @patch('httpx.AsyncClient.delete', new_callable=AsyncMock)
    async def test_delete_document(self, mock_delete):
        mock_response = AsyncMock()
        mock_response.json.return_value = {'success': True}
        mock_response.status_code = 200
        mock_delete.return_value.__aenter__.return_value = mock_response

        url = reverse('delete', args=[1])
        response = await self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'success': True})

    @patch('httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_analyse_document(self, mock_post):
        mock_response = AsyncMock()
        mock_response.json.return_value = {'analysis': 'result'}
        mock_response.status_code = 200
        mock_post.return_value.__aenter__.return_value = mock_response

        url = reverse('analyse', args=[1])
        response = await self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'analysis': 'result'})

    @patch('httpx.AsyncClient.get', new_callable=AsyncMock)
    async def test_get_text_document(self, mock_get):
        mock_response = AsyncMock()
        mock_response.json.return_value = {'text': 'sample text'}
        mock_response.status_code = 200
        mock_get.return_value.__aenter__.return_value = mock_response

        url = reverse('get_text', args=[1])
        response = await self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'text': 'sample text'})
