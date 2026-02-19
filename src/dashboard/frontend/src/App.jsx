import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Header from './components/Header'
import { useWebSocket } from './hooks/useWebSocket'
import Dashboard from './pages/Dashboard'
import SimplifiedView from './pages/SimplifiedView'

function AppLayout() {
  useWebSocket() // Inicia e mantém conexão WebSocket global

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <Header />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/simplified" element={<SimplifiedView />} />
      </Routes>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  )
}
