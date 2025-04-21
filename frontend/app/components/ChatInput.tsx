import { useRef } from "react";

interface ChatInputProps {
  value: string;
  isLoading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

export default function ChatInput({ value, isLoading, onChange, onSubmit }: ChatInputProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  // IME変換中Enter送信防止
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.nativeEvent.isComposing) {
      onSubmit();
    }
  };

  return (
    <div className="flex gap-2 mt-4">
      <div className="relative flex-1">
        <input
          ref={inputRef}
          className="w-full border border-gray-300 rounded-lg px-4 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="メッセージを入力..."
          disabled={isLoading}
        />
        {value && !isLoading && (
          <button
            type="button"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1 rounded focus:outline-none"
            onClick={() => {
              onChange("");
              inputRef.current?.focus();
            }}
            aria-label="入力をクリア"
            tabIndex={0}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
      <button
        onClick={onSubmit}
        disabled={isLoading || !value.trim()}
        className="flex items-center gap-2 bg-blue-600 text-white px-5 py-2 rounded-lg font-semibold shadow hover:bg-blue-700 disabled:bg-blue-300 transition min-w-[90px]"
      >
        {isLoading ? (
          <svg className="animate-spin h-5 w-5 mr-1 text-white" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        ) : (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        )}
        {isLoading ? "送信中..." : "送信"}
      </button>
    </div>
  );
}
