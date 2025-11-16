import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

interface User {
  id: number;
  username: string;
  email: string;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    // Get user from localStorage
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login', { replace: true })
  }

  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Bienvenue sur Immobilier</h1>
        <button 
          onClick={handleLogout}
          style={{
            padding: '0.5rem 1rem',
            background: '#e74c3c',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>

      {user && (
        <div style={{ marginBottom: '1rem', padding: '1rem', background: '#f0f0f0', borderRadius: '4px' }}>
          <p>Connecté en tant que: <strong>{user.username}</strong> ({user.email})</p>
        </div>
      )}

      <p>Application Full-Stack avec React + TypeScript et FastAPI</p>
    </div>
  )
}
