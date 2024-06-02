import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import Inputs from "./components/Inputs";

function App() {

  const [messages, setMessages] = useState([
    { user: true, content: "Нарисуй что-нибудь" },
    { user: false, imageUrl: "example.png" },
  ]);

  const handleUserInput = (inputValue) => {
    const newMessage = { user: true, content: inputValue };
    setMessages([...messages, newMessage]);
  };

  const handleAnswer = (value) => {
    const newMessage = { user: false, content: value };
    setMessages([...messages, newMessage]);
  };

  return (
    <div className="App">
      <div className="left-block">
        <div>
          <img src="logo.png" alt="лого" />
          <p>Designer Chat</p>
        </div>
      </div>
      <main>
        <ChatWindow messages={messages} />
        <Inputs handleUserInput={handleUserInput} handleAnswer={handleAnswer} />
      </main>
    </div>
  );
}

export default App;
