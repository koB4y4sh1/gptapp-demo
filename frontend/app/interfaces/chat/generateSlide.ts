/**
 * スライド生成API
 */
export async function generateSlide(title: string, sessionId: string) {
  const res = await fetch("http://localhost:5000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, session_id: sessionId }),
  });

  if (!res.ok) {
    throw new Error("生成リクエストに失敗しました");
  }

  const data = await res.json();
  return {
    sessionId: data.session_id as string,
    preview: data.preview as string,
  };
}
