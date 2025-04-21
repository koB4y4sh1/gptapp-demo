import { useState } from "react";
import type { MetaFunction } from "@remix-run/node";
import Chat, { ChatMessage, ChatStatus } from "../components/Chat";
import { generateSlide } from "../interfaces/chat/generateSlide";
import { confirmSlide } from "../interfaces/chat/confirmSlide";

export const meta: MetaFunction = () => {
  return [
    { title: "チャット - PowerPoint Generator" },
    { name: "description", content: "AIとチャットしてPowerPointスライドのアイデアを生成します" },
  ];
};

export default function ChatPage() {
  const [sessionId, setSessionId] = useState("");
  const [preview, setPreview] = useState("");
  const [slideStructure, setSlideStructure] = useState<any[] | null>(null);
  const [cancel, setCancel] = useState(false);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<ChatStatus>("idle");

  // メッセージ送信時
  const handleSend = async () => {
    if (!input.trim() || status !== "idle") return;

    const userMessage: ChatMessage = { role: "user", content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setStatus("loading");

    try {
      // 生成API呼び出し
      const data = await generateSlide(userMessage.content, sessionId);
      setSessionId(data.sessionId);
      setPreview(data.preview);

      // previewがJSONならパースしてスライド構成として保持
      let parsed = null;
      try {
        parsed = typeof data.preview === "string" ? JSON.parse(data.preview) : data.preview;
        console.log(parsed)
        if (Array.isArray(parsed)) {
          setSlideStructure(parsed);
        } else {
          setSlideStructure(null);
        }
      } catch {
        setSlideStructure(null);
      }

      const assistantMessage: ChatMessage = { role: "assistant", content: "以下のスライド構成でスライドを作成します。" };
      setMessages(prev => [...prev, assistantMessage]);
      setStatus("waiting_confirmation");
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "エラーが発生しました" }]);
      setStatus("idle");
    }
  };

  // 入力欄変更時
  const handleInputChange = (value: string) => {
    setInput(value);
  };

  // 確認ボタン押下時
  const handleConfirm = async (isConfirmed: boolean) => {
    setMessages(prev => [...prev, { role: "user", content: isConfirmed ? "はい" : "いいえ" }]);

    if (isConfirmed) {
      setStatus("confirmed");
      try {
        if (!sessionId) throw new Error("セッションIDがありません");
        const blob = await confirmSlide(sessionId, true);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "presentation.pptx";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        setMessages(prev => [
          ...prev,
          { role: "assistant", content: "プレゼンテーションをダウンロードしました。" },
        ]);
      } catch {
        setMessages(prev => [
          ...prev,
          { role: "assistant", content: "エラーが発生しました" },
        ]);
      }
      setStatus("idle");
    } else {
      setStatus("revising");
      setSlideStructure(null);
      setPreview("");
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: "訂正する内容を入力してください。" },
      ]);
      setStatus("idle");
    }
  };

  return (
    <div >
      <Chat
        messages={messages}
        input={input}
        status={status}
        onInputChange={handleInputChange}
        onSend={handleSend}
        onConfirm={handleConfirm}
        slideStructure={slideStructure ?? undefined}
      />
    </div>
  );
}
