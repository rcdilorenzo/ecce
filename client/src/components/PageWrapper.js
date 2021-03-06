import React from 'react';

const PageWrapper = ({ children }) => (
  <main className="max-w-lg mx-auto p-3 pb-5 overflow-hidden">
    {children}
  </main>
);

export default PageWrapper;
