import React from 'react';

const Dashboard = (props) => (
  <div className="absolute pin-l p-5 w-full">
    <div className="flex flex-wrap">
      {props.children}
    </div>
  </div>
);

export default Dashboard;
