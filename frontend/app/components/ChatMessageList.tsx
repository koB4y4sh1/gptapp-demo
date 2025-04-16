import ChatMessage from "./ChatMessage";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface ChatMessageListProps {
  messages: ChatMessage[];
}

export default function ChatMessageList({ messages }: ChatMessageListProps) {
  return (
    <div className="space-y-4 mb-6">
      {messages.map((msg, idx) => (
        <ChatMessage key={idx} role={msg.role} content={msg.content} />
      ))}
    </div>
  );
} 