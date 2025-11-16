import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Home from '@pages/Home'
import Login from '@pages/Login'
import ProfitabilitySimulator from '@pages/ProfitabilitySimulator'
import './App.css'

// Protected route component that checks token on every render
function ProtectedRoute({ element }: { element: React.ReactElement }) {
  const token = localStorage.getItem('token')
  if (!token) {
    return <Navigate to="/login" replace />
  }
  return element
}

function LoginRoute({ element }: { element: React.ReactElement }) {
  const token = localStorage.getItem('token')
  if (token) {
    return <Navigate to="/" replace />
  }
  return element
}

function App() {
  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={<LoginRoute element={<Login />} />} 
        />
        <Route 
          path="/" 
          element={<ProtectedRoute element={<Home />} />} 
        />
        <Route 
          path="/simulator" 
          element={<ProtectedRoute element={<ProfitabilitySimulator />} />} 
        />
      </Routes>
    </Router>
  )
}

export default App
