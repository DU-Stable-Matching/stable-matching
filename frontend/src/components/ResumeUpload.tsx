import React, { useState, useRef, DragEvent, ChangeEvent } from 'react';

interface ResumeUploadProps {
  onUpload?: (file: File) => Promise<void> | void;
}

const ResumeUpload: React.FC<ResumeUploadProps> = ({ onUpload }) => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string>('');
  const [uploaded, setUploaded] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFiles = (files: FileList | null) => {
    console.log('Files:', files);
    if (uploaded) return;     
    console.log("attempt")           // already done
    if (files && files.length > 0) {
      const chosen = files[0];
      const allowed = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      ];
      if (!allowed.includes(chosen.type)) {
        setError('Only PDF or Word documents are allowed.');
        return;
      }
      console.log('File:', chosen);
      setError('');
      setFile(chosen);
    }
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const onDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  const handleClear = () => {
    if (uploaded) return;                // cannot clear once uploaded
    setFile(null);
    setError('');
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleUploadClick = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }
    try {
      await onUpload?.(file);
      setUploaded(true);
    } catch (err) {
      setError('Upload failed. Please try again.');
    }
  };

  return (
    <div className="w-full max-w-lg mx-auto space-y-4">
      <label className="block text-sm font-medium text-gray-700">
        {uploaded ? 'Resume Uploaded' : 'Upload Your Resume'}
      </label>

      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        onClick={() => !uploaded && inputRef.current?.click()}
        className={`
          relative cursor-pointer rounded-lg border-2 p-6 flex flex-col items-center justify-center transition
          ${error 
            ? 'border-red-500' 
            : uploaded
              ? 'border-green-500 bg-green-50 pointer-events-none opacity-70'
              : 'border-dashed border-gray-300 hover:bg-gray-50'}
        `}
      >
        <input
          ref={inputRef}
          type="file"
          name="resume"
          accept=".pdf,.doc,.docx"
          multiple={false}
          disabled={uploaded}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={handleChange}
        />

        <svg
          className="w-12 h-12 text-gray-400 mb-3"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M12 4v16m8-8H4" />
        </svg>

        {file ? (
          <p className="text-gray-700">{file.name}</p>
        ) : (
          <p className="text-gray-500">
            {uploaded
              ? 'Your resume has been uploaded.'
              : 'Drag & drop or click to browse (PDF, DOC, DOCX)'}
          </p>
        )}
      </div>

      {!uploaded && file && (
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={handleClear}
            className="text-sm text-red-500 hover:underline"
          >
            Remove file
          </button>
          <button
            type="button"
            onClick={handleUploadClick}
            className="bg-dark-green text-white px-4 py-2 rounded-lg font-medium hover:bg-myrtle-green transition"
          >
            Upload
          </button>
        </div>
      )}

      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default ResumeUpload;
