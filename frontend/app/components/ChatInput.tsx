interface ChatInputProps {
  value: string;
  isLoading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

export default function ChatInput({ value, isLoading, onChange, onSubmit }: ChatInputProps) {
  return (
    <div className="flex gap-2">
      <input
        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && onSubmit()}
        placeholder="メッセージを入力..."
        disabled={isLoading}
      />
      <button
        onClick={onSubmit}
        disabled={isLoading}
        className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-blue-300"
      >
        {isLoading ? "送信中..." : "送信"}
      </button>
    </div>
  );
} 