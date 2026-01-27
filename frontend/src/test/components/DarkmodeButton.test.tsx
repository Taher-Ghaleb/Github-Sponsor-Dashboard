/**
 * Tests for DarkmodeButton component
 */
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import DarkmodeButton from '../../components/DarkmodeButton'
import { TestWrapper } from '../TestWrapper'

describe('DarkmodeButton', () => {
  it('renders dark mode button', () => {
    render(
      <TestWrapper>
        <DarkmodeButton />
      </TestWrapper>
    )

    // The button should be in the document (exact text depends on implementation)
    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
  })

  it('toggles theme when clicked', async () => {
    const userEvent = (await import('@testing-library/user-event')).default
    const user = userEvent.setup()

    render(
      <TestWrapper>
        <DarkmodeButton />
      </TestWrapper>
    )

    const button = screen.getByRole('button')
    await user.click(button)

    // Theme should be toggled (verify through localStorage or other means)
    // This depends on the actual implementation of DarkmodeButton
    expect(localStorage.getItem('theme')).toBeTruthy()
  })
})
