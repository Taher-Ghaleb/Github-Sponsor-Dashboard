/**
 * Mock API responses for testing
 */

export const mockUserData = {
  id: 1,
  username: 'testuser',
  name: 'Test User',
  type: 'User',
  gender: 'Male',
  location: 'United States',
  followers: 100,
  following: 50,
  public_repos: 25,
  total_sponsors: 10,
  total_sponsoring: 5,
  estimated_earnings: 500,
  avatar_url: 'https://example.com/avatar.png',
}

export const mockUsersResponse = {
  users: [mockUserData],
  total: 1,
  page: 1,
  per_page: 10,
}

export const mockStatsResponse = {
  total_users: 1000,
  total_sponsorships: 5000,
  top_sponsoring: {
    username: 'topsponsor',
    avatar_url: 'https://example.com/avatar.png',
    total_sponsoring: 100,
  },
  top_sponsored: {
    username: 'topsponsored',
    avatar_url: 'https://example.com/avatar2.png',
    total_sponsors: 200,
  },
}

export const mockQueueResponse = [
  {
    github_id: 12345,
    priority: 5,
    created_at: '2024-01-01T00:00:00',
  },
]
