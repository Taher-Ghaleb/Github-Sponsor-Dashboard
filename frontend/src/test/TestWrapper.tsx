/**
 * Test wrapper component that provides all necessary context providers
 */
import { ReactNode } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '../context/ThemeContext'
import { SearchProvider } from '../context/SearchContext'

interface TestWrapperProps {
  children: ReactNode
}

export const TestWrapper = ({ children }: TestWrapperProps) => {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <SearchProvider>
          {children}
        </SearchProvider>
      </ThemeProvider>
    </BrowserRouter>
  )
}
