import React, { act } from "react";
import { useState } from "react";
import { useEffect, useRef } from "react";

export default function ChatUi() {
  useEffect(() => {
    document.title = "🚀 Saarthi Chat";
  }, []);
  let [chats, setChats] = useState([]);
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(() => {
    scrollToBottom();
  }, [chats]);

  const handleKeyPress = (e) => {
    // console.log(e.key);
    if (e.key === "Enter") {
      e.preventDefault();
      sendMsg();
    }
  };
  async function sendMsg() {
    if (inputMsg.trim() === "") return;
  
    setChats((c) => [...c, { role: "user", parts: [inputMsg] }]);
    setInputMsg("");
  
    // Show "Typing..." indicator
    setChats((c) => [...c, { role: "model", parts: ["Typing..."] }]);
  
    try {
      let res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ role: "user", parts: [inputMsg] }),
      });
  
      const data = await res.json();
      console.log("Bot Response:", data);
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      // Update chat UI with actual response
      setChats((c) => {
        const newChats = c.filter(chat => chat.parts[0] !== "Typing...");
        return [...newChats, { role: "model", parts: [data.parts[0]] }];
      });
  
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  }
  
  
  useEffect( () => {
    async function fetchData() {
    const res = await fetch("http://127.0.0.1:5000/api/chat");
    const data = await res.json();
    setChats(data);
    // console.log(data);
  }
  fetchData();}
  ,[]);
  const [inputMsg, setInputMsg] = useState("");

  return (
    <div className="chat-ui">
      <div className="chat-ui-header">
        <h2>Chat with Saarthi</h2>
      </div>
      <div className="chat-ui-messages">
        {chats.map((chat, index) => (
          <div
            key={index}
            className={`chat-ui-message ${chat.role}`}
            style={{
              alignSelf: chat.role === "user" ? "flex-end" : "flex-start",
              backgroundColor: "#333",
              borderColor: chat.role === "user" ? "#007bff" : "#28a745",
              borderRadius: "10px",
              padding: "10px",
              margin: "5px 0",
              maxWidth: "70%",
            }}
          >
            {chat.parts[0]}
          </div>
        ))}
      </div>
      <div ref={messagesEndRef} />
      
      <div className="chat-ui-input">
        
        <input
          value={inputMsg}
          type="text"
          placeholder="Type your message..."
          onChange={(e) => setInputMsg(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button onClick={sendMsg}>Send</button>
        
      </div>
    </div>
  );
}
