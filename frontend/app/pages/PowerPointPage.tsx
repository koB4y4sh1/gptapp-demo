import { useState } from 'react';
import { InputField } from '../components/InputField';
import { PageForm } from '../components/PageForm';

export default function PowerPointPage() {
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
        <InputField
          id="title"
          label="タイトル"
          value={title}
          onChange={setTitle}
          required
        />

        {pages.map((page, index) => (
          <PageForm
            key={index}
            index={index}
            page={page}
            onPageChange={handlePageChange}
          />
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