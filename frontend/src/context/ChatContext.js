import { createContext, useContext, useEffect, useState } from "react";

const ChatContext = createContext();

const ChatContextProvider = ({ children }) => {
  const [userToken, setUserToken] = useState("");

  return (
    <ChatContext.Provider value={{ userToken, setUserToken }}>
      {children}
    </ChatContext.Provider>
  );
};

export const ChatState = () => {
  return useContext(ChatContext);
};

export default ChatContextProvider;
