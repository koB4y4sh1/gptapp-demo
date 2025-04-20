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
  slideStructure?: any[]; // スライド構成プレビュー
}

export default function Chat({
  messages,
  input,
  status,
  onInputChange,
  onSend,
  onConfirm,
  slideStructure,
}: ChatProps) {
  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">AIチャット</h1>
      <ChatMessageList messages={messages} />

      {/* スライド構成プレビュー */}
      {slideStructure && Array.isArray(slideStructure) && (
        <div className="my-6 p-4 border rounded bg-gray-50">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">スライド構成プレビュー</h2>
          <ol className="list-decimal list-inside space-y-1">
            {slideStructure.map((slide, idx) => (
              <li key={idx}>
                {/* タイトル・ヘッダー等をstring化して表示 */}
                {slide.header
                  ? <span className="font-bold text-gray-700">{typeof slide.header === "string" ? slide.header : JSON.stringify(slide.header)}</span>
                  : <span>スライド{idx + 1}</span>
                }
                {slide.template && (
                  <div className="text-xs text-gray-500 ml-4">
                    [template] {typeof slide.template === "string"
                      ? slide.template
                      : JSON.stringify(slide.template)}
                  </div>
                )}
              </li>
            ))}
          </ol>
        </div>
      )}

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
