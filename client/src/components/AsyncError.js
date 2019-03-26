import React from 'react';
import Async from 'react-async';

const AsyncError = (_props) => {
  const renderError = error => {
    console.error(error);
    return (
      <p className="bg-red text-white p-5 rounded-sm">
        Oops: {error.message}
      </p>
    );
  };

  return (<Async.Rejected>{renderError}</Async.Rejected>);
};

export default AsyncError;
