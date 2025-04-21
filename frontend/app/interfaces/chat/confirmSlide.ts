/**
 * スライド確認・ダウンロードAPI
 */
export async function confirmSlide(sessionId: string, confirmed: boolean) {
  const res = await fetch("http://localhost:5000/confirm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, confirmed }),
  });

  if (!res.ok) {
    throw new Error("確認リクエストに失敗しました");
  }

  const blob = await res.blob();
  return blob;
}
