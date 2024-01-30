mock_user_data = {
    'login': 'mock_user',
    'id': 123456789,
    'node_id': 'MDQ6VXNlcjEzNzI1MDUy',
    'avatar_url': 'https://avatars.githubusercontent.com/u/123456789?v=4',
    'html_url': 'https://github.com/mock_user',
    'followers_url': 'https://api.github.com/users/mock_user/followers',
    'following_url': 'https://api.github.com/users/mock_user/following{/other_user}',
    'name': 'Mock User',
    'location': 'Mock City',
    'bio': 'A passionate coder',
    'public_repos': 10,
    'public_gists': 5,
    'followers': 20,
    'following': 15,
    'created_at': '2021-01-01T12:00:00Z',
    'updated_at': '2022-01-01T12:00:00Z',
}

mock_repo_data = [{
    'id': 987654321,
    'node_id': 'MDEwOlJlcG9zaXRvcnk5ODc2NTQzMjE=',
    'name': 'mock_repository',
    'full_name': 'mock_user/mock_repository',
    'private': False,
    'owner': {
        'login': 'mock_user',
        'id': 123456789,
        'avatar_url': 'https://avatars.githubusercontent.com/u/123456789?v=4',
        'html_url': 'https://github.com/mock_user',
        'site_admin': False,
    },
    'html_url': 'https://github.com/mock_user/mock_repository',
    'description': 'A mock repository for testing',
    'fork': False,
    'url': 'https://api.github.com/repos/mock_user/mock_repository',
    'forks_url': 'https://api.github.com/repos/mock_user/mock_repository/forks',
    'languages_url': 'https://api.github.com/repos/mock_user/mock_repository/languages',
    'stargazers_count': 15,
    'watchers_count': 10,
    'forks_count': 5,
    'open_issues_count': 2,
    'created_at': '2022-01-01T12:00:00Z',
    'updated_at': '2022-01-10T12:00:00Z',
}]

mock_processed_user_data = {
    'avatar_url': 'https://dummyavatars.com/example.jpg',
    'html_url': 'https://github.com/exampleuser',
    'login': 'exampleuser',
    'name': 'John Doe',
    'location': 'Dummy City, Dummy Country',
    'bio': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis tristique elit.',
    'repositories': [
        {
            'name': 'dummy-repo-1',
            'full_name': 'exampleuser/dummy-repo-1',
            'url': 'https://api.github.com/repos/exampleuser/dummy-repo-1',
            'description': 'Dummy repository 1 for testing purposes.'
        },
        {
            'name': 'dummy-repo-2',
            'full_name': 'exampleuser/dummy-repo-2',
            'url': 'https://api.github.com/repos/exampleuser/dummy-repo-2',
            'description': 'Dummy repository 2 for testing purposes.'
        },
        {
            'name': 'dummy-repo-3',
            'full_name': 'exampleuser/dummy-repo-3',
            'url': 'https://api.github.com/repos/exampleuser/dummy-repo-3',
            'description': 'Dummy repository 3 for testing purposes.'
        }
    ]
}