import React from 'react';
import { InputField } from './InputField';

interface PageFormProps {
  index: number;
  page: {
    header: string;
    content: string;
    template: string;
    images: string[];
  };
  onPageChange: (index: number, field: string, value: string) => void;
}

export const PageForm: React.FC<PageFormProps> = ({ index, page, onPageChange }) => {
  return (
    <div className="border p-4 rounded-md bg-gray-50">
      <h2 className="font-semibold mb-2">ページ {index + 1}</h2>
      <InputField
        id={`header-${index}`}
        label="見出し"
        value={page.header}
        onChange={(value) => onPageChange(index, 'header', value)}
        placeholder="見出し（header）"
      />
      <InputField
        id={`content-${index}`}
        label="内容"
        value={page.content}
        onChange={(value) => onPageChange(index, 'content', value)}
        type="textarea"
        placeholder="内容（content）"
        rows={3}
      />
      <InputField
        id={`template-${index}`}
        label="テンプレート"
        value={page.template}
        onChange={(value) => onPageChange(index, 'template', value)}
        placeholder="テンプレート（text, image, tableなど）"
      />
      <InputField
        id={`images-${index}`}
        label="画像URL"
        value={page.images.join(', ')}
        onChange={(value) => onPageChange(index, 'images', value)}
        placeholder="画像URL（カンマ区切り）"
      />
    </div>
  );
}; 