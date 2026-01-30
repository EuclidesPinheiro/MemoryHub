
import React from 'react';
import { Copy, Check } from 'lucide-react';

export const Docs: React.FC = () => {
  const [copied, setCopied] = React.useState(false);

  const pythonCode = `import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select, col, or_
from sqlalchemy.types import JSON
from pydantic import ConfigDict

# ... (Full backend implementation generated previously)

app = FastAPI(title="MemoryCloud MVP")

# Add your implementation here based on the specification
`;

  const copyCode = () => {
    navigator.clipboard.writeText(pythonCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h2>Developer Resources</h2>
          <p className="subtitle">Implementation details and API specification.</p>
        </div>
      </header>

      <div className="docs-content">
        <section className="docs-section">
          <h3>Backend Implementation (Python/FastAPI)</h3>
          <p>
            To run the production backend, copy the code below into a <code>main.py</code> file 
            and run <code>uvicorn main:app --reload</code>.
          </p>
          
          <div className="code-block-container">
            <button className="copy-btn" onClick={copyCode}>
              {copied ? <Check size={16} /> : <Copy size={16} />}
              {copied ? 'Copied' : 'Copy'}
            </button>
            <pre className="language-python">
              <code>{pythonCode}</code>
            </pre>
          </div>
        </section>

        <section className="docs-section">
          <h3>LLM System Prompt</h3>
          <div className="info-box">
            <p className="prompt-text">
              <strong>INSTRUÇÃO DE SISTEMA:</strong> Você tem acesso a uma ferramenta de memória persistente chamada MemoryCloud.
              Use o <code>app_id</code> "meu-agente" para salvar preferências do usuário e fatos importantes.
              Organize memórias por <code>namespace</code> (ex: profile, tasks).
            </p>
          </div>
        </section>
      </div>
    </div>
  );
};
