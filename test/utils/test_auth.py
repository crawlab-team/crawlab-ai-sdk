import os
from unittest.mock import patch, mock_open
from crawlab_ai.utils import auth


def test_set_token_creates_directory_and_file():
    with patch('os.path.exists', return_value=False), patch('os.makedirs'), patch('builtins.open',
                                                                                  new_callable=mock_open):
        auth.set_token('test_token')
        os.makedirs.assert_called_once_with(auth.ROOT_DIRECTORY)
        open.assert_called_once_with(f'{auth.ROOT_DIRECTORY}/token', 'w')


def test_set_token_writes_token_to_file():
    with patch('os.path.exists', return_value=True), patch('builtins.open', new_callable=mock_open) as new_mock_open:
        auth.set_token('test_token')
        new_mock_open().write.assert_called_once_with('test_token')


def test_get_token_returns_env_var_token():
    with patch.dict(os.environ, {'CRAWLAB_TOKEN': 'env_token'}):
        assert auth.get_token() == 'env_token'


def test_get_token_returns_file_token():
    with patch('os.path.exists', return_value=True), patch('builtins.open', new_callable=mock_open,
                                                           read_data='file_token'):
        assert auth.get_token() == 'file_token'


def test_get_token_prompts_for_token():
    with patch('os.path.exists', return_value=False), patch('builtins.input', return_value='input_token'), patch(
            'crawlab_ai.utils.auth.set_token') as mock_set_token:
        assert auth.get_token() == 'input_token'
        mock_set_token.assert_called_once_with('input_token')
