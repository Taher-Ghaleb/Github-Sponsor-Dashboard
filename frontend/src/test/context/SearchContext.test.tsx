/**
 * Tests for SearchContext
 */
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { SearchProvider, SearchContext } from '../../context/SearchContext'
import { useContext } from 'react'

// Test component that uses the search context
const TestComponent = () => {
  const context = useContext(SearchContext)
  if (!context) {
    return <div>No context</div>
  }
  const { searchTerm, setSearchTerm } = context
  return (
    <div>
      <span data-testid="search-term">{searchTerm}</span>
      <input
        data-testid="search-input"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
    </div>
  )
}

describe('SearchContext', () => {
  it('provides default empty search term', () => {
    render(
      <SearchProvider>
        <TestComponent />
      </SearchProvider>
    )

    expect(screen.getByTestId('search-term')).toHaveTextContent('')
  })

  it('updates search term when input changes', async () => {
    const userEvent = (await import('@testing-library/user-event')).default
    const user = userEvent.setup()

    render(
      <SearchProvider>
        <TestComponent />
      </SearchProvider>
    )

    const input = screen.getByTestId('search-input')
    await user.type(input, 'test query')

    expect(screen.getByTestId('search-term')).toHaveTextContent('test query')
  })

  it('allows clearing search term', async () => {
    const userEvent = (await import('@testing-library/user-event')).default
    const user = userEvent.setup()

    render(
      <SearchProvider>
        <TestComponent />
      </SearchProvider>
    )

    const input = screen.getByTestId('search-input')
    await user.type(input, 'test')
    await user.clear(input)

    expect(screen.getByTestId('search-term')).toHaveTextContent('')
  })
})
