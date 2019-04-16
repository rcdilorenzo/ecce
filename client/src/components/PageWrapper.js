import React from 'react';

const PageWrapper = ({ children }) => (
  <div className="mx-auto pt-3 pb-5">
    <main className="max-w-lg mx-auto">
      {children}
    </main>
  </div>
);

export default PageWrapper;
