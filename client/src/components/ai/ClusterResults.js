import React, { useState, useEffect } from 'react';
import LoadingIndicator from 'react-loading-indicator';

import scrollToComponent from 'react-scroll-to-component';

import PassageGroupBlock from './PassageGroupBlock';

const ClusterResults = ({ data }) => {
  const [openUUID, setOpenUUID] = useState(null);
  const [ref, setRef] = useState(null);

  const openingCallback = (_ref, uuid) => {
    setOpenUUID(uuid);
    setRef(_ref);
  };

  useEffect(() => {
    if (ref) {
      scrollToComponent(ref, { align: 'top', duration: 50, offset: -100 });
      setRef(null);
    }
  }, [ref, setRef]);

  return (
    <React.Fragment>
      <h2>Passages</h2>
      {data.length === 0 && <p className="list-item">
        <LoadingIndicator />
        <span className="ml-2">Loading</span>
      </p>}
      {data.length > 0 && data.map(c =>
        <PassageGroupBlock
          key={c.uuid}
          open={c.uuid === openUUID}
          opening={openingCallback}
          cluster={c} />
      )}
    </React.Fragment>
  );
};

export default ClusterResults;
