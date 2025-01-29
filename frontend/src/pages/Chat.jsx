import React, { useState, useEffect } from "react";
import Spinner from "../Loading/Spinners";
import { URL } from "../constants/constants";
import axios from "axios";
import { ChatState } from "../context/ChatContext";

function Chat() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchingLoading] = useState(false);

  // const { userToken } = ChatState();

  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchChatHistory = async () => {
      setFetchingLoading(true);
      try {
        const response = await axios.get(`${URL}/chat-history`);
        setHistory(response.data.chat_history);
        setFetchingLoading(false);
      } catch (error) {
        setFetchingLoading(false);
        console.error("Error fetching chat history:", error);
      }
    };

    fetchChatHistory();
    console.log(history);
  }, [token]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setChat((prevChat) => [...prevChat, { user: "You", message }]);
    try {
      setLoading(true);
      const response = await axios.post(
        `${URL}/query`,
        { user_query: message, token: token } // Passing user_id and message
      );
      setChat((prevChat) => [
        ...prevChat,
        { user: "Bot", message: response.data.response },
      ]);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error("Error sending message:", error);
    }
    setMessage("");
  };

  return (
    <div className="min-h-screen bg-blue-500 text-white p-6 flex flex-col items-center">
      <h2 className="text-xl font-bold">Welcome</h2>
      <h3>Start Your Sql Query eg: what products are available?</h3>

      <div className="chat-box bg-white text-black rounded-md p-4 w-full max-w-lg mt-5">
        {chat.map((c, index) => (
          <div
            key={index}
            className={c.user === "You" ? "chat-user" : "chat-bot"}
          >
            <strong>{c.user}:</strong> {c.message}
          </div>
        ))}
        {loading ? (
          <span className="fetch-load">
            <Spinner
              loading={loading}
              size={8}
              color={"black"}
              spinner={"sync"}
            />
          </span>
        ) : (
          ""
        )}
      </div>

      <form
        onSubmit={sendMessage}
        className="flex w-full max-w-lg mt-4 space-x-2"
      >
        <input
          type="text"
          className="flex-grow px-4 py-2 rounded-md border border-gray-300 text-black"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md"
        >
          Send
        </button>
      </form>

      <h3 className="text-lg font-bold mt-6">Chat History</h3>
      {fetchLoading ? (
        <div className="loading flex justify-center items-center">
          <Spinner
            loading={fetchLoading}
            size={92}
            color={"#000"}
            spinner={""}
          />
        </div>
      ) : (
        <div className="history-box bg-white text-black rounded-md p-4 w-full max-w-lg mt-4 overflow-y-auto max-h-72">
          {history.map((h, index) => (
            <div key={index} className="mb-4">
              <strong>You:</strong> {h.query} <br />
              <strong>Bot:</strong> {h.response} <br />
              <small>{new Date(h.createdAt).toLocaleString()}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Chat;
