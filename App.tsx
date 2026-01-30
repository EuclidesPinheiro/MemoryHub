
import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Explorer } from './pages/Explorer';
import { Playground } from './pages/Playground';
import { Docs } from './pages/Docs';
import './styles.css';

const App = () => {
  const [page, setPage] = useState('explorer');

  const renderPage = () => {
    switch (page) {
      case 'explorer': return <Explorer />;
      case 'playground': return <Playground />;
      case 'docs': return <Docs />;
      default: return <Explorer />;
    }
  };

  return (
    <div className="app-layout">
      <Sidebar currentPage={page} onNavigate={setPage} />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
};

export default App;
