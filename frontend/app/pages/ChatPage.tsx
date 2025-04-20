import { useState } from "react";
import type { MetaFunction } from "@remix-run/node";
import Chat from "../components/Chat";

export const meta: MetaFunction = () => {
  return [
    { title: "チャット - PowerPoint Generator" },
    { name: "description", content: "AIとチャットしてPowerPointスライドのアイデアを生成します" },
  ];
};

export default function ChatPage() {
  const [sessionId, setSessionId] = useState("");
  const [preview, setPreview] = useState("");
  const [cancel,setCancel] = useState(false);

  const handleGenerate = async (title: string) => {
    const res = await fetch("http://localhost:5000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, session_id: sessionId }),
    });

    if (!res.ok) {
      throw new Error("生成リクエストに失敗しました");
    }

    const data = await res.json();
    setSessionId(data.session_id);
    setPreview(data.preview);
    return data.preview;
  };

  const handleConfirm = async (confirmed: boolean) => {
    if (!sessionId) {
      throw new Error("セッションIDがありません");
    }

    const res = await fetch("http://localhost:5000/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, confirmed }),
    });

    if (!res.ok) {
      throw new Error("確認リクエストに失敗しました");
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "presentation.pptx";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const handleSendMessage = async (message: string, confirmed: boolean): Promise<string> => {
    if (!confirmed) {
      return await handleGenerate(message);
    } else {
      await handleConfirm(confirmed);
      return cancel ? "生成をキャンセルしました。" : "プレゼンテーションをダウンロードしました。";
    }
  };

  return <Chat onSendMessage={handleSendMessage} />;
} 