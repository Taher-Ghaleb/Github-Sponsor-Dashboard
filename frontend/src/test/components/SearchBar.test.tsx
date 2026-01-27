/**
 * Tests for SearchBar component
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SearchBar from '../../components/SearchBar'
import { TestWrapper } from '../TestWrapper'

describe('SearchBar', () => {
  const mockOnSubmit = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders search input', () => {
    render(
      <TestWrapper>
        <SearchBar onSubmit={mockOnSubmit} />
      </TestWrapper>
    )

    const input = screen.getByPlaceholderText('Search by name or username')
    expect(input).toBeInTheDocument()
  })

  it('updates search term on input change', async () => {
    const user = userEvent.setup()
    render(
      <TestWrapper>
        <SearchBar onSubmit={mockOnSubmit} />
      </TestWrapper>
    )

    const input = screen.getByPlaceholderText('Search by name or username')
    await user.type(input, 'test query')

    expect(input).toHaveValue('test query')
  })

  it('calls onSubmit after debounce delay', async () => {
    vi.useFakeTimers()
    const user = userEvent.setup({ delay: null })
    
    render(
      <TestWrapper>
        <SearchBar onSubmit={mockOnSubmit} />
      </TestWrapper>
    )

    const input = screen.getByPlaceholderText('Search by name or username')
    await user.type(input, 'test')

    // Fast-forward time to trigger debounce
    vi.advanceTimersByTime(1500)

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith('test')
    })

    vi.useRealTimers()
  })

  it('clears search term when clear button is clicked', async () => {
    const user = userEvent.setup()
    render(
      <TestWrapper>
        <SearchBar onSubmit={mockOnSubmit} />
      </TestWrapper>
    )

    const input = screen.getByPlaceholderText('Search by name or username')
    await user.type(input, 'test query')

    // Find and click clear button (Ant Design Input with allowClear)
    const clearButton = screen.getByRole('button', { hidden: true })
    await user.click(clearButton)

    expect(input).toHaveValue('')
  })
})
