import { useState } from 'react';

export default function PowerPointForm() {
  const [title, setTitle] = useState('');
  const [pages, setPages] = useState([
    { header: '', content: '', template: 'text', images: [''] }
  ]);

  const handlePageChange = (index: number, field: string, value: string) => {
    const updatedPages = [...pages];
    if (field === 'images') {
        updatedPages[index].images = value.split(',').map((s) => s.trim());
      } else {
        (updatedPages[index] as any)[field] = value;
      }
      setPages(updatedPages);
    };

  const addPage = () => {
    setPages([...pages, { header: '', content: '', template: 'text', images: [''] }]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = { title, pages };

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

        {pages.map((page, index) => (
          <div key={index} className="border p-4 rounded-md bg-gray-50">
            <h2 className="font-semibold mb-2">ページ {index + 1}</h2>
            <input
              type="text"
              placeholder="見出し（header）"
              value={page.header}
              onChange={(e) => handlePageChange(index, 'header', e.target.value)}
              className="mb-2 w-full px-2 py-1 border rounded"
            />
            <textarea
              placeholder="内容（content）"
              value={page.content}
              onChange={(e) => handlePageChange(index, 'content', e.target.value)}
              className="mb-2 w-full px-2 py-1 border rounded"
              rows={3}
            />
            <input
              type="text"
              placeholder="テンプレート（text, image, tableなど）"
              value={page.template}
              onChange={(e) => handlePageChange(index, 'template', e.target.value)}
              className="mb-2 w-full px-2 py-1 border rounded"
            />
            <input
              type="text"
              placeholder="画像URL（カンマ区切り）"
              value={page.images.join(', ')}
              onChange={(e) => handlePageChange(index, 'images', e.target.value)}
              className="mb-2 w-full px-2 py-1 border rounded"
            />
          </div>
        ))}

        <button
          type="button"
          onClick={addPage}
          className="py-1 px-3 bg-green-500 text-white rounded hover:bg-green-600"
        >
          ページを追加
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
