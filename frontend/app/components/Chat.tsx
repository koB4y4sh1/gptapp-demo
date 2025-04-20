import ChatMessageList from "./ChatMessageList";
import ChatInput from "./ChatInput";

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export type ChatStatus = "idle" | "loading" | "waiting_confirmation" | "confirmed" | "revising";

interface ChatProps {
  messages: ChatMessage[];
  input: string;
  status: ChatStatus;
  onInputChange: (value: string) => void;
  onSend: () => void;
  onConfirm: (isConfirmed: boolean) => void;
}

export default function Chat({
  messages,
  input,
  status,
  onInputChange,
  onSend,
  onConfirm,
}: ChatProps) {
  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">AIチャット</h1>
      <ChatMessageList messages={messages} />
      {status === "waiting_confirmation" && (
        <div className="text-center mt-4">
          <p>こちらの内容でよろしいでしょうか？</p>
          <button onClick={() => onConfirm(true)}>はい</button>
          <button onClick={() => onConfirm(false)}>いいえ</button>
        </div>
      )}
      <ChatInput
        value={input}
        isLoading={status === "loading"}
        onChange={onInputChange}
        onSubmit={onSend}
      />
    </div>
  );
}
