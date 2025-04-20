import { useState } from "react";
import ChatMessageList from "./ChatMessageList";
import ChatInput from "./ChatInput";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface ChatProps {
  onSendMessage: (message: string, confirmed: boolean) => Promise<string>;
}

export default function Chat({ onSendMessage }: ChatProps) {
  type ChatStatus = "idle" | "loading" | "waiting_confirmation" | "confirmed" | "revising";
  const [status, setStatus] = useState<ChatStatus>("idle");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || status !== "idle") return;
  
    const userMessage: ChatMessage = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setStatus("loading");
  
    try {
      const reply = await onSendMessage(input,false);
      const assistantMessage: ChatMessage = { role: "assistant", content: reply };
      setMessages(prev => [...prev, assistantMessage]);
      setStatus("waiting_confirmation");
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "エラーが発生しました" }]);
      setStatus("idle");
    }
  };

  const handleConfirmClick = async (isConfirmed: boolean) => {
    setMessages(prev => [...prev, { role: "user", content: isConfirmed ? "はい" : "いいえ" }]);
  
    if (isConfirmed) {
      setStatus("confirmed");
      const result = await onSendMessage("はい",true);
      setMessages(prev => [...prev, { role: "assistant", content: result }]);
      setStatus("idle");
    } else {
      setStatus("revising");
      setMessages(prev => [...prev, { role: "assistant", content: "訂正する内容を入力してください。" }]);
      setStatus("idle");
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">AIチャット</h1>
      <ChatMessageList messages={messages} />
      {status === "waiting_confirmation" && (
        <div className="text-center mt-4">
          <p>こちらの内容でよろしいでしょうか？</p>
          <button onClick={() => handleConfirmClick(true)}>はい</button>
          <button onClick={() => handleConfirmClick(false)}>いいえ</button>
        </div>
      )}
      <ChatInput
        value={input}
        isLoading={status==="loading"}
        onChange={setInput}
        onSubmit={handleSend}
      />
    </div>
  );
} 