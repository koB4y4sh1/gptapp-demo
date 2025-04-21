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
    <div className="flex flex-col h-screen max-h-screen max-w-screen  bg-white dark:bg-gray-800">
      <h1 className="text-2xl font-bold mb-4 text-center pt-4">AIチャット</h1>
      <div className="flex-1 overflow-y-auto px-4 pb-4">
        <ChatMessageList messages={messages} />

        {/* スライド構成プレビュー */}
        {slideStructure && Array.isArray(slideStructure) && (
          <div className="my-6 p-4 border rounded-lg bg-white dark:bg-gray-300 shadow-sm max-h-72 overflow-y-auto">
            <h2 className="text-lg font-semibold text-gray-700 mb-3 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 17v-2a4 4 0 014-4h4m0 0V7a4 4 0 00-4-4H7a4 4 0 00-4 4v10a4 4 0 004 4h4"></path></svg>
              スライド構成プレビュー
            </h2>
            <ol className="list-decimal list-inside space-y-2">
              {slideStructure.map((slide, idx) => (
                <li key={idx} className="pl-2 py-1 border-l-4 dark:text-gray-700 border-blue-200 bg-blue-50 rounded">
                  {slide.header
                    ? <span className="font-bold text-blue-700">{typeof slide.header === "string" ? slide.header : JSON.stringify(slide.header)}</span>
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
          <div className="text-center mt-6 flex flex-col items-center gap-3">
            <p className="mb-2 text-base font-medium text-gray-700">こちらの内容でよろしいでしょうか？</p>
            <div className="flex gap-4">
              <button
                onClick={() => onConfirm(true)}
                className="px-6 py-2 rounded bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              >
                はい
              </button>
              <button
                onClick={() => onConfirm(false)}
                className="px-6 py-2 rounded bg-gray-200 text-gray-700 font-semibold shadow hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 transition"
              >
                いいえ
              </button>
            </div>
          </div>
        )}
      </div>
      <div className="px-4 pb-4 pt-2 ">
        <ChatInput
          value={input}
          isLoading={status === "loading"}
          onChange={onInputChange}
          onSubmit={onSend}
        />
      </div>
    </div>
  );
}
