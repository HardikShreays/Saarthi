import { useState } from 'react'
import './App.css'
import ChatUi from './components/chatUi.jsx'



function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    
    <ChatUi/>
    </>
  )
}

export default App
