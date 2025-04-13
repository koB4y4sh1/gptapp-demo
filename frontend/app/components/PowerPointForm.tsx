// app/components/PowerPointForm.tsx
import { useState } from 'react';

export default function PowerPointForm() {
  const [title, setTitle] = useState('');
  const [slides, setSlides] = useState([
    { section: '', content: '', image: '' }
  ]);

  const handleSlideChange = (index: number, field: string, value: string) => {
    const newSlides = [...slides];
    newSlides[index][field as keyof typeof newSlides[0]] = value;
    setSlides(newSlides);
  };

  const addSlide = () => {
    setSlides([...slides, { section: '', content: '', image: '' }]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = { title, slides };

    try {
      const res = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error('生成に失敗しました');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${title}.pptx`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert('生成に失敗しました。');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold text-center mb-6">PowerPoint資料自動生成フォーム</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium">タイトル</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>

        {slides.map((slide, index) => (
          <div key={index} className="border p-4 rounded-md bg-gray-50">
            <h2 className="font-semibold mb-2">スライド {index + 1}</h2>
            <input
              type="text"
              placeholder="セクション"
              value={slide.section}
              onChange={(e) => handleSlideChange(index, 'section', e.target.value)}
              className="mb-2 w-full px-2 py-1 border rounded"
            />
            <textarea
              placeholder="内容"
              value={slide.content}
              onChange={(e) => handleSlideChange(index, 'content', e.target.value)}
              className="mb-2 w-full px-2 py-1 border rounded"
              rows={3}
            />
            <input
              type="text"
              placeholder="画像URL (任意)"
              value={slide.image}
              onChange={(e) => handleSlideChange(index, 'image', e.target.value)}
              className="mb-2 w-full px-2 py-1 border rounded"
            />
          </div>
        ))}

        <button
          type="button"
          onClick={addSlide}
          className="py-1 px-3 bg-green-500 text-white rounded hover:bg-green-600"
        >
          スライドを追加
        </button>

        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          資料を生成する
        </button>

      </form>
    </div>
  );
}
